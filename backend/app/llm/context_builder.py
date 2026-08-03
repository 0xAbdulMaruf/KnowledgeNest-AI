import re

from app.models.topic import Topic
from app.models.unit import Unit
from app.models.subject import Subject


MAX_CONTEXT_CHARS = 18000
MAX_RESOURCE_EXCERPT_CHARS = 1400
MAX_GENERAL_TOPICS = 18


def _active_resources(topic: Topic) -> list:
    priority = {
        "college_notes": 0,
        "external_notes": 1,
        "documentation": 2,
        "book": 3,
        "important_questions": 4,
        "practice_questions": 5,
        "pyq": 6,
        "video": 7,
    }
    return sorted(
        (resource for resource in topic.resources if resource.deleted_at is None),
        key=lambda resource: priority.get(resource.type.value, 99),
    )


def _resource_lines(topic: Topic, max_resources: int = 4) -> list[str]:
    lines: list[str] = []
    for resource in _active_resources(topic)[:max_resources]:
        excerpt = (resource.content or "").strip()[:MAX_RESOURCE_EXCERPT_CHARS]
        line = f"[{resource.type.value}] {resource.title}"
        if excerpt:
            line += f"\nExcerpt: {excerpt}"
        lines.append(line)
    return lines


def _topic_summary(topic: Topic) -> str:
    """One-line summary used inside unit/subject context lists."""
    parts = [f"- {topic.name}"]
    if topic.description:
        parts.append(f": {topic.description[:400]}")
    if topic.tags:
        parts.append(f" (tags: {', '.join(topic.tags[:6])})")
    return "".join(parts)


def build_context(topic: Topic, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Build detailed, bounded context for one topic from active academic content."""
    parts: list[str] = [f"Topic: {topic.name}"]
    if topic.description:
        parts.append(f"Description: {topic.description}")
    if topic.tags:
        parts.append(f"Tags: {', '.join(topic.tags)}")
    if topic.unit:
        parts.append(f"Unit: {topic.unit.name}")
        if topic.unit.subject:
            parts.append(f"Subject: {topic.unit.subject.name}")

    resources = _resource_lines(topic)
    if resources:
        parts.append("\n--- Active Resources ---")
        parts.extend(resources)

    return "\n".join(parts)[:max_chars]


def build_unit_context(unit: Unit, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Build curriculum context for a whole unit: name, description, and topic summaries."""
    parts: list[str] = [f"Unit: {unit.name}"]
    if unit.description:
        parts.append(f"Description: {unit.description}")
    if unit.subject:
        parts.append(f"Subject: {unit.subject.name}")
    if unit.topics:
        parts.append(f"\nTopics in this unit ({len(unit.topics)}):")
        for topic in sorted(unit.topics, key=lambda t: t.name):
            parts.append(_topic_summary(topic))
    return "\n".join(parts)[:max_chars]


def build_subject_context(subject: Subject, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Build curriculum map for a whole subject: name, code, unit and topic summaries."""
    parts: list[str] = [f"Subject: {subject.name}"]
    if subject.code:
        parts.append(f"Code: {subject.code}")
    if subject.description:
        parts.append(f"Description: {subject.description}")
    if subject.units:
        parts.append(f"\nUnits in this subject ({len(subject.units)}):")
        for unit in sorted(subject.units, key=lambda u: u.number if u.number is not None else 0):
            parts.append(f"  - Unit {unit.number}: {unit.name}")
            if unit.topics:
                for topic in sorted(unit.topics, key=lambda t: t.name):
                    parts.append(f"      {_topic_summary(topic)}")
    return "\n".join(parts)[:max_chars]


def _topic_search_text(topic: Topic) -> str:
    values = [topic.name, topic.description or "", " ".join(topic.tags or [])]
    if topic.unit:
        values.extend([topic.unit.name, topic.unit.description or ""])
        if topic.unit.subject:
            values.extend([topic.unit.subject.name, topic.unit.subject.description or ""])
    return " ".join(values).lower()


def _topic_score(topic: Topic, query_terms: set[str]) -> float:
    text = _topic_search_text(topic)
    name = topic.name.lower()
    matches = sum(1 for term in query_terms if term in text)
    name_matches = sum(1 for term in query_terms if term in name)
    return (topic.importance_score or 0.0) + matches * 2.0 + name_matches * 3.0


def build_general_context(topics: list[Topic], question: str, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Build a compact curriculum map plus the most relevant active topics.

    General chat has no selected topic, so context is ranked against the question and
    bounded to keep the model focused. The model may use general knowledge when this
    curriculum context is not relevant.
    """
    query_terms = {
        term for term in re.findall(r"[a-zA-Z0-9_]{3,}", question.lower())
        if term not in {"the", "and", "for", "with", "what", "how", "why", "can", "this", "that"}
    }
    ranked_topics = sorted(
        topics,
        key=lambda topic: (-_topic_score(topic, query_terms), topic.name.lower()),
    )[:MAX_GENERAL_TOPICS]

    parts = [
        "Curriculum context (use only when relevant to the student's request):",
        "The platform covers the following subjects, units, and high-priority topics.",
    ]
    for topic in ranked_topics:
        subject_name = topic.unit.subject.name if topic.unit and topic.unit.subject else ""
        unit_name = topic.unit.name if topic.unit else ""
        location = " / ".join(value for value in (subject_name, unit_name) if value)
        line = f"- {location + ' / ' if location else ''}{topic.name}"
        if topic.description:
            line += f": {topic.description[:500]}"
        if topic.tags:
            line += f" (tags: {', '.join(topic.tags[:8])})"
        parts.append(line)
        resources = _resource_lines(topic, max_resources=2)
        if resources:
            parts.append("  Resources: " + " | ".join(resources))

    return "\n".join(parts)[:max_chars]

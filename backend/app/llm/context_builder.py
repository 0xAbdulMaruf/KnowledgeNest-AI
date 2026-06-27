from app.models.topic import Topic


def build_context(topic: Topic) -> str:
    parts = []
    parts.append(f"Topic: {topic.name}")
    if topic.description:
        parts.append(f"Description: {topic.description}")
    if topic.tags:
        parts.append(f"Tags: {', '.join(topic.tags)}")

    if topic.unit:
        parts.append(f"Unit: {topic.unit.name}")
        if topic.unit.subject:
            parts.append(f"Subject: {topic.unit.subject.name}")

    if topic.resources:
        parts.append("\n--- Resources ---")
        for r in topic.resources:
            res_line = f"[{r.type.value}] {r.title}"
            if r.url:
                res_line += f" - URL: {r.url}"
            if r.content:
                res_line += f"\nContent excerpt: {r.content[:500]}"
            parts.append(res_line)

    return "\n".join(parts)

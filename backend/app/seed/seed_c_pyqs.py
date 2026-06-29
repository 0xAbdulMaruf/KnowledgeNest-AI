import sys
import os
import json
import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal, engine, Base
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.topic import Topic
from app.models.resource import Resource, ResourceType


def extract_questions_from_json(data):
    """Extract all questions from PYQ JSON data."""
    questions = []
    
    # Extract MCQ questions
    if "group_a" in data:
        for q in data["group_a"].get("questions", []):
            questions.append({
                "id": q.get("id", ""),
                "question": q.get("question", ""),
                "type": "MCQ",
                "options": q.get("options", [])
            })
    
    # Extract question_1 part_a (older format)
    if "question_1" in data:
        if "part_a" in data["question_1"]:
            for q in data["question_1"]["part_a"].get("questions", []):
                questions.append({
                    "id": q.get("id", ""),
                    "question": q.get("question", ""),
                    "type": "MCQ",
                    "options": q.get("options", [])
                })
        if "part_b" in data["question_1"]:
            for q in data["question_1"]["part_b"].get("questions", []):
                questions.append({
                    "id": q.get("id", ""),
                    "question": q.get("code", ""),
                    "type": "Program Output"
                })
    
    # Extract descriptive questions
    if "descriptive_questions" in data:
        for section in data["descriptive_questions"]:
            for q in section.get("questions", []):
                if isinstance(q, str):
                    questions.append({
                        "id": f"Q{section.get('number', '')}",
                        "question": q,
                        "type": "Descriptive",
                        "marks": section.get("marks", "")
                    })
    
    # Extract group_b questions (newer format)
    if "group_b" in data:
        for section in data["group_b"].get("questions", []):
            for q in section.get("questions", []):
                if isinstance(q, str):
                    questions.append({
                        "id": f"Q{section.get('number', '')}",
                        "question": q,
                        "type": "Descriptive",
                        "marks": section.get("marks", "")
                    })
    
    return questions


def map_question_to_topic(question_text):
    """Map a question to the most relevant topic based on keywords."""
    question_lower = question_text.lower()
    
    # Unit 1: Basics of C
    if any(kw in question_lower for kw in ["variable", "data type", "operator", "printf", "scanf", "format specifier", "keyword", "identifier", "constant", "token"]):
        return "Basics of C"
    
    # Unit 2: Decision Control and Looping
    if any(kw in question_lower for kw in ["if", "else", "switch", "loop", "while", "for", "do-while", "break", "continue", "goto", "nested loop", "infinite loop"]):
        return "Decision Control and Looping Statements"
    
    # Unit 3: Arrays and Strings
    if any(kw in question_lower for kw in ["array", "string", "strlen", "strcpy", "strcat", "strcmp", "2d array", "matrix", "substring"]):
        return "Subscripted Variables / Arrays"
    
    # Unit 4: Functions
    if any(kw in question_lower for kw in ["function", "recursion", "recursive", "storage class", "auto", "static", "extern", "register", "call by", "parameter", "argument"]):
        return "User defined functions"
    
    # Unit 5: Pointers
    if any(kw in question_lower for kw in ["pointer", "address", "dereference", "malloc", "calloc", "realloc", "free", "dynamic memory", "pointer to pointer"]):
        return "Pointers in C"
    
    # Default to Unit 1
    return "Basics of C"


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    pyq_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "FilesBYuser", "C")
    
    if not os.path.exists(pyq_dir):
        print(f"PYQ directory not found: {pyq_dir}")
        return
    
    # Get C Programming subject
    c_subject = db.query(Subject).filter(Subject.code == "CST201").first()
    if not c_subject:
        print("C Programming subject not found. Run seed_c_python.py first.")
        return
    
    # Get all units for C Programming
    units = db.query(Unit).filter(Unit.subject_id == c_subject.id).all()
    unit_map = {u.name: u for u in units}
    
    # Get all topics for C Programming
    topics = db.query(Topic).filter(Topic.unit_id.in_([u.id for u in units])).all()
    topic_map = {}
    for t in topics:
        if t.unit.name not in topic_map:
            topic_map[t.unit.name] = []
        topic_map[t.unit.name].append(t)
    
    # Process each PYQ file
    pyq_files = glob.glob(os.path.join(pyq_dir, "*.txt"))
    
    for pyq_file in pyq_files:
        filename = os.path.basename(pyq_file)
        print(f"Processing: {filename}")
        
        try:
            with open(pyq_file, 'r') as f:
                data = json.load(f)
            
            exam_info = data.get("exam", {})
            session = exam_info.get("session", "Unknown")
            title = exam_info.get("title", "C Programming")
            
            # Extract questions
            questions = extract_questions_from_json(data)
            
            # Create PYQ resource for each unit
            for unit_name, unit_topics in topic_map.items():
                # Filter questions relevant to this unit
                unit_questions = []
                for q in questions:
                    mapped_unit = map_question_to_topic(q["question"])
                    if mapped_unit == unit_name:
                        unit_questions.append(q)
                
                if not unit_questions:
                    continue
                
                # Create content string
                content_lines = [f"Previous Year Questions - {session}", f"Subject: {title}", ""]
                for q in unit_questions[:10]:  # Limit to 10 questions per resource
                    content_lines.append(f"[{q['id']}] {q['question']}")
                    if q.get("options"):
                        for i, opt in enumerate(q["options"]):
                            content_lines.append(f"  {chr(97+i)}) {opt}")
                    content_lines.append("")
                
                content = "\n".join(content_lines)
                
                # Add to first topic in unit (or create a general PYQ topic)
                target_topic = unit_topics[0] if unit_topics else None
                
                if target_topic:
                    # Check if PYQ already exists
                    existing = db.query(Resource).filter(
                        Resource.topic_id == target_topic.id,
                        Resource.type == ResourceType.pyq,
                        Resource.title.like(f"%{session}%")
                    ).first()
                    
                    if not existing:
                        resource = Resource(
                            topic_id=target_topic.id,
                            type=ResourceType.pyq,
                            title=f"PYQ {session} - {title}",
                            url=f"https://college.edu/pyq/c-{session.lower().replace(' ', '-')}",
                            content=content,
                            metadata_={"session": session, "year": session.split()[-1], "source": "wbsttevsd"}
                        )
                        db.add(resource)
                        print(f"  Added PYQ for {unit_name}: {len(unit_questions)} questions")
        
        except Exception as e:
            print(f"  Error processing {filename}: {e}")
    
    db.commit()
    print("\nPYQ seeding completed!")
    db.close()


if __name__ == "__main__":
    run_seed()

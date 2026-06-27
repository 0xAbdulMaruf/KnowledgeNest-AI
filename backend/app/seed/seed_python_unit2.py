import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal, engine, Base
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.topic import Topic
from app.models.resource import Resource, ResourceType


PYTHON_UNIT2_TOPICS = [
    {
        "name": "Conditional Statements - if, elif, else",
        "description": "if statement, if-else, if-elif-else, nested if, ternary operator, match-case statement, truthy/falsy values, short-hand if",
        "tags": ["if-elif-else", "conditional", "ternary", "truthy-falsy", "match-case", "nested-if"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Python Conditionals",
                "url": "https://college.edu/notes/python-conditionals",
                "content": "if condition: ... elif condition: ... else: ... No braces, indentation-based. Ternary: x if condition else y. Falsy values: None, False, 0, 0.0, '', [], {}, set(). Nested if: if within if. match-case (Python 3.10+). Short-hand if: single line. if-elif-else chain for multiple conditions."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Conditional Statements in Python",
                "url": "https://www.geeksforgeeks.org/python/conditional-statements-in-python/",
                "content": "Conditional statements control flow based on conditions. If: executes when condition is True. If-else: True block or False block. If-elif-else: multiple conditions checked sequentially. Nested if-else: if inside another if/else. Ternary: value_if_true if condition else value_if_false. Match-case: compare value against patterns (Python 3.10+). Short-hand if: single line execution."
            },
            {
                "type": "video",
                "title": "YouTube - Python Conditional Statements",
                "url": "https://www.youtube.com/watch?v=python-conditionals"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Conditional Statements",
                "url": "https://college.edu/pyq/python-conditionals-2023",
                "content": "Q1: What is the difference between if-else and elif? Q2: Explain ternary operator with example. Q3: What are truthy and falsy values? Q4: Write a program to find largest of three numbers. Q5: Explain match-case statement."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Conditional Statements",
                "url": "https://college.edu/practice/python-conditionals",
                "content": "1. Grade calculator (A/B/C/D/F). 2. Leap year check. 3. Largest of three numbers. 4. Menu-driven calculator. 5. Check positive/negative/zero. 6. Eligibility check (age, marks). 7. Simple calculator with match-case."
            }
        ]
    },
    {
        "name": "For Loop and Iteration",
        "description": "for loop with range(), iterating over sequences (list, string, tuple, dict, set), enumerate(), zip(), nested for loops, loop control (break, continue, else), list comprehension",
        "tags": ["for-loop", "range", "enumerate", "zip", "iteration", "break", "continue", "list-comprehension"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Python For Loop",
                "url": "https://college.edu/notes/python-for",
                "content": "for item in iterable: ... range(n), range(start, stop, step). Iterating: lists, strings, tuples, dicts, sets, files. enumerate(seq) gives (index, value). zip(seq1, seq2) pairs elements. Nested: for i in ...: for j in .... break/continue/else. List comprehension: [expr for item in iterable]. Iterating by index: range(len(seq))."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Loops in Python",
                "url": "https://www.geeksforgeeks.org/python/loops-in-python/",
                "content": "For loops iterate over sequences (list, tuple, string, range). Executes block once per item. range(0, n) generates 0 to n-1. Iterating by index: range(len(sequence)). While loop: executes while condition is True. Infinite while loop: condition always True. Nested loops: loop inside loop, inner executes fully for each outer iteration. break: exit loop. continue: skip to next iteration."
            },
            {
                "type": "video",
                "title": "YouTube - Python For Loop Tutorial",
                "url": "https://www.youtube.com/watch?v=python-for-loop"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - For Loop",
                "url": "https://college.edu/pyq/python-for-loop-2023",
                "content": "Q1: What is the difference between range() and len()? Q2: Explain enumerate() with example. Q3: What is list comprehension? Q4: Write a program to print Fibonacci series. Q5: Explain break and continue with examples."
            },
            {
                "type": "coding_problems",
                "title": "Practice - For Loop",
                "url": "https://college.edu/practice/python-for-loop",
                "content": "1. Print patterns (triangle, pyramid, diamond). 2. Fibonacci series. 3. Prime numbers in range. 4. Factorial using loop. 5. Multiplication table. 6. Sum of digits. 7. Reverse a number. 8. List comprehension exercises."
            }
        ]
    },
    {
        "name": "While Loop",
        "description": "while loop syntax, infinite while loop, while-else, loop control (break, continue, pass), sentinel values, do-while simulation",
        "tags": ["while-loop", "break", "continue", "pass", "infinite-loop", "while-else", "sentinel"],
        "importance_score": 0.85,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Python While Loop",
                "url": "https://college.edu/notes/python-while",
                "content": "while condition: ... Executes while condition is True. while True: (infinite). while-else: else executes if loop completes normally (no break). break: exit loop. continue: skip to next iteration. pass: do nothing (placeholder). Sentinel values: special value to stop input. Do-while simulation: while True with break."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Loops in Python",
                "url": "https://www.geeksforgeeks.org/python/loops-in-python/",
                "content": "While loop repeatedly executes block while condition is True. When condition becomes False, execution continues after loop. Infinite while loop: condition always True (use with caution). Nested loops: inner loop executes fully for each outer iteration. Counter-controlled: use counter variable. Sentinel-controlled: use special value to stop."
            },
            {
                "type": "video",
                "title": "YouTube - Python While Loop",
                "url": "https://www.youtube.com/watch?v=python-while-loop"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - While Loop",
                "url": "https://college.edu/pyq/python-while-loop-2023",
                "content": "Q1: What is the difference between for and while loop? Q2: Explain while-else with example. Q3: What is an infinite loop? How to avoid? Q4: Write a program to reverse a number using while. Q5: Explain sentinel-controlled loop."
            },
            {
                "type": "coding_problems",
                "title": "Practice - While Loop",
                "url": "https://college.edu/practice/python-while-loop",
                "content": "1. Guess the number game. 2. Sum until sentinel value. 3. Reverse a number. 4. GCD using while. 5. Armstrong number check. 6. Menu-driven program. 7. Count digits in number. 8. Do-while simulation."
            }
        ]
    }
]


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if Python subject exists
        python_subject = db.query(Subject).filter(Subject.code == "CST203").first()
        if not python_subject:
            print("Python subject not found. Run seed_c_python.py first.")
            return

        # Get or create Unit 2
        unit2 = db.query(Unit).filter(
            Unit.subject_id == python_subject.id,
            Unit.number == 2
        ).first()

        if not unit2:
            unit2 = Unit(
                name="Control Structures",
                number=2,
                subject_id=python_subject.id,
                description="if-elif-else, for loop, while loop, break, continue, pass, nested loops"
            )
            db.add(unit2)
            db.flush()

        # Clear existing topics for this unit
        existing_topics = db.query(Topic).filter(Topic.unit_id == unit2.id).all()
        for t in existing_topics:
            db.delete(t)
        db.flush()

        # Create topics
        for topic_data in PYTHON_UNIT2_TOPICS:
            topic = Topic(
                name=topic_data["name"],
                unit_id=unit2.id,
                description=topic_data["description"],
                tags=topic_data["tags"],
                importance_score=topic_data["importance_score"]
            )
            db.add(topic)
            db.flush()

            # Create resources
            for res_data in topic_data["resources"]:
                resource = Resource(
                    topic_id=topic.id,
                    type=ResourceType(res_data["type"]),
                    title=res_data["title"],
                    url=res_data.get("url", ""),
                    content=res_data.get("content", ""),
                    metadata_={"source": "geeksforgeeks+syllabus", "difficulty": "medium"}
                )
                db.add(resource)

        db.commit()
        print("Python Unit 2 detailed dataset seeded successfully!")
        print(f"Created {len(PYTHON_UNIT2_TOPICS)} topics with detailed resources")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

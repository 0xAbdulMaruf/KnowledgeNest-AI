import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal, engine, Base
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.topic import Topic
from app.models.resource import Resource, ResourceType


PYTHON_UNIT1_TOPICS = [
    {
        "name": "Introduction to Python",
        "description": "History of Python by Guido van Rossum (1991), features (interpreted, dynamically typed, indentation-based), installation, basic syntax, interactive interpreter, Hello World program",
        "tags": ["python-intro", "history", "features", "installation", "hello-world"],
        "importance_score": 0.8,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Introduction to Python",
                "url": "https://college.edu/notes/python-intro",
                "content": "Python: high-level, interpreted, dynamically typed language by Guido van Rossum (1991). Features: easy syntax, indentation-based, extensive libraries, cross-platform, object-oriented, interpreted. Versions: Python 2 (legacy) vs Python 3 (current). Interactive mode: python3 interpreter. Script mode: python3 script.py. Hello World: print('Hello, World!'). Comments: # single line, '''multi line'''."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Introduction to Python",
                "url": "https://www.geeksforgeeks.org/python/introduction-to-python/",
                "content": "Python is a high-level programming language known for its simple and readable syntax. Features: allows writing clean code with fewer lines, supports multiple programming paradigms (object-oriented, functional, procedural), widely used in web development, automation, data analysis, AI, dynamically typed with automatic garbage collection. Hello World demonstrates basic structure: print('Hello, World!'). Python uses indentation instead of braces."
            },
            {
                "type": "video",
                "title": "NPTEL - Python Basics Introduction",
                "url": "https://nptel.ac.in/courses/python-basics"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Python Basics",
                "url": "https://college.edu/pyq/python-intro-2023",
                "content": "Q1: Who developed Python and when? Q2: List any 5 features of Python. Q3: What is the difference between Python 2 and Python 3? Q4: Write a Hello World program in Python. Q5: Explain indentation in Python with example."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Python Basics",
                "url": "https://college.edu/practice/python-basics",
                "content": "1. Write Hello World program. 2. Print your name and age. 3. Add two numbers and print result. 4. Calculate area of circle. 5. Print multiplication table of 5."
            },
            {
                "type": "book",
                "title": "Python Programming: Using Problem Solving Approach - Reema Thareja",
                "url": "https://college.edu/books/python-reema-thareja"
            }
        ]
    },
    {
        "name": "Python Variables and Data Types",
        "description": "Variable declaration, naming rules, dynamic typing, type() function, int, float, complex, bool, str, type conversion, type casting, object reference, garbage collection",
        "tags": ["variables", "data-types", "int", "float", "string", "bool", "type-casting", "dynamic-typing"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Python Variables",
                "url": "https://college.edu/notes/python-variables",
                "content": "Variables: no declaration needed, dynamically typed. x = 10 (int), y = 3.14 (float), z = 'hello' (str), b = True (bool). Type checking: type(x). Naming: start with letter/underscore, case sensitive, no keywords. Multiple assignment: a, b, c = 1, 2, 3. Same value: a = b = c = 100. Type conversion: int(), float(), str(), bool(). Delete: del x. Object reference: variables store references to objects. Swapping: a, b = b, a."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Python Variables",
                "url": "https://www.geeksforgeeks.org/python/python-variables/",
                "content": "Variables store data referenced during execution. No explicit type declaration needed. Rules: names can contain letters/digits/underscore, first char cannot be digit, case-sensitive, no keywords. Basic assignment: x = 5. Dynamic typing: same variable can store different types. Multiple assignment: x, y, z = 1, 2.5, 'Python'. Object reference: variables reference objects, not values. Shared reference: y = x makes y reference same object. Delete: del x removes variable."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Python Data Types",
                "url": "https://www.geeksforgeeks.org/python/python-data-types/",
                "content": "Data types define type of value stored in variable. Numeric: int (whole numbers), float (decimal), complex (real+imaginary). Sequence: str (text), list (mutable ordered), tuple (immutable ordered). Boolean: True/False. Set: unordered unique elements. Dictionary: key-value pairs. Type checking: type(x). Type casting: int(), float(), str()."
            },
            {
                "type": "video",
                "title": "YouTube - Python Variables and Data Types",
                "url": "https://www.youtube.com/watch?v=python-variables-datatypes"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Variables and Data Types",
                "url": "https://college.edu/pyq/python-variables-2023",
                "content": "Q1: What is dynamic typing? Give example. Q2: What are the naming rules for Python variables? Q3: Explain type conversion with examples. Q4: What is the difference between mutable and immutable data types? Q5: Write a program to swap two variables."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Variables and Data Types",
                "url": "https://college.edu/practice/python-variables",
                "content": "1. Swap two variables without temp. 2. Check type of different variables. 3. Type conversion: string to int, int to float. 4. Calculate area of rectangle using variables. 5. Demonstrate multiple assignment."
            }
        ]
    },
    {
        "name": "Python Strings",
        "description": "String creation, indexing, slicing, string methods (upper, lower, strip, replace, split, join, find, count), formatting (f-strings, format()), concatenation, repetition, immutability, membership testing",
        "tags": ["strings", "slicing", "string-methods", "f-strings", "formatting", "immutability"],
        "importance_score": 0.9,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Python Strings",
                "url": "https://college.edu/notes/python-strings",
                "content": "Strings: immutable sequences of characters. Single/double/triple quotes. Indexing: s[0], s[-1]. Slicing: s[start:stop:step]. Methods: upper(), lower(), strip(), split(), join(), find(), replace(), count(), startswith(), endswith(). Formatting: f'Hello {name}', '{}'.format(), %s. Concatenation: s1 + s2. Repetition: s * n. Membership: 'x' in s. Escape: \\n, \\t, \\\\."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Python Strings",
                "url": "https://www.geeksforgeeks.org/python/python-string/",
                "content": "Strings are sequence of characters in quotes. No separate character type. Creating: single or double quotes. Multi-line: triple quotes. Accessing: positive indexing (0-based), negative indexing (-1 from end). Slicing: s[start:end] extracts portion. Looping: for char in s. Immutability: cannot change after creation. Methods: len(), upper(), lower(), strip(), replace(). Concatenation: + operator. Repetition: * operator. Formatting: f-strings, format(). Membership: in keyword."
            },
            {
                "type": "video",
                "title": "YouTube - Python Strings Tutorial",
                "url": "https://www.youtube.com/watch?v=python-strings"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Strings",
                "url": "https://college.edu/pyq/python-strings-2023",
                "content": "Q1: What is string slicing? Give examples. Q2: Explain string immutability. Q3: List any 5 string methods with examples. Q4: What is the difference between remove() and pop()? Q5: Write a program to check if a string is palindrome."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Python Strings",
                "url": "https://college.edu/practice/python-strings",
                "content": "1. Reverse a string. 2. Check palindrome. 3. Count words in string. 4. Count vowels and consonants. 5. String formatting exercises. 6. Replace specific character. 7. Extract substring."
            }
        ]
    },
    {
        "name": "Python Lists",
        "description": "List creation, indexing, slicing, list methods (append, insert, extend, remove, pop, sort, reverse, index, count), list comprehensions, nested lists, mutability, iteration",
        "tags": ["lists", "list-methods", "list-comprehension", "slicing", "mutable"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Python Lists",
                "url": "https://college.edu/notes/python-lists",
                "content": "Lists: mutable, ordered, allows duplicates. Create: [] or list(). Methods: append(x), insert(i, x), extend([x,y]), remove(x), pop(i), sort(), reverse(), index(x), count(x). Slicing: l[start:stop:step]. List comprehension: [x for x in range(10)]. Nested lists: [[1,2],[3,4]]. Copy: l.copy() or l[:]. Concatenation: l1 + l2. Repetition: l * n. Iteration: for item in l."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Python Lists",
                "url": "https://www.geeksforgeeks.org/python/python-lists/",
                "content": "List is built-in data structure for ordered collection. Dynamic, resizable, multiple data types. Mutable: elements can be changed. Ordered: maintains insertion order. Index-based: accessed by position. Creating: square brackets, list(), multiplication. Accessing: zero-based indexing, negative indexing. Adding: append() end, insert() specific position, extend() multiple. Updating: assign new value by index. Removing: remove() first occurrence, pop() specific index, del statement, clear() all. Iterating: for loop. Nested lists: list inside list."
            },
            {
                "type": "video",
                "title": "YouTube - Python Lists Tutorial",
                "url": "https://www.youtube.com/watch?v=python-lists"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Lists",
                "url": "https://college.edu/pyq/python-lists-2023",
                "content": "Q1: What is the difference between append() and extend()? Q2: Explain list slicing with examples. Q3: What is list comprehension? Give example. Q4: How to remove duplicates from a list? Q5: Write a program to sort a list without using sort()."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Python Lists",
                "url": "https://college.edu/practice/python-lists",
                "content": "1. Find max/min without built-in. 2. Flatten nested list. 3. Remove duplicates. 4. List comprehension: squares, even numbers. 5. Sort list of tuples. 6. Reverse a list. 7. Merge two lists."
            }
        ]
    },
    {
        "name": "Python Tuples, Dictionaries and Sets",
        "description": "Tuples (immutable, ordered, packing/unpacking), Dictionaries (key-value pairs, methods), Sets (unique elements, union, intersection, difference), frozenset",
        "tags": ["tuples", "dictionaries", "sets", "key-value", "immutable", "unique"],
        "importance_score": 0.85,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Tuples, Dicts, Sets",
                "url": "https://college.edu/notes/python-data-structs",
                "content": "Tuples: immutable, ordered. t = (1, 2, 3). Methods: count(), index(). Packing/unpacking. Single element: t = (1,). Dictionaries: mutable, key-value. d = {'name': 'John'}. Methods: keys(), values(), items(), get(), update(), pop(). Sets: unordered, unique. s = {1, 2, 3}. Methods: add(), remove(), union(), intersection(), difference(). Frozenset: immutable set."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Python Tuples",
                "url": "https://www.geeksforgeeks.org/python/python-tuples/",
                "content": "Tuple is immutable ordered collection. Similar to lists but cannot be changed. Mixed datatypes allowed. Creating: parentheses (), tuple() constructor. Accessing: indexing and slicing. Concatenation: + operator. Slicing: tuple[start:stop:step]. Deleting: del tuple (entire tuple only). Unpacking: a, b, c = tup. Asterisk unpacking: a, *b, c = tup."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Python Dictionaries",
                "url": "https://www.geeksforgeeks.org/python/python-dictionary/",
                "content": "Dictionary stores key-value pairs. Keys must be unique and immutable. Creating: {} or dict(). Accessing: d[key] or d.get(key). Adding/Updating: d[key] = value. Removing: del, pop(), popitem(), clear(). Iterating: keys(), values(), items(). Nested dictionaries: dictionary inside dictionary."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Python Sets",
                "url": "https://www.geeksforgeeks.org/python/sets-in-python/",
                "content": "Set stores unique items. Unordered, no duplicates. Creating: {} or set(). Type casting: set(list). Frozen sets: immutable version. Methods: add(), union(), intersection(), difference(), clear(). Operators: in, not in, ==, <=, <, >=, >, |, &, -, ^."
            },
            {
                "type": "video",
                "title": "YouTube - Python Data Structures",
                "url": "https://www.youtube.com/watch?v=python-data-structures"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Data Structures",
                "url": "https://college.edu/pyq/python-data-structs-2023",
                "content": "Q1: What is the difference between list and tuple? Q2: Explain dictionary methods with examples. Q3: What is a frozenset? Q4: How to merge two dictionaries? Q5: Write a program to count word frequency using dictionary."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Data Structures",
                "url": "https://college.edu/practice/python-data-structs",
                "content": "1. Word frequency counter using dict. 2. Merge two dictionaries. 3. Find common elements using sets. 4. Convert list to dictionary. 5. Tuple unpacking examples. 6. Set operations (union, intersection)."
            }
        ]
    },
    {
        "name": "Python Operators",
        "description": "Arithmetic (+, -, *, /, //, %, **), comparison (==, !=, >, <, >=, <=), logical (and, or, not), bitwise (&, |, ^, ~, <<, >>), assignment (=, +=, -=), membership (in, not in), identity (is, is not), precedence, associativity, ternary operator",
        "tags": ["operators", "arithmetic", "comparison", "logical", "bitwise", "membership", "precedence"],
        "importance_score": 0.85,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Python Operators",
                "url": "https://college.edu/notes/python-operators",
                "content": "Arithmetic: +, -, *, /, //, %, **. Comparison: ==, !=, >, <, >=, <=. Logical: and, or, not. Bitwise: &, |, ^, ~, <<, >>. Assignment: =, +=, -=, *=, /=, //=, **=. Membership: in, not in. Identity: is, is not. Ternary: x if condition else y. Precedence: ** > ~x > * / // % > + - > >> << > & > ^ | > comparison > not > and > or."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Python Operators",
                "url": "https://www.geeksforgeeks.org/python/python-operators/",
                "content": "Operators perform operations on values and variables. Types: Arithmetic (math operations), Comparison (compare values), Logical (combine conditions), Bitwise (bit-by-bit), Assignment (assign values), Membership (test in sequence), Identity (check same memory). Precedence determines which operation first. Associativity: left-to-right or right-to-left. Ternary: [on_true] if [expression] else [on_false]."
            },
            {
                "type": "video",
                "title": "YouTube - Python Operators Tutorial",
                "url": "https://www.youtube.com/watch?v=python-operators"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Operators",
                "url": "https://college.edu/pyq/python-operators-2023",
                "content": "Q1: What is the difference between / and //? Q2: Explain bitwise operators with examples. Q3: What is operator precedence? Q4: What is the difference between 'is' and '=='? Q5: Write a program using ternary operator."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Python Operators",
                "url": "https://college.edu/practice/python-operators",
                "content": "1. Calculator using arithmetic operators. 2. Check even/odd using bitwise AND. 3. Swap using XOR. 4. Find maximum using ternary. 5. Membership testing examples. 6. Precedence examples."
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
            # Create semester 3 if not exists
            semester = db.query(Semester).filter(Semester.number == 3).first()
            if not semester:
                semester = Semester(name="Semester 3", number=3)
                db.add(semester)
                db.flush()

            # Create Python subject
            python_subject = Subject(
                name="Scripting Languages (Python)",
                code="CST203",
                semester_id=semester.id,
                description="Learn Python programming covering variables, control structures, functions, file I/O, regular expressions, and Django framework",
                tags=["python", "scripting", "programming"]
            )
            db.add(python_subject)
            db.flush()

        # Get or create Unit 1
        unit1 = db.query(Unit).filter(
            Unit.subject_id == python_subject.id,
            Unit.number == 1
        ).first()

        if not unit1:
            unit1 = Unit(
                name="Introduction, Variables and Data Types",
                number=1,
                subject_id=python_subject.id,
                description="Python history, features, variables, numeric types, strings, lists, tuples, dictionaries, operators"
            )
            db.add(unit1)
            db.flush()

        # Clear existing topics for this unit
        existing_topics = db.query(Topic).filter(Topic.unit_id == unit1.id).all()
        for t in existing_topics:
            db.delete(t)
        db.flush()

        # Create topics
        for topic_data in PYTHON_UNIT1_TOPICS:
            topic = Topic(
                name=topic_data["name"],
                unit_id=unit1.id,
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
        print("Python Unit 1 detailed dataset seeded successfully!")
        print(f"Created {len(PYTHON_UNIT1_TOPICS)} topics with detailed resources")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal, engine, Base
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.topic import Topic
from app.models.resource import Resource, ResourceType


ALGORITHMS_UNIT1_TOPICS = [
    {
        "name": "Definitions and Characteristics of Algorithm",
        "description": "Algorithm definition, properties (finiteness, definiteness, input, output, effectiveness), how to express algorithms (natural language, flowchart, pseudocode), steps to design algorithms, algorithm analysis (priori and posteriori)",
        "tags": ["algorithm", "definition", "properties", "pseudocode", "flowchart", "analysis"],
        "importance_score": 0.9,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Introduction to Algorithms",
                "url": "https://college.edu/notes/algo-intro",
                "content": "Algorithm: finite set of well-defined instructions to solve a problem. Properties: Finiteness (terminates), Definiteness (unambiguous), Input (0 or more), Output (at least 1), Effectiveness (feasible steps). Express: Natural language, Flowchart, Pseudocode. Design: Define problem, identify constraints, determine inputs/outputs, design solution. Analysis: Priori (theoretical), Posteriori (practical)."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Introduction to Algorithms",
                "url": "https://www.geeksforgeeks.org/dsa/introduction-to-algorithms/",
                "content": "Algorithm is a set of finite, well-defined steps to solve a problem. Need: solve complex problems efficiently, automate processes, enable computers. Properties: Clear/Unambiguous, Well-Defined Inputs/Outputs, Finiteness, Effectiveness, Deterministic, Language Independent. Express: Natural Language, Flowchart, Pseudocode. Design: Problem Definition, Constraints, Inputs, Outputs, Solution Feasibility. Analysis: Priori (before implementation), Posteriori (after implementation)."
            },
            {
                "type": "video",
                "title": "YouTube - Introduction to Algorithms",
                "url": "https://www.youtube.com/watch?v=0IAPZzGSbME"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Algorithm Basics",
                "url": "https://college.edu/pyq/algo-basics-2023",
                "content": "Q1: Define algorithm and list its properties. Q2: What is the difference between algorithm and program? Q3: Explain priori and posteriori analysis. Q4: Write an algorithm to find largest of three numbers. Q5: What is pseudocode? Give example."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Algorithm Basics",
                "url": "https://college.edu/practice/algo-basics",
                "content": "1. Write algorithm to swap two numbers. 2. Write algorithm to check prime number. 3. Write algorithm to find factorial. 4. Write algorithm for Fibonacci series. 5. Convert algorithm to pseudocode."
            },
            {
                "type": "book",
                "title": "Introduction to Algorithms - CLRS (Chapter 1)",
                "url": "https://college.edu/books/clrs"
            }
        ]
    },
    {
        "name": "Data Abstraction",
        "description": "Abstract Data Types (ADT), data abstraction concepts, encapsulation, interface vs implementation, examples of ADTs (List, Stack, Queue, Dictionary)",
        "tags": ["abstraction", "adt", "encapsulation", "interface", "data-structures"],
        "importance_score": 0.8,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Data Abstraction",
                "url": "https://college.edu/notes/algo-abstraction",
                "content": "Data Abstraction: hiding implementation details, showing only essential features. Abstract Data Type (ADT): mathematical model with defined operations, independent of implementation. Examples: List (add, remove, get), Stack (push, pop, peek), Queue (enqueue, dequeue). Benefits: modularity, reusability, information hiding."
            },
            {
                "type": "external_notes",
                "title": "Data Abstraction Notes",
                "url": "https://college.edu/notes/data-abstraction",
                "content": "Data abstraction is the process of hiding implementation details while exposing only the necessary interface. ADT defines a data type by its behavior (operations) rather than its implementation. Key concepts: encapsulation (bundling data and methods), interface (what operations are available), implementation (how operations work). Common ADTs: List, Stack, Queue, Priority Queue, Dictionary, Set."
            },
            {
                "type": "video",
                "title": "YouTube - Abstract Data Types",
                "url": "https://www.youtube.com/watch?v=wgFhBkMKbcc"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Data Abstraction",
                "url": "https://college.edu/pyq/algo-abstraction-2023",
                "content": "Q1: What is data abstraction? Explain with example. Q2: Define ADT. List any 4 ADTs. Q3: Difference between abstraction and encapsulation. Q4: Why is abstraction important in algorithm design?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Data Abstraction",
                "url": "https://college.edu/practice/algo-abstraction",
                "content": "1. Implement Stack ADT using list. 2. Implement Queue ADT. 3. Design ADT for a Dictionary. 4. Compare Array ADT vs List ADT."
            }
        ]
    },
    {
        "name": "Sets, Multisets, Stacks, Queues",
        "description": "Set operations (union, intersection, difference), Multiset (bag), Stack (LIFO, push, pop), Queue (FIFO, enqueue, dequeue), applications of each",
        "tags": ["sets", "multisets", "stacks", "queues", "lifo", "fifo", "data-structures"],
        "importance_score": 0.9,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Sets, Stacks, Queues",
                "url": "https://college.edu/notes/algo-ds",
                "content": "Sets: collection of unique elements. Operations: Union (A∪B), Intersection (A∩B), Difference (A-B), Subset, Superset. Multiset: allows duplicate elements. Stack: LIFO structure. Operations: Push (add top), Pop (remove top), Peek (view top). Applications: expression evaluation, backtracking, recursion. Queue: FIFO structure. Operations: Enqueue (add rear), Dequeue (remove front). Applications: BFS, scheduling, buffering."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Stack Data Structure",
                "url": "https://www.w3schools.com/dsa/dsa_data_stacks.php",
                "content": "Stack is a linear data structure following LIFO (Last In First Out) principle. Main operations: Push (add element to top), Pop (remove element from top), Peek/Top (return top element). Stack can be implemented using arrays or linked lists. Applications: undo mechanisms, expression parsing, backtracking algorithms, function call management."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Queue Data Structure",
                "url": "https://www.w3schools.com/dsa/dsa_data_queues.php",
                "content": "Queue is a linear data structure following FIFO (First In First Out) principle. Main operations: Enqueue (add element to rear), Dequeue (remove element from front), Front (get front element). Types: Simple Queue, Circular Queue, Priority Queue, Double-Ended Queue (Deque). Applications: CPU scheduling, disk scheduling, handling requests."
            },
            {
                "type": "external_notes",
                "title": "Set and Multiset Data Structure",
                "url": "https://dev.to/fernandoblima/set-and-multiset-data-structure-algorithm-part-iii-1ea8",
                "content": "Set is an abstract data type that stores unique elements with no particular order. Operations: add, remove, contains, union, intersection, difference. Multiset (Bag) allows duplicate elements. Implementation: Hash Table (O(1) operations), BST (O(log n) operations). Applications: removing duplicates, membership testing, mathematical set operations."
            },
            {
                "type": "video",
                "title": "YouTube - Stack and Queue Data Structures",
                "url": "https://www.youtube.com/watch?v=FI4LIC8CJ0A"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Sets, Stacks, Queues",
                "url": "https://college.edu/pyq/algo-ds-2023",
                "content": "Q1: Explain Stack with operations and example. Q2: Difference between Stack and Queue. Q3: What is a Multiset? How does it differ from Set? Q4: List applications of Queue. Q5: Implement Stack using two Queues."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Sets, Stacks, Queues",
                "url": "https://college.edu/practice/algo-ds",
                "content": "1. Implement Stack using array. 2. Implement Queue using array. 3. Check balanced parentheses using Stack. 4. Implement Set operations (union, intersection). 5. Reverse a string using Stack. 6. Implement Circular Queue."
            }
        ]
    },
    {
        "name": "Asymptotic Notations",
        "description": "Big-O (upper bound, worst case), Omega (lower bound, best case), Theta (tight bound, average case), properties (reflexive, transitive, symmetric), examples, little-o and little-omega",
        "tags": ["big-o", "omega", "theta", "asymptotic", "complexity", "notation"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Asymptotic Notations",
                "url": "https://college.edu/notes/algo-notations",
                "content": "Asymptotic Notations: mathematical tools to represent time complexity. Big-O: upper bound (worst case). f(n) = O(g(n)) if f(n) <= c*g(n) for n >= n0. Omega: lower bound (best case). f(n) = Ω(g(n)) if f(n) >= c*g(n) for n >= n0. Theta: tight bound (average case). c1*g(n) <= f(n) <= c2*g(n). Properties: Reflexive, Transitive, Symmetric (Theta only). Little-o: strict upper bound. Little-omega: strict lower bound."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Asymptotic Notations",
                "url": "https://www.geeksforgeeks.org/dsa/types-of-asymptotic-notations-in-complexity-analysis-of-algorithms/",
                "content": "Asymptotic Notations analyze algorithm efficiency independent of machine constants. Three main notations: Theta (Θ) - exact bounds (average case), Big-O (O) - upper bound (worst case), Omega (Ω) - lower bound (best case). Properties: General (constant multiplication), Transitive, Reflexive, Symmetric (Theta), Transpose Symmetric (O and Ω). Examples: O(1) constant, O(n) linear, O(n²) quadratic."
            },
            {
                "type": "video",
                "title": "YouTube - Asymptotic Notation Big O, Omega, Theta",
                "url": "https://www.youtube.com/watch?v=0oD_AhoFVZo"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Asymptotic Notations",
                "url": "https://college.edu/pyq/algo-notations-2023",
                "content": "Q1: Explain Big-O notation with example. Q2: Difference between O, Ω, and Θ. Q3: What are properties of asymptotic notations? Q4: Find time complexity of given code. Q5: What is little-o notation?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Asymptotic Notations",
                "url": "https://college.edu/practice/algo-notations",
                "content": "1. Find Big-O of simple loop. 2. Find Big-O of nested loop. 3. Compare O(n) vs O(n²). 4. Find time complexity of recursive function. 5. Prove 2n+3 = O(n)."
            }
        ]
    },
    {
        "name": "Time and Space Complexity Analysis",
        "description": "Time complexity (best, average, worst case), space complexity (auxiliary space), how to analyze loops, recursion complexity, trade-offs between time and space",
        "tags": ["time-complexity", "space-complexity", "best-case", "worst-case", "average-case", "analysis"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Complexity Analysis",
                "url": "https://college.edu/notes/algo-complexity",
                "content": "Time Complexity: amount of time algorithm takes as function of input size. Best Case: minimum time (Omega). Average Case: expected time (Theta). Worst Case: maximum time (Big-O). Space Complexity: total memory used. Auxiliary Space: extra space excluding input. Analyze loops: multiply iterations. Recursion: use recurrence relation. Common complexities: O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)"
            },
            {
                "type": "external_notes",
                "title": "Medium - Time and Space Complexity Guide",
                "url": "https://medium.com/@pnandhiniofficial/time-and-space-complexity-a-beginners-guide-88d617d29d01",
                "content": "Time complexity measures how runtime grows with input size. Best case: fastest execution. Worst case: slowest execution. Average case: expected execution. Space complexity measures memory usage. Analyze: count operations, consider nested loops, handle recursion with recurrence relations. Common complexities: Constant O(1), Logarithmic O(log n), Linear O(n), Linearithmic O(n log n), Quadratic O(n²), Exponential O(2ⁿ)."
            },
            {
                "type": "video",
                "title": "YouTube - Time and Space Complexity",
                "url": "https://www.youtube.com/watch?v=FPuP9dKRf0A"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Complexity Analysis",
                "url": "https://college.edu/pyq/algo-complexity-2023",
                "content": "Q1: Explain best, average, worst case with example. Q2: Find time complexity of binary search. Q3: What is space complexity? Q4: Compare time vs space trade-off. Q5: Find complexity of recursive Fibonacci."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Complexity Analysis",
                "url": "https://college.edu/practice/algo-complexity",
                "content": "1. Analyze time complexity of linear search. 2. Analyze time complexity of binary search. 3. Find complexity of nested loops. 4. Analyze recursive function complexity. 5. Compare O(n²) vs O(n log n) sorting."
            }
        ]
    },
    {
        "name": "Programming Models (Divide and Conquer, Greedy, Dynamic Programming)",
        "description": "Divide and Conquer (divide, conquer, merge), Greedy algorithms (locally optimal choices), Dynamic Programming (overlapping subproblems, optimal substructure), when to use which approach",
        "tags": ["divide-conquer", "greedy", "dynamic-programming", "algorithm-paradigms", "optimization"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Algorithm Paradigms",
                "url": "https://college.edu/notes/algo-paradigms",
                "content": "Divide and Conquer: divide problem into subproblems, solve recursively, combine solutions. Examples: Merge Sort, Quick Sort, Binary Search. Greedy: make locally optimal choice at each step. Examples: Dijkstra, Kruskal, Huffman. Dynamic Programming: solve overlapping subproblems, store results. Two approaches: Memoization (top-down), Tabulation (bottom-up). When to use: D&C (independent subproblems), Greedy (optimal substructure), DP (overlapping subproblems)."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Divide and Conquer",
                "url": "https://www.geeksforgeeks.org/dsa/introduction-to-divide-and-conquer-algorithm/",
                "content": "Divide and Conquer: break problem into subproblems, solve individually, merge solutions. Three steps: Divide (break into smaller), Conquer (solve each), Merge (combine results). Characteristics: dividing problem, independence of subproblems, conquering each, combining solutions. Examples: Merge Sort, Quick Sort, Binary Search. Complexity: T(n) = aT(n/b) + f(n). Advantages: efficiency, parallelism, cache-friendly."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Greedy Algorithms",
                "url": "https://www.geeksforgeeks.org/dsa/greedy-algorithms/",
                "content": "Greedy algorithms make locally optimal choices at each step. At every step, choose the best option available. Sometimes sort array for next optimal choice. Check constraints after each choice. Not always optimal (coin change, 0/1 knapsack need DP). Examples where Greedy works: Fractional Knapsack, Dijkstra, Kruskal, Huffman Coding, Activity Selection, Job Sequencing."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Dynamic Programming",
                "url": "https://www.geeksforgeeks.org/dsa/introduction-to-dynamic-programming-data-structures-and-algorithm-tutorials/",
                "content": "DP solves complex problems by breaking into smaller overlapping subproblems, storing results to avoid recomputation. Characteristics: Optimal Substructure (use optimal subproblem results), Overlapping Subproblems (same subproblems solved repeatedly). Approaches: Top-Down (Memoization) - recursive with stored results, Bottom-Up (Tabulation) - iterative building up. Examples: Fibonacci, LCS, Edit Distance, Knapsack, Bellman-Ford."
            },
            {
                "type": "video",
                "title": "YouTube - Divide and Conquer, Greedy, DP",
                "url": "https://www.youtube.com/watch?v=obBV41aECq4"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Algorithm Paradigms",
                "url": "https://college.edu/pyq/algo-paradigms-2023",
                "content": "Q1: Explain Divide and Conquer with example. Q2: What is Greedy approach? When does it fail? Q3: Explain DP with Fibonacci example. Q4: Difference between Memoization and Tabulation. Q5: When to use D&C vs DP?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Algorithm Paradigms",
                "url": "https://college.edu/practice/algo-paradigms",
                "content": "1. Implement Merge Sort (D&C). 2. Implement Quick Sort (D&C). 3. Activity Selection (Greedy). 4. Fibonacci using DP (Memoization). 5. Fibonacci using DP (Tabulation). 6. Coin Change problem (DP). 7. 0/1 Knapsack (DP)."
            }
        ]
    }
]


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Get or create Semester 3
        semester = db.query(Semester).filter(Semester.number == 3).first()
        if not semester:
            semester = Semester(name="Semester 3", number=3)
            db.add(semester)
            db.flush()

        # Get or create Algorithms subject
        algo_subject = db.query(Subject).filter(Subject.code == "CST209").first()
        if not algo_subject:
            algo_subject = Subject(
                name="Algorithms",
                code="CST209",
                semester_id=semester.id,
                description="Fundamentals of algorithm design and analysis including sorting, searching, graph algorithms, and algorithm paradigms",
                tags=["algorithms", "dsa", "complexity", "sorting", "searching", "graphs"]
            )
            db.add(algo_subject)
            db.flush()

        # Get or create Unit 1
        unit1 = db.query(Unit).filter(
            Unit.subject_id == algo_subject.id,
            Unit.number == 1
        ).first()

        if not unit1:
            unit1 = Unit(
                name="Fundamentals of Algorithms",
                number=1,
                subject_id=algo_subject.id,
                description="Definitions, characteristics, data abstraction, sets, stacks, queues, asymptotic notations, time/space complexity, algorithm paradigms"
            )
            db.add(unit1)
            db.flush()

        # Clear existing topics for this unit
        existing_topics = db.query(Topic).filter(Topic.unit_id == unit1.id).all()
        for t in existing_topics:
            db.delete(t)
        db.flush()

        # Create topics
        for topic_data in ALGORITHMS_UNIT1_TOPICS:
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
                    metadata_={"source": "geeksforgeeks+w3schools+syllabus", "difficulty": "medium"}
                )
                db.add(resource)

        db.commit()
        print("Algorithms Unit 1 detailed dataset seeded successfully!")
        print(f"Created {len(ALGORITHMS_UNIT1_TOPICS)} topics with detailed resources")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

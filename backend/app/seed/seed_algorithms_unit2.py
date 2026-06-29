import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal, engine, Base
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.topic import Topic
from app.models.resource import Resource, ResourceType


ALGORITHMS_UNIT2_TOPICS = [
    {
        "name": "Introduction to Sorting Algorithms",
        "description": "Sorting problem overview, comparison-based vs non-comparison-based sorting, in-place vs stable sorting, internal vs external sorting, hybrid sorting",
        "tags": ["sorting", "comparison-based", "in-place", "stable", "hybrid"],
        "importance_score": 0.85,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Introduction to Sorting",
                "url": "https://college.edu/notes/algo-sorting-intro",
                "content": "Sorting: rearrangement of elements according to comparison operator. Types: Comparison-based (compare elements), Non-comparison-based (count/radix). In-place: O(1) extra space. Stable: maintains relative order of equal elements. Internal: all data in main memory. External: data on disk. Hybrid: combines multiple algorithms (e.g., IntroSort = QuickSort + InsertionSort)."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Introduction to Sorting",
                "url": "https://www.geeksforgeeks.org/dsa/introduction-to-sorting-algorithm/",
                "content": "Sorting refers to rearrangement of elements according to comparison operator. Important for: organizing datasets, enabling binary search, solving advanced problems. Types: In-place (constant space), Internal (main memory), External (disk), Stable (preserves order), Hybrid (multiple algorithms). Comparison-based: Bubble, Selection, Insertion, Merge, Quick, Heap. Non-comparison: Counting, Radix, Bucket."
            },
            {
                "type": "video",
                "title": "YouTube - Sorting Algorithms Overview",
                "url": "https://www.youtube.com/watch?v=kgBjXUE_Nwc"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Sorting Basics",
                "url": "https://college.edu/pyq/algo-sorting-intro-2023",
                "content": "Q1: What is sorting? Why is it important? Q2: Difference between stable and unstable sorting. Q3: Compare comparison-based and non-comparison-based sorting. Q4: What is in-place sorting? Give examples."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Sorting Basics",
                "url": "https://college.edu/practice/algo-sorting-intro",
                "content": "1. Identify stable/unstable sorts. 2. Compare time complexities. 3. Choose best sorting for given scenario."
            }
        ]
    },
    {
        "name": "Bubble Sort",
        "description": "Bubble sort algorithm, adjacent element swapping, optimized version with early termination, time complexity O(n²), space O(1), stable, in-place",
        "tags": ["bubble-sort", "comparison", "n2", "stable", "in-place"],
        "importance_score": 0.8,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Bubble Sort",
                "url": "https://college.edu/notes/algo-bubble-sort",
                "content": "Bubble Sort: repeatedly swap adjacent elements if in wrong order. After each pass, largest element bubbles to end. Optimized: use swapped flag to detect if array is already sorted. Time: Best O(n), Average O(n²), Worst O(n²). Space: O(1). Stable: Yes. In-place: Yes."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Bubble Sort",
                "url": "https://www.w3schools.com/dsa/dsa_algo_bubblesort.php",
                "content": "Bubble Sort is a simple sorting algorithm that repeatedly swaps adjacent elements if they are in the wrong order. After each pass, the largest unsorted element moves to its correct position. Optimized version uses swapped flag for early termination. Time: O(n²) average/worst, O(n) best. Space: O(1)."
            },
            {
                "type": "video",
                "title": "YouTube - Bubble Sort Algorithm",
                "url": "https://www.youtube.com/watch?v=nmhjrI-aW5o"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Bubble Sort",
                "url": "https://college.edu/pyq/algo-bubble-2023",
                "content": "Q1: Explain Bubble Sort with example. Q2: What is the time complexity of Bubble Sort? Q3: How to optimize Bubble Sort? Q4: Is Bubble Sort stable? Why?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Bubble Sort",
                "url": "https://college.edu/practice/algo-bubble",
                "content": "1. Implement Bubble Sort. 2. Implement optimized Bubble Sort with swapped flag. 3. Sort array in descending order. 4. Count number of swaps."
            }
        ]
    },
    {
        "name": "Selection Sort",
        "description": "Selection sort algorithm, finding minimum element, swapping with first unsorted position, time complexity O(n²), space O(1), unstable, in-place",
        "tags": ["selection-sort", "comparison", "n2", "unstable", "in-place"],
        "importance_score": 0.8,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Selection Sort",
                "url": "https://college.edu/notes/algo-selection-sort",
                "content": "Selection Sort: repeatedly find minimum from unsorted portion and swap with first unsorted element. Time: O(n²) all cases. Space: O(1). Unstable: relative order of equal elements may change. In-place: Yes. Minimum number of swaps: O(n)."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Selection Sort",
                "url": "https://www.w3schools.com/dsa/dsa_algo_selectionsort.php",
                "content": "Selection Sort repeatedly selects the smallest element from unsorted part and swaps it with first unsorted element. Process continues until array is sorted. Time: O(n²) all cases. Space: O(1). Unstable sort."
            },
            {
                "type": "video",
                "title": "YouTube - Selection Sort Algorithm",
                "url": "https://www.youtube.com/watch?v=GUDLRanO-Ps"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Selection Sort",
                "url": "https://college.edu/pyq/algo-selection-2023",
                "content": "Q1: Explain Selection Sort with example. Q2: Why is Selection Sort unstable? Q3: Time complexity of Selection Sort? Q4: Compare Bubble and Selection Sort."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Selection Sort",
                "url": "https://college.edu/practice/algo-selection",
                "content": "1. Implement Selection Sort. 2. Find minimum swaps needed. 3. Sort linked list using Selection Sort."
            }
        ]
    },
    {
        "name": "Insertion Sort",
        "description": "Insertion sort algorithm, inserting element into correct position in sorted portion, time complexity O(n²), space O(1), stable, in-place, best for small arrays",
        "tags": ["insertion-sort", "comparison", "n2", "stable", "in-place", "adaptive"],
        "importance_score": 0.85,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Insertion Sort",
                "url": "https://college.edu/notes/algo-insertion-sort",
                "content": "Insertion Sort: build sorted array one element at a time. Start with second element, insert into correct position in sorted portion. Like sorting playing cards. Time: Best O(n), Average O(n²), Worst O(n²). Space: O(1). Stable: Yes. In-place: Yes. Adaptive: faster for nearly sorted data. Best for small arrays."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Insertion Sort",
                "url": "https://www.w3schools.com/dsa/dsa_algo_insertionsort.php",
                "content": "Insertion Sort builds sorted array one element at a time. Works like sorting playing cards in hand. Start with second element, insert into correct position among already sorted cards. Time: O(n²) average/worst, O(n) best. Space: O(1). Stable sort."
            },
            {
                "type": "video",
                "title": "YouTube - Insertion Sort Algorithm",
                "url": "https://www.youtube.com/watch?v=JU767SDHBvE"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Insertion Sort",
                "url": "https://college.edu/pyq/algo-insertion-2023",
                "content": "Q1: Explain Insertion Sort with example. Q2: When is Insertion Sort best choice? Q3: Is Insertion Sort stable? Explain. Q4: Compare Insertion and Selection Sort."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Insertion Sort",
                "url": "https://college.edu/practice/algo-insertion",
                "content": "1. Implement Insertion Sort. 2. Sort linked list using Insertion Sort. 3. Binary Insertion Sort. 4. Count shifts in Insertion Sort."
            }
        ]
    },
    {
        "name": "Shell Sort",
        "description": "Shell sort algorithm, gap sequence, diminishing increment sort, time complexity depends on gap sequence, space O(1), unstable, in-place, generalization of insertion sort",
        "tags": ["shell-sort", "gap-sequence", "comparison", "in-place", "unstable"],
        "importance_score": 0.75,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Shell Sort",
                "url": "https://college.edu/notes/algo-shell-sort",
                "content": "Shell Sort: generalization of insertion sort using gap sequence. Start with large gap, perform insertion sort on elements separated by gap. Reduce gap, repeat. Final pass with gap=1 is regular insertion sort. Gap sequences: Shell (n/2), Knuth (3k+1), Hibbard (2k-1). Time: O(n^1.5) with Knuth sequence. Space: O(1). Unstable."
            },
            {
                "type": "external_notes",
                "title": "TutorialsPoint - Shell Sort",
                "url": "https://www.tutorialspoint.com/data_structures_algorithms/shell_sort_algorithm.htm",
                "content": "Shell Sort is a generalization of Insertion Sort. It allows exchange of far apart elements. Uses gap sequence to determine which elements to compare. Start with large gap, reduce until gap=1. Performance depends on gap sequence chosen. Time: O(n log n) to O(n²) depending on gap. Space: O(1)."
            },
            {
                "type": "video",
                "title": "YouTube - Shell Sort Algorithm",
                "url": "https://www.youtube.com/watch?v=ddeLSDsYVp8"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Shell Sort",
                "url": "https://college.edu/pyq/algo-shell-2023",
                "content": "Q1: What is Shell Sort? How does it differ from Insertion Sort? Q2: Explain gap sequence in Shell Sort. Q3: Time complexity of Shell Sort?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Shell Sort",
                "url": "https://college.edu/practice/algo-shell",
                "content": "1. Implement Shell Sort with Shell's gap sequence. 2. Implement with Knuth's gap sequence. 3. Compare different gap sequences."
            }
        ]
    },
    {
        "name": "Merge Sort",
        "description": "Merge sort algorithm, divide and conquer approach, merging sorted halves, time complexity O(n log n), space O(n), stable, external sorting",
        "tags": ["merge-sort", "divide-conquer", "nlogn", "stable", "external-sorting"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Merge Sort",
                "url": "https://college.edu/notes/algo-merge-sort",
                "content": "Merge Sort: divide array into halves, recursively sort each half, merge sorted halves. Divide: O(1), Conquer: 2T(n/2), Merge: O(n). Time: O(n log n) all cases. Space: O(n). Stable: Yes. External sorting: Yes (works with disk). Used in LinkedList sorting, external sorting, inversion counting."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Merge Sort",
                "url": "https://www.w3schools.com/dsa/dsa_algo_mergesort.php",
                "content": "Merge Sort divides array into two halves, recursively sorts them, then merges sorted halves. Divide step is simple, merge step is critical. Time: O(n log n) all cases. Space: O(n). Stable sort. Works well for linked lists and external sorting."
            },
            {
                "type": "video",
                "title": "YouTube - Merge Sort Algorithm",
                "url": "https://www.youtube.com/watch?v=JSceec-wEyw"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Merge Sort",
                "url": "https://college.edu/pyq/algo-merge-2023",
                "content": "Q1: Explain Merge Sort with example. Q2: Derive time complexity of Merge Sort. Q3: Why is Merge Sort preferred for linked lists? Q4: Is Merge Sort stable? Explain."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Merge Sort",
                "url": "https://college.edu/practice/algo-merge",
                "content": "1. Implement Merge Sort. 2. Count inversions using Merge Sort. 3. Merge Sort for linked list. 4. External merge sort."
            }
        ]
    },
    {
        "name": "Quicksort",
        "description": "Quicksort algorithm, pivot selection, partitioning, time complexity O(n log n) average, O(n²) worst, space O(log n), unstable, in-place",
        "tags": ["quicksort", "divide-conquer", "pivot", "partition", "nlogn", "unstable"],
        "importance_score": 0.95,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Quicksort",
                "url": "https://college.edu/notes/algo-quicksort",
                "content": "Quicksort: pick pivot, partition array around pivot (elements < pivot left, > pivot right), recursively sort partitions. Pivot selection: first, last, median-of-three, random. Partition: Lomuto, Hoare. Time: Best/Average O(n log n), Worst O(n²) (sorted input). Space: O(log n). Unstable. In practice fastest comparison sort."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Quicksort",
                "url": "https://www.w3schools.com/dsa/dsa_algo_quicksort.php",
                "content": "Quicksort picks a pivot element and rearranges array so elements smaller than pivot move left, greater move right. Recursively sorts subarrays. Time: O(n log n) average, O(n²) worst. Space: O(log n). Unstable sort. Fastest in practice for average case."
            },
            {
                "type": "video",
                "title": "YouTube - Quicksort Algorithm",
                "url": "https://www.youtube.com/watch?v=COk73cpxbMs"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Quicksort",
                "url": "https://college.edu/pyq/algo-quick-2023",
                "content": "Q1: Explain Quicksort with example. Q2: What is pivot selection? Different methods? Q3: When does Quicksort give worst case? Q4: Compare Merge Sort and Quicksort."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Quicksort",
                "url": "https://college.edu/practice/algo-quick",
                "content": "1. Implement Quicksort. 2. Implement 3-way Quicksort. 3. Quick Select algorithm. 4. Randomized Quicksort."
            }
        ]
    },
    {
        "name": "Heapsort",
        "description": "Heapsort algorithm, heap data structure, build heap, extract max, time complexity O(n log n), space O(1), unstable, in-place",
        "tags": ["heapsort", "heap", "nlogn", "unstable", "in-place", "selection-sort"],
        "importance_score": 0.9,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Heapsort",
                "url": "https://college.edu/notes/algo-heapsort",
                "content": "Heapsort: build max heap from array, repeatedly extract maximum and place at end. Build heap: O(n). Extract max: O(log n) each, n times = O(n log n). Total: O(n log n). Space: O(1). Unstable. In-place. Guaranteed O(n log n) unlike Quicksort."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Heap Sort",
                "url": "https://www.geeksforgeeks.org/dsa/heap-sort/",
                "content": "Heap Sort uses binary heap data structure. Build max heap, then repeatedly extract maximum. Time: O(n log n) all cases. Space: O(1). Unstable. In-place. Advantages: guaranteed O(n log n), constant space. Disadvantages: not stable, not adaptive."
            },
            {
                "type": "video",
                "title": "YouTube - Heapsort Algorithm",
                "url": "https://www.youtube.com/watch?v=2DmK_H7IdTo"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Heapsort",
                "url": "https://college.edu/pyq/algo-heap-2023",
                "content": "Q1: Explain Heapsort with example. Q2: Build heap time complexity? Q3: Compare Heapsort and Quicksort. Q4: Why is Heapsort not stable?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Heapsort",
                "url": "https://college.edu/practice/algo-heap",
                "content": "1. Implement Heapsort. 2. Build max heap. 3. Find kth largest using heap. 4. Heapify algorithm."
            }
        ]
    },
    {
        "name": "Time Complexity Analysis of Sorting Algorithms",
        "description": "Best, average, worst case analysis for Bubble, Selection, Insertion, Merge, Quick, Heap sort. Comparison table. When to use which sort.",
        "tags": ["time-complexity", "analysis", "comparison", "sorting-comparison"],
        "importance_score": 0.9,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Sorting Complexity",
                "url": "https://college.edu/notes/algo-sort-complexity",
                "content": "Comparison: Bubble O(n²), Selection O(n²), Insertion O(n²), Merge O(n log n), Quick O(n log n avg), Heap O(n log n). Best for small: Insertion. Best for linked list: Merge. Best average: Quick. Guaranteed: Merge/Heap. Stable: Bubble, Insertion, Merge. In-place: Bubble, Selection, Insertion, Quick, Heap."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Sorting Complexity Theory",
                "url": "https://www.w3schools.com/dsa/dsa_timecomplexity_theory.php",
                "content": "Sorting algorithms can be compared by time complexity, space usage, stability, and adaptivity. O(n²) algorithms: Bubble, Selection, Insertion. O(n log n): Merge, Quick, Heap. Linear: Counting, Radix, Bucket. No comparison-based sort can be faster than O(n log n)."
            },
            {
                "type": "video",
                "title": "YouTube - Sorting Algorithms Comparison",
                "url": "https://www.youtube.com/watch?v=ZZuD6iUe3Pc"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Sorting Comparison",
                "url": "https://college.edu/pyq/algo-sort-compare-2023",
                "content": "Q1: Compare all sorting algorithms with time complexities. Q2: When to use Merge Sort vs Quick Sort? Q3: Why is O(n log n) lower bound for comparison sorts? Q4: Which sort is best for nearly sorted data?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Sorting Comparison",
                "url": "https://college.edu/practice/algo-sort-compare",
                "content": "1. Benchmark different sorting algorithms. 2. Choose best sort for given scenario. 3. Analyze sorting stability."
            }
        ]
    },
    {
        "name": "Counting Sort",
        "description": "Counting sort algorithm, non-comparison based, counting frequencies, prefix sum, time O(n+k), space O(k), stable, used when range is small",
        "tags": ["counting-sort", "non-comparison", "linear", "stable", "integer-sort"],
        "importance_score": 0.85,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Counting Sort",
                "url": "https://college.edu/notes/algo-counting-sort",
                "content": "Counting Sort: non-comparison based. Count frequency of each element, use prefix sum to determine positions. Time: O(n+k) where k is range. Space: O(k). Stable: Yes. Works for integers. Not suitable when k >> n. Used as subroutine in Radix Sort."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Counting Sort",
                "url": "https://www.w3schools.com/dsa/dsa_algo_countingsort.php",
                "content": "Counting Sort is non-comparison-based that works when range of input values is small relative to number of elements. Counts frequency of each element, uses prefix sum to place elements in correct positions. Time: O(n+k). Space: O(k). Stable sort."
            },
            {
                "type": "video",
                "title": "YouTube - Counting Sort Algorithm",
                "url": "https://www.youtube.com/watch?v=7zuGmKfUt7s"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Counting Sort",
                "url": "https://college.edu/pyq/algo-counting-2023",
                "content": "Q1: Explain Counting Sort with example. Q2: When to use Counting Sort? Q3: Is Counting Sort comparison-based? Q4: Time and space complexity of Counting Sort?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Counting Sort",
                "url": "https://college.edu/practice/algo-counting",
                "content": "1. Implement Counting Sort. 2. Sort negative numbers. 3. Counting Sort for strings."
            }
        ]
    },
    {
        "name": "Bucket Sort",
        "description": "Bucket sort algorithm, distributing elements into buckets, sorting each bucket, time O(n+k) average, space O(n+k), stable if bucket sort is stable",
        "tags": ["bucket-sort", "non-comparison", "linear", "distribution"],
        "importance_score": 0.8,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Bucket Sort",
                "url": "https://college.edu/notes/algo-bucket-sort",
                "content": "Bucket Sort: distribute elements into buckets based on range, sort each bucket (using insertion sort or recursively), concatenate buckets. Time: O(n+k) average, O(n²) worst. Space: O(n+k). Works for uniformly distributed data. Used for floating point numbers in range [0,1)."
            },
            {
                "type": "external_notes",
                "title": "GeeksforGeeks - Bucket Sort",
                "url": "https://www.geeksforgeeks.org/dsa/bucket-sort-2/",
                "content": "Bucket Sort distributes elements into buckets, sorts each bucket individually, then concatenates. Works best for uniformly distributed data. Time: O(n+k) average, O(n²) worst. Space: O(n+k). Often used for floating point numbers."
            },
            {
                "type": "video",
                "title": "YouTube - Bucket Sort Algorithm",
                "url": "https://www.youtube.com/watch?v=VuXbEb5ywrU"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Bucket Sort",
                "url": "https://college.edu/pyq/algo-bucket-2023",
                "content": "Q1: Explain Bucket Sort with example. Q2: When is Bucket Sort most efficient? Q3: Time complexity of Bucket Sort?"
            },
            {
                "type": "coding_problems",
                "title": "Practice - Bucket Sort",
                "url": "https://college.edu/practice/algo-bucket",
                "content": "1. Implement Bucket Sort. 2. Sort floating point numbers. 3. Bucket Sort for integers."
            }
        ]
    },
    {
        "name": "Radix Sort",
        "description": "Radix sort algorithm, digit by digit sorting, using counting sort as subroutine, time O(d*(n+k)), space O(n+k), stable",
        "tags": ["radix-sort", "non-comparison", "digit-by-digit", "stable", "linear"],
        "importance_score": 0.85,
        "resources": [
            {
                "type": "college_notes",
                "title": "Lecture Notes - Radix Sort",
                "url": "https://college.edu/notes/algo-radix-sort",
                "content": "Radix Sort: sort elements digit by digit from least significant to most significant. Uses stable sort (counting sort) as subroutine. Time: O(d*(n+k)) where d is number of digits, k is base. Space: O(n+k). Stable. Works for integers and strings. LSD (least significant digit first) or MSD (most significant digit first)."
            },
            {
                "type": "external_notes",
                "title": "W3Schools - Radix Sort",
                "url": "https://www.w3schools.com/dsa/dsa_algo_radixsort.php",
                "content": "Radix Sort sorts elements digit by digit, starting from least significant digit. Uses a stable sort as subroutine for each digit. Time: O(d*(n+k)). Space: O(n+k). Stable sort. Works for integers and strings."
            },
            {
                "type": "video",
                "title": "YouTube - Radix Sort Algorithm",
                "url": "https://www.youtube.com/watch?v=XiuSW_mEn7g"
            },
            {
                "type": "pyq",
                "title": "PYQ 2023 - Radix Sort",
                "url": "https://college.edu/pyq/algo-radix-2023",
                "content": "Q1: Explain Radix Sort with example. Q2: Why does Radix Sort use stable sort as subroutine? Q3: Time complexity of Radix Sort? Q4: Compare Radix Sort and Counting Sort."
            },
            {
                "type": "coding_problems",
                "title": "Practice - Radix Sort",
                "url": "https://college.edu/practice/algo-radix",
                "content": "1. Implement Radix Sort. 2. LSD Radix Sort. 3. MSD Radix Sort. 4. Radix Sort for strings."
            }
        ]
    }
]


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Get Algorithms subject
        algo_subject = db.query(Subject).filter(Subject.code == "CST209").first()
        if not algo_subject:
            print("Algorithms subject not found. Run seed_algorithms_unit1.py first.")
            return

        # Get or create Unit 2
        unit2 = db.query(Unit).filter(
            Unit.subject_id == algo_subject.id,
            Unit.number == 2
        ).first()

        if not unit2:
            unit2 = Unit(
                name="Sorting",
                number=2,
                subject_id=algo_subject.id,
                description="Sorting algorithms including Bubble, Selection, Insertion, Shell, Merge, Quick, Heap, Counting, Bucket, Radix sort with complexity analysis"
            )
            db.add(unit2)
            db.flush()

        # Clear existing topics for this unit
        existing_topics = db.query(Topic).filter(Topic.unit_id == unit2.id).all()
        for t in existing_topics:
            db.delete(t)
        db.flush()

        # Create topics
        for topic_data in ALGORITHMS_UNIT2_TOPICS:
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
                    metadata_={"source": "geeksforgeeks+w3schools+syllabus", "difficulty": "medium"}
                )
                db.add(resource)

        db.commit()
        print("Algorithms Unit 2 detailed dataset seeded successfully!")
        print(f"Created {len(ALGORITHMS_UNIT2_TOPICS)} topics with detailed resources")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

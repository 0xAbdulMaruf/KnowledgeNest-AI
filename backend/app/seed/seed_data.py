import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal, engine, Base
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.topic import Topic
from app.models.resource import Resource, ResourceType


SEED = [
    {
        "semester": 1,
        "name": "Semester 1",
        "subjects": [
            {
                "name": "Engineering Mathematics I",
                "code": "MATH101",
                "description": "Calculus, linear algebra, and differential equations",
                "tags": ["mathematics", "calculus", "algebra"],
                "units": [
                    {
                        "name": "Differential Calculus",
                        "number": 1,
                        "topics": [
                            {"name": "Limits and Continuity", "description": "Concept of limits, continuity of functions, types of discontinuities", "tags": ["limits", "continuity"], "importance_score": 0.8},
                            {"name": "Differentiation", "description": "Derivatives, chain rule, implicit differentiation, higher order derivatives", "tags": ["derivatives", "chain-rule"], "importance_score": 0.9},
                            {"name": "Applications of Derivatives", "description": "Maxima, minima, curve sketching, mean value theorems", "tags": ["maxima", "minima", "mvt"], "importance_score": 0.7},
                        ],
                    },
                    {
                        "name": "Integral Calculus",
                        "number": 2,
                        "topics": [
                            {"name": "Integration Techniques", "description": "Substitution, integration by parts, partial fractions, trigonometric integrals", "tags": ["integration", "substitution"], "importance_score": 0.9},
                            {"name": "Definite Integrals", "description": "Riemann sums, fundamental theorem of calculus, area under curves", "tags": ["definite-integral", "ftc"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Linear Algebra",
                        "number": 3,
                        "topics": [
                            {"name": "Matrices and Determinants", "description": "Matrix operations, determinants, inverse, rank of a matrix", "tags": ["matrices", "determinants"], "importance_score": 0.8},
                            {"name": "Eigenvalues and Eigenvectors", "description": "Characteristic equation, diagonalization, Cayley-Hamilton theorem", "tags": ["eigenvalues", "eigenvectors"], "importance_score": 0.9},
                        ],
                    },
                ],
            },
            {
                "name": "Programming in C",
                "code": "CS101",
                "description": "Fundamentals of C programming language",
                "tags": ["programming", "c-language", "basics"],
                "units": [
                    {
                        "name": "Introduction to Programming",
                        "number": 1,
                        "topics": [
                            {"name": "Variables and Data Types", "description": "int, float, char, double, type casting, sizeof operator", "tags": ["variables", "data-types", "c"], "importance_score": 0.9},
                            {"name": "Control Structures", "description": "if-else, switch, for, while, do-while loops, break and continue", "tags": ["control-flow", "loops", "c"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Functions and Arrays",
                        "number": 2,
                        "topics": [
                            {"name": "Functions", "description": "Function declaration, definition, calling, recursion, scope rules", "tags": ["functions", "recursion", "c"], "importance_score": 0.85},
                            {"name": "Arrays", "description": "1D and 2D arrays, array manipulation, searching and sorting", "tags": ["arrays", "sorting", "c"], "importance_score": 0.85},
                            {"name": "Strings", "description": "String handling functions, string manipulation, arrays of strings", "tags": ["strings", "c"], "importance_score": 0.7},
                        ],
                    },
                    {
                        "name": "Pointers and Structures",
                        "number": 3,
                        "topics": [
                            {"name": "Pointers", "description": "Pointer arithmetic, pointer to pointer, function pointers, dynamic memory allocation", "tags": ["pointers", "memory", "c"], "importance_score": 0.95},
                            {"name": "Structures and Unions", "description": "struct, union, typedef, enum, file handling basics", "tags": ["structures", "unions", "c"], "importance_score": 0.75},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "semester": 2,
        "name": "Semester 2",
        "subjects": [
            {
                "name": "Engineering Mathematics II",
                "code": "MATH201",
                "description": "Probability, statistics, complex analysis, and transforms",
                "tags": ["mathematics", "probability", "transforms"],
                "units": [
                    {
                        "name": "Probability and Statistics",
                        "number": 1,
                        "topics": [
                            {"name": "Probability Theory", "description": "Axioms of probability, conditional probability, Bayes theorem, random variables", "tags": ["probability", "bayes"], "importance_score": 0.9},
                            {"name": "Probability Distributions", "description": "Binomial, Poisson, normal distributions, central limit theorem", "tags": ["distributions", "normal", "clt"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Complex Analysis",
                        "number": 2,
                        "topics": [
                            {"name": "Complex Functions", "description": "Analytic functions, Cauchy-Riemann equations, harmonic functions", "tags": ["complex", "analytic"], "importance_score": 0.7},
                            {"name": "Contour Integration", "description": "Cauchy integral theorem, residue theorem, evaluation of real integrals", "tags": ["contour", "residue"], "importance_score": 0.75},
                        ],
                    },
                    {
                        "name": "Transforms",
                        "number": 3,
                        "topics": [
                            {"name": "Laplace Transform", "description": "Laplace transforms, inverse transforms, applications to differential equations", "tags": ["laplace", "transforms"], "importance_score": 0.8},
                            {"name": "Z-Transform", "description": "Z-transform, inverse Z-transform, applications to difference equations", "tags": ["z-transform", "signals"], "importance_score": 0.7},
                        ],
                    },
                ],
            },
            {
                "name": "Data Structures",
                "code": "CS201",
                "description": "Fundamental data structures and algorithms",
                "tags": ["data-structures", "algorithms", "dsa"],
                "units": [
                    {
                        "name": "Arrays and Linked Lists",
                        "number": 1,
                        "topics": [
                            {"name": "Arrays and Dynamic Arrays", "description": "Static and dynamic arrays, amortized analysis, array-based data structures", "tags": ["arrays", "dynamic-arrays"], "importance_score": 0.9},
                            {"name": "Linked Lists", "description": "Singly, doubly, and circular linked lists, operations and applications", "tags": ["linked-lists", "pointers"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Stacks and Queues",
                        "number": 2,
                        "topics": [
                            {"name": "Stacks", "description": "Stack implementation, applications in expression evaluation, recursion", "tags": ["stack", "recursion"], "importance_score": 0.85},
                            {"name": "Queues", "description": "Queue, circular queue, deque, priority queue, applications", "tags": ["queue", "priority-queue"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Trees",
                        "number": 3,
                        "topics": [
                            {"name": "Binary Trees", "description": "Binary tree traversals, construction, properties, BST operations", "tags": ["binary-tree", "bst", "traversal"], "importance_score": 0.95},
                            {"name": "AVL Trees", "description": "AVL tree rotations, insertion, deletion, balancing", "tags": ["avl", "balanced-tree"], "importance_score": 0.8},
                            {"name": "Heap and Priority Queue", "description": "Min-heap, max-heap, heap operations, heap sort", "tags": ["heap", "heap-sort"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Graphs",
                        "number": 4,
                        "topics": [
                            {"name": "Graph Representations", "description": "Adjacency matrix, adjacency list, graph traversals (BFS, DFS)", "tags": ["graph", "bfs", "dfs"], "importance_score": 0.9},
                            {"name": "Shortest Path Algorithms", "description": "Dijkstra, Bellman-Ford, Floyd-Warshall algorithms", "tags": ["dijkstra", "shortest-path"], "importance_score": 0.9},
                            {"name": "Minimum Spanning Trees", "description": "Kruskal and Prim algorithms, applications of MST", "tags": ["mst", "kruskal", "prim"], "importance_score": 0.8},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "semester": 3,
        "name": "Semester 3",
        "subjects": [
            {
                "name": "Object Oriented Programming",
                "code": "CS301",
                "description": "OOP concepts using Java/C++",
                "tags": ["oop", "java", "design"],
                "units": [
                    {
                        "name": "OOP Fundamentals",
                        "number": 1,
                        "topics": [
                            {"name": "Classes and Objects", "description": "Class definition, constructors, destructors, access specifiers, this pointer", "tags": ["classes", "objects", "constructors"], "importance_score": 0.9},
                            {"name": "Inheritance", "description": "Single, multiple, multilevel inheritance, virtual inheritance", "tags": ["inheritance", "polymorphism"], "importance_score": 0.95},
                        ],
                    },
                    {
                        "name": "Advanced OOP",
                        "number": 2,
                        "topics": [
                            {"name": "Polymorphism", "description": "Function overloading, operator overloading, virtual functions, abstract classes", "tags": ["polymorphism", "virtual", "overloading"], "importance_score": 0.95},
                            {"name": "Templates and Generics", "description": "Function templates, class templates, generic programming", "tags": ["templates", "generics"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Design Principles",
                        "number": 3,
                        "topics": [
                            {"name": "SOLID Principles", "description": "Single responsibility, open-closed, Liskov substitution, interface segregation, dependency inversion", "tags": ["solid", "design-principles"], "importance_score": 0.85},
                            {"name": "Design Patterns", "description": "Singleton, Factory, Observer, Strategy patterns", "tags": ["design-patterns", "gang-of-four"], "importance_score": 0.8},
                        ],
                    },
                ],
            },
            {
                "name": "Database Management Systems",
                "code": "CS302",
                "description": "Relational databases, SQL, normalization, and transaction processing",
                "tags": ["database", "sql", "rdbms"],
                "units": [
                    {
                        "name": "Introduction to DBMS",
                        "number": 1,
                        "topics": [
                            {"name": "Database Concepts", "description": "DBMS architecture, data models, ER model, relational model", "tags": ["dbms", "er-model", "relational"], "importance_score": 0.9},
                            {"name": "ER Diagrams", "description": "Entity-Relationship model, strong/weak entities, relationships, cardinality", "tags": ["er-diagram", "modeling"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "SQL",
                        "number": 2,
                        "topics": [
                            {"name": "SQL Fundamentals", "description": "DDL, DML, DCL commands, joins, subqueries, views", "tags": ["sql", "queries", "joins"], "importance_score": 0.95},
                            {"name": "Advanced SQL", "description": "Window functions, CTEs, stored procedures, triggers, cursors", "tags": ["advanced-sql", "procedures", "triggers"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Normalization",
                        "number": 3,
                        "topics": [
                            {"name": "Functional Dependencies", "description": "Types of functional dependencies, closure, minimal cover", "tags": ["functional-dependencies", "normalization"], "importance_score": 0.85},
                            {"name": "Normal Forms", "description": "1NF, 2NF, 3NF, BCNF, decomposition algorithms", "tags": ["1nf", "2nf", "3nf", "bcnf"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Transactions and Recovery",
                        "number": 4,
                        "topics": [
                            {"name": "Transaction Processing", "description": "ACID properties, concurrency control, locking, 2PL, timestamp ordering", "tags": ["transactions", "acid", "concurrency"], "importance_score": 0.85},
                            {"name": "Recovery Systems", "description": "Log-based recovery, checkpoints, ARIES algorithm", "tags": ["recovery", "logging", "aries"], "importance_score": 0.75},
                        ],
                    },
                ],
            },
            {
                "name": "Operating Systems",
                "code": "CS303",
                "description": "Process management, memory management, file systems, and I/O",
                "tags": ["os", "systems", "kernel"],
                "units": [
                    {
                        "name": "Process Management",
                        "number": 1,
                        "topics": [
                            {"name": "Processes and Threads", "description": "Process states, PCB, context switching, threads, multithreading models", "tags": ["processes", "threads", "pcb"], "importance_score": 0.95},
                            {"name": "CPU Scheduling", "description": "FCFS, SJF, Round Robin, Priority, Multilevel queue scheduling algorithms", "tags": ["scheduling", "fcfs", "rr"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Process Synchronization",
                        "number": 2,
                        "topics": [
                            {"name": "Synchronization Tools", "description": "Mutex, semaphore, monitors, critical section problem", "tags": ["mutex", "semaphore", "critical-section"], "importance_score": 0.95},
                            {"name": "Deadlocks", "description": "Conditions for deadlock, prevention, avoidance (Banker's algorithm), detection", "tags": ["deadlock", "banker"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Memory Management",
                        "number": 3,
                        "topics": [
                            {"name": "Virtual Memory", "description": "Paging, segmentation, page replacement algorithms, thrashing", "tags": ["virtual-memory", "paging", "page-replacement"], "importance_score": 0.95},
                            {"name": "Memory Allocation", "description": "Contiguous allocation, fragmentation, buddy system, slab allocation", "tags": ["memory-allocation", "fragmentation"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "File Systems",
                        "number": 4,
                        "topics": [
                            {"name": "File System Implementation", "description": "Directory structure, allocation methods, free space management", "tags": ["filesystem", "directory", "allocation"], "importance_score": 0.8},
                            {"name": "Disk Scheduling", "description": "FCFS, SCAN, C-SCAN, LOOK disk scheduling algorithms", "tags": ["disk-scheduling", "scan", "look"], "importance_score": 0.7},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "semester": 4,
        "name": "Semester 4",
        "subjects": [
            {
                "name": "Computer Networks",
                "code": "CS401",
                "description": "Network protocols, architecture, and security",
                "tags": ["networking", "tcp-ip", "protocols"],
                "units": [
                    {
                        "name": "Network Models",
                        "number": 1,
                        "topics": [
                            {"name": "OSI and TCP/IP Models", "description": "Seven layer OSI model, TCP/IP model, encapsulation, protocol data units", "tags": ["osi", "tcp-ip", "layers"], "importance_score": 0.9},
                            {"name": "Physical Layer", "description": "Transmission media, encoding techniques, multiplexing, switching", "tags": ["physical-layer", "encoding", "multiplexing"], "importance_score": 0.7},
                        ],
                    },
                    {
                        "name": "Data Link and Network Layer",
                        "number": 2,
                        "topics": [
                            {"name": "Data Link Layer", "description": "Framing, error detection (CRC), flow control, HDLC, Ethernet", "tags": ["data-link", "crc", "ethernet"], "importance_score": 0.8},
                            {"name": "IP Addressing", "description": "IPv4, subnetting, CIDR, NAT, IPv6 fundamentals", "tags": ["ip", "subnetting", "cidr", "ipv6"], "importance_score": 0.95},
                            {"name": "Routing Algorithms", "description": "Distance vector, link state, OSPF, BGP, RIP", "tags": ["routing", "ospf", "bgp"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Transport and Application Layer",
                        "number": 3,
                        "topics": [
                            {"name": "TCP and UDP", "description": "TCP three-way handshake, flow control, congestion control, UDP characteristics", "tags": ["tcp", "udp", "congestion"], "importance_score": 0.95},
                            {"name": "Application Layer Protocols", "description": "HTTP, HTTPS, DNS, DHCP, SMTP, FTP, WebSocket", "tags": ["http", "dns", "dhcp", "smtp"], "importance_score": 0.9},
                        ],
                    },
                ],
            },
            {
                "name": "Design and Analysis of Algorithms",
                "code": "CS402",
                "description": "Algorithm design paradigms and complexity analysis",
                "tags": ["algorithms", "complexity", "optimization"],
                "units": [
                    {
                        "name": "Complexity Analysis",
                        "number": 1,
                        "topics": [
                            {"name": "Asymptotic Notations", "description": "Big-O, Omega, Theta notations, amortized analysis, recurrences", "tags": ["big-o", "complexity", "recurrence"], "importance_score": 0.95},
                            {"name": "Recurrence Relations", "description": "Master theorem, substitution method, recursion tree method", "tags": ["master-theorem", "recursion-tree"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Divide and Conquer",
                        "number": 2,
                        "topics": [
                            {"name": "Sorting Algorithms", "description": "Merge sort, quick sort, heap sort, lower bound for sorting", "tags": ["merge-sort", "quick-sort", "sorting"], "importance_score": 0.9},
                            {"name": "Binary Search Variants", "description": "Binary search on answer, search in rotated array, peak finding", "tags": ["binary-search", "search"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Dynamic Programming",
                        "number": 3,
                        "topics": [
                            {"name": "DP Fundamentals", "description": "Overlapping subproblems, optimal substructure, memoization vs tabulation", "tags": ["dp", "memoization", "tabulation"], "importance_score": 0.95},
                            {"name": "Classic DP Problems", "description": "LCS, LIS, knapsack, matrix chain multiplication, edit distance", "tags": ["lcs", "lis", "knapsack", "mcm"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Greedy and Backtracking",
                        "number": 4,
                        "topics": [
                            {"name": "Greedy Algorithms", "description": "Activity selection, Huffman coding, fractional knapsack, job sequencing", "tags": ["greedy", "huffman", "activity-selection"], "importance_score": 0.85},
                            {"name": "Backtracking", "description": "N-Queens, subset sum, graph coloring, Hamiltonian path", "tags": ["backtracking", "n-queens", "subset-sum"], "importance_score": 0.8},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "semester": 5,
        "name": "Semester 5",
        "subjects": [
            {
                "name": "Theory of Computation",
                "code": "CS501",
                "description": "Automata theory, formal languages, and computability",
                "tags": ["toc", "automata", "formal-languages"],
                "units": [
                    {
                        "name": "Finite Automata",
                        "number": 1,
                        "topics": [
                            {"name": "DFA and NFA", "description": "Deterministic and nondeterministic finite automata, equivalence, minimization", "tags": ["dfa", "nfa", "finite-automata"], "importance_score": 0.9},
                            {"name": "Regular Expressions", "description": "Regular expressions, pumping lemma, closure properties of regular languages", "tags": ["regex", "pumping-lemma"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Context-Free Languages",
                        "number": 2,
                        "topics": [
                            {"name": "Context-Free Grammars", "description": "CFG, parse trees, ambiguity, Chomsky normal form, CYK algorithm", "tags": ["cfg", "parsing", "cnf"], "importance_score": 0.9},
                            {"name": "Pushdown Automata", "description": "PDA, equivalence with CFG, deterministic PDA", "tags": ["pda", "pushdown"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Turing Machines",
                        "number": 3,
                        "topics": [
                            {"name": "Turing Machine Basics", "description": "Turing machine model, variants, Church-Turing thesis", "tags": ["turing-machine", "church-turing"], "importance_score": 0.85},
                            {"name": "Undecidability", "description": "Halting problem, reductions, Rice theorem", "tags": ["undecidability", "halting-problem", "rice"], "importance_score": 0.9},
                        ],
                    },
                ],
            },
            {
                "name": "Machine Learning",
                "code": "CS502",
                "description": "Supervised, unsupervised, and reinforcement learning",
                "tags": ["ml", "ai", "data-science"],
                "units": [
                    {
                        "name": "Supervised Learning",
                        "number": 1,
                        "topics": [
                            {"name": "Linear Regression", "description": "Simple and multiple linear regression, gradient descent, regularization", "tags": ["regression", "gradient-descent"], "importance_score": 0.9},
                            {"name": "Classification Algorithms", "description": "Logistic regression, SVM, decision trees, random forests", "tags": ["classification", "svm", "decision-tree"], "importance_score": 0.95},
                        ],
                    },
                    {
                        "name": "Unsupervised Learning",
                        "number": 2,
                        "topics": [
                            {"name": "Clustering", "description": "K-means, hierarchical clustering, DBSCAN, evaluation metrics", "tags": ["clustering", "kmeans", "dbscan"], "importance_score": 0.85},
                            {"name": "Dimensionality Reduction", "description": "PCA, t-SNE, autoencoders, feature selection", "tags": ["pca", "dimensionality-reduction", "feature-selection"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Neural Networks",
                        "number": 3,
                        "topics": [
                            {"name": "Perceptrons and MLP", "description": "Single layer perceptron, multilayer perceptron, backpropagation algorithm", "tags": ["neural-network", "perceptron", "backpropagation"], "importance_score": 0.9},
                            {"name": "Deep Learning Basics", "description": "CNNs, RNNs, activation functions, dropout, batch normalization", "tags": ["deep-learning", "cnn", "rnn"], "importance_score": 0.85},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "semester": 6,
        "name": "Semester 6",
        "subjects": [
            {
                "name": "Compiler Design",
                "code": "CS601",
                "description": "Lexical analysis, parsing, code generation, and optimization",
                "tags": ["compiler", "parsing", "code-generation"],
                "units": [
                    {
                        "name": "Lexical Analysis",
                        "number": 1,
                        "topics": [
                            {"name": "Lexical Analyzer", "description": "Tokens, patterns, lexemes, regular expressions for tokens, DFA construction", "tags": ["lexer", "tokens", "scanner"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Syntax Analysis",
                        "number": 2,
                        "topics": [
                            {"name": "Top-Down Parsing", "description": "LL(1) parsers, predictive parsing, FIRST and FOLLOW sets", "tags": ["ll-parsing", "first-follow"], "importance_score": 0.85},
                            {"name": "Bottom-Up Parsing", "description": "LR(0), SLR, CLR, LALR parsers, parsing table construction", "tags": ["lr-parsing", "slr", "lalr"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Code Generation",
                        "number": 3,
                        "topics": [
                            {"name": "Intermediate Code Generation", "description": "Three-address code, quadruples, triples, syntax-directed translation", "tags": ["intermediate-code", "three-address"], "importance_score": 0.8},
                            {"name": "Code Optimization", "description": "Local and global optimization, loop optimization, data flow analysis", "tags": ["optimization", "data-flow"], "importance_score": 0.75},
                        ],
                    },
                ],
            },
            {
                "name": "Web Development",
                "code": "CS602",
                "description": "Full stack web development with modern frameworks",
                "tags": ["web", "frontend", "backend", "fullstack"],
                "units": [
                    {
                        "name": "Frontend Fundamentals",
                        "number": 1,
                        "topics": [
                            {"name": "HTML and CSS", "description": "Semantic HTML5, CSS3, Flexbox, Grid, responsive design principles", "tags": ["html", "css", "responsive"], "importance_score": 0.8},
                            {"name": "JavaScript Essentials", "description": "ES6+, DOM manipulation, event handling, async/await, fetch API", "tags": ["javascript", "dom", "async"], "importance_score": 0.95},
                            {"name": "React Fundamentals", "description": "Components, JSX, props, state, hooks, virtual DOM", "tags": ["react", "components", "hooks"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Backend Development",
                        "number": 2,
                        "topics": [
                            {"name": "Node.js and Express", "description": "Node.js runtime, Express middleware, routing, REST API design", "tags": ["nodejs", "express", "rest-api"], "importance_score": 0.9},
                            {"name": "Authentication and Authorization", "description": "JWT, OAuth 2.0, session management, RBAC", "tags": ["auth", "jwt", "oauth"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Database and Deployment",
                        "number": 3,
                        "topics": [
                            {"name": "NoSQL Databases", "description": "MongoDB, Redis, document databases vs relational databases", "tags": ["mongodb", "redis", "nosql"], "importance_score": 0.8},
                            {"name": "Deployment and DevOps", "description": "Docker, CI/CD pipelines, cloud deployment, monitoring", "tags": ["docker", "cicd", "deployment"], "importance_score": 0.75},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "semester": 7,
        "name": "Semester 7",
        "subjects": [
            {
                "name": "Artificial Intelligence",
                "code": "CS701",
                "description": "Search algorithms, knowledge representation, and AI techniques",
                "tags": ["ai", "search", "knowledge-representation"],
                "units": [
                    {
                        "name": "Search Algorithms",
                        "number": 1,
                        "topics": [
                            {"name": "Uninformed Search", "description": "BFS, DFS, iterative deepening, uniform cost search", "tags": ["bfs", "dfs", "search"], "importance_score": 0.85},
                            {"name": "Informed Search", "description": "A* search, heuristic functions, greedy best-first search", "tags": ["a-star", "heuristic", "informed-search"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Knowledge Representation",
                        "number": 2,
                        "topics": [
                            {"name": "Logic and Reasoning", "description": "Propositional logic, predicate logic, resolution, inference", "tags": ["logic", "inference", "resolution"], "importance_score": 0.85},
                            {"name": "Bayesian Networks", "description": "Probabilistic reasoning, Bayesian inference, conditional independence", "tags": ["bayesian", "probabilistic-reasoning"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Advanced AI",
                        "number": 3,
                        "topics": [
                            {"name": "Game Playing", "description": "Minimax algorithm, alpha-beta pruning, evaluation functions", "tags": ["minimax", "alpha-beta", "game-tree"], "importance_score": 0.75},
                            {"name": "Natural Language Processing", "description": "Tokenization, parsing, sentiment analysis, word embeddings", "tags": ["nlp", "tokenization", "embeddings"], "importance_score": 0.8},
                        ],
                    },
                ],
            },
            {
                "name": "Software Engineering",
                "code": "CS702",
                "description": "Software development methodologies, testing, and project management",
                "tags": ["sdlc", "testing", "agile"],
                "units": [
                    {
                        "name": "SDLC Models",
                        "number": 1,
                        "topics": [
                            {"name": "Agile Methodology", "description": "Scrum, Kanban, sprint planning, user stories, retrospectives", "tags": ["agile", "scrum", "kanban"], "importance_score": 0.9},
                            {"name": "Requirements Engineering", "description": "SRS document, use case diagrams, requirements elicitation techniques", "tags": ["requirements", "srs", "use-cases"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Software Design and Testing",
                        "number": 2,
                        "topics": [
                            {"name": "UML Diagrams", "description": "Class, sequence, activity, state machine, component diagrams", "tags": ["uml", "class-diagram", "sequence-diagram"], "importance_score": 0.85},
                            {"name": "Software Testing", "description": "Unit testing, integration testing, system testing, TDD, BDD", "tags": ["testing", "tdd", "bdd", "unit-testing"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Project Management",
                        "number": 3,
                        "topics": [
                            {"name": "Project Estimation", "description": "COCOMO, function point analysis, effort estimation techniques", "tags": ["estimation", "cocomo", "function-point"], "importance_score": 0.7},
                            {"name": "Version Control", "description": "Git workflows, branching strategies, code review practices", "tags": ["git", "version-control", "branching"], "importance_score": 0.85},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "semester": 8,
        "name": "Semester 8",
        "subjects": [
            {
                "name": "Information Security",
                "code": "CS801",
                "description": "Cryptography, network security, and security practices",
                "tags": ["security", "cryptography", "cybersecurity"],
                "units": [
                    {
                        "name": "Cryptography",
                        "number": 1,
                        "topics": [
                            {"name": "Symmetric Key Cryptography", "description": "DES, AES, block ciphers, stream ciphers, modes of operation", "tags": ["aes", "des", "symmetric"], "importance_score": 0.9},
                            {"name": "Public Key Cryptography", "description": "RSA, Diffie-Hellman, digital signatures, PKI infrastructure", "tags": ["rsa", "diffie-hellman", "pki"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Network Security",
                        "number": 2,
                        "topics": [
                            {"name": "Web Security", "description": "XSS, CSRF, SQL injection, OWASP top 10, secure coding", "tags": ["xss", "csrf", "sql-injection", "owasp"], "importance_score": 0.95},
                            {"name": "Network Protocols Security", "description": "SSL/TLS, IPSec, firewalls, IDS/IPS, VPN", "tags": ["ssl", "tls", "firewall", "vpn"], "importance_score": 0.85},
                        ],
                    },
                    {
                        "name": "Security Practices",
                        "number": 3,
                        "topics": [
                            {"name": "Authentication Mechanisms", "description": "MFA, biometrics, password hashing, session security", "tags": ["authentication", "mfa", "hashing"], "importance_score": 0.85},
                            {"name": "Security Auditing", "description": "Penetration testing, vulnerability assessment, security compliance", "tags": ["pentesting", "vulnerability", "compliance"], "importance_score": 0.75},
                        ],
                    },
                ],
            },
            {
                "name": "Cloud Computing",
                "code": "CS802",
                "description": "Cloud architecture, services, and deployment models",
                "tags": ["cloud", "aws", "devops"],
                "units": [
                    {
                        "name": "Cloud Fundamentals",
                        "number": 1,
                        "topics": [
                            {"name": "Cloud Service Models", "description": "IaaS, PaaS, SaaS comparison, cloud deployment models (public, private, hybrid)", "tags": ["iaas", "paas", "saas", "cloud-models"], "importance_score": 0.85},
                            {"name": "Virtualization", "description": "Virtual machines, containers, hypervisors, Docker, Kubernetes", "tags": ["virtualization", "docker", "kubernetes"], "importance_score": 0.9},
                        ],
                    },
                    {
                        "name": "Cloud Services",
                        "number": 2,
                        "topics": [
                            {"name": "AWS Core Services", "description": "EC2, S3, RDS, Lambda, VPC, IAM", "tags": ["aws", "ec2", "s3", "lambda"], "importance_score": 0.9},
                            {"name": "Serverless Architecture", "description": "Functions as a Service, event-driven architecture, API Gateway", "tags": ["serverless", "faas", "event-driven"], "importance_score": 0.8},
                        ],
                    },
                    {
                        "name": "Cloud Architecture",
                        "number": 3,
                        "topics": [
                            {"name": "Microservices", "description": "Microservice architecture, service mesh, API gateway patterns", "tags": ["microservices", "service-mesh", "api-gateway"], "importance_score": 0.85},
                            {"name": "Scalability and Reliability", "description": "Auto-scaling, load balancing, disaster recovery, CAP theorem", "tags": ["scalability", "load-balancing", "cap-theorem"], "importance_score": 0.8},
                        ],
                    },
                ],
            },
        ],
    },
]

RESOURCE_TEMPLATES = {
    "college_notes": [
        ("Lecture Notes - {topic}", "https://college.edu/notes/{slug}"),
        ("Class Handout - {topic}", "https://college.edu/handouts/{slug}"),
    ],
    "external_notes": [
        ("GeeksForGeeks - {topic}", "https://www.geeksforgeeks.org/{slug}"),
        ("TutorialsPoint - {topic}", "https://www.tutorialspoint.com/{slug}"),
    ],
    "pdf": [
        ("Reference Material - {topic}", "https://college.edu/pdfs/{slug}.pdf"),
    ],
    "video": [
        ("NPTEL Lecture - {topic}", "https://nptel.ac.in/courses/{slug}"),
        ("YouTube Tutorial - {topic}", "https://www.youtube.com/watch?v={slug}"),
    ],
    "pyq": [
        ("Previous Year Questions 2023", "https://college.edu/pyq/{slug}_2023"),
        ("Previous Year Questions 2022", "https://college.edu/pyq/{slug}_2022"),
    ],
    "important_questions": [
        ("Important Questions Bank", "https://college.edu/questions/{slug}"),
    ],
    "practice_questions": [
        ("Practice Set 1 - {topic}", "https://college.edu/practice/{slug}_set1"),
        ("Practice Set 2 - {topic}", "https://college.edu/practice/{slug}_set2"),
    ],
    "coding_problems": [
        ("LeetCode Problems - {topic}", "https://leetcode.com/tag/{slug}"),
        ("HackerRank Challenges - {topic}", "https://www.hackerrank.com/domains/{slug}"),
    ],
    "assignment": [
        ("Assignment 1 - {topic}", "https://college.edu/assignments/{slug}_a1"),
    ],
    "book": [
        ("Recommended Textbook - {topic}", "https://college.edu/books/{slug}"),
    ],
    "documentation": [
        ("Official Documentation - {topic}", "https://docs.example.com/{slug}"),
    ],
    "image": [
        ("Diagram - {topic}", "https://college.edu/images/{slug}.png"),
    ],
}


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-")


def seed_resources(db: SessionLocal, topic: Topic) -> None:
    import random

    slug = slugify(topic.name)
    resource_types = list(RESOURCE_TEMPLATES.keys())
    selected_types = random.sample(resource_types, min(random.randint(2, 4), len(resource_types)))

    for res_type in selected_types:
        templates = RESOURCE_TEMPLATES[res_type]
        title, url_template = random.choice(templates)
        resource = Resource(
            topic_id=topic.id,
            type=ResourceType(res_type),
            title=title.format(topic=topic.name, slug=slug),
            url=url_template.format(topic=topic.name, slug=slug),
            content=f"Content related to {topic.name} - {res_type}",
            metadata_={"difficulty": random.choice(["easy", "medium", "hard"]), "rating": round(random.uniform(3.0, 5.0), 1)},
        )
        db.add(resource)


def run_seed():
    import random
    random.seed(42)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing = db.query(Semester).first()
        if existing:
            print("Database already seeded. Skipping.")
            return

        for sem_data in SEED:
            semester = Semester(name=sem_data["name"], number=sem_data["semester"])
            db.add(semester)
            db.flush()

            for subj_data in sem_data["subjects"]:
                subject = Subject(
                    name=subj_data["name"],
                    code=subj_data["code"],
                    semester_id=semester.id,
                    description=subj_data["description"],
                    tags=subj_data["tags"],
                )
                db.add(subject)
                db.flush()

                for unit_data in subj_data["units"]:
                    unit = Unit(
                        name=unit_data["name"],
                        number=unit_data["number"],
                        subject_id=subject.id,
                        description=f"Unit {unit_data['number']} of {subj_data['name']}",
                    )
                    db.add(unit)
                    db.flush()

                    for topic_data in unit_data["topics"]:
                        topic = Topic(
                            name=topic_data["name"],
                            unit_id=unit.id,
                            description=topic_data["description"],
                            tags=topic_data["tags"],
                            importance_score=topic_data["importance_score"],
                        )
                        db.add(topic)
                        db.flush()

                        seed_resources(db, topic)

        db.commit()
        print("Seed data inserted successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

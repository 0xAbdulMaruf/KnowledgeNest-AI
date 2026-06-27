import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal, engine, Base
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.topic import Topic
from app.models.resource import Resource, ResourceType


C_PROGRAMMING_SUBJECT = {
    "name": "Computer Programming in C",
    "code": "CST201",
    "description": "Study of structured programming concepts using C language covering basics, control structures, arrays, functions, and pointers",
    "tags": ["c-programming", "structured-programming", "procedural"],
    "units": [
        {
            "name": "Basics of C",
            "number": 1,
            "description": "History of C, character set, tokens, constants, variables, keywords, data types, operators, precedence, I/O",
            "topics": [
                {
                    "name": "Introduction to C Language",
                    "description": "History of C by Dennis Ritchie at Bell Labs (1972), advantages of structured programming, source/header/object/binary files, characteristics of C language",
                    "tags": ["c-intro", "history", "structured-programming"],
                    "importance_score": 0.8,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Introduction to C", "url": "https://college.edu/notes/c-intro", "content": "C is a general-purpose mid-level programming language developed by Dennis M. Ritchie at Bell Laboratories in 1972. It was initially used for UNIX OS development. C is considered mother of all programming languages. Key features: structured, portable, efficient, rich library, extensible, middle-level language."},
                        {"type": "external_notes", "title": "GeeksforGeeks - C Language Introduction", "url": "https://www.geeksforgeeks.org/c/c-language-introduction/", "content": "C is a procedural programming language. It was initially developed by Dennis Ritchie between 1969 and 1973. It was mainly developed as a system programming language to write an operating system. Main features: Simple, Machine Independent, Mid-Level, Structured, Rich Library, Memory Management, Speed, Pointer, Recursion."},
                        {"type": "video", "title": "NPTEL - Introduction to C Programming", "url": "https://nptel.ac.in/courses/c-intro"},
                        {"type": "pyq", "title": "PYQ 2023 - Introduction to C", "url": "https://college.edu/pyq/c-intro-2023", "content": "Q1: Who developed C language? Q2: List any 5 features of C language. Q3: Explain the compilation process of a C program."},
                        {"type": "book", "title": "Programming in C - Reema Thareja (Ch 1)", "url": "https://college.edu/books/reema-thareja-c"},
                    ]
                },
                {
                    "name": "C Character Set, Tokens and Keywords",
                    "description": "C character set (letters, digits, special characters), tokens (keywords, identifiers, constants, strings, operators, punctuators), 32 keywords in C",
                    "tags": ["tokens", "keywords", "identifiers", "character-set"],
                    "importance_score": 0.85,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Tokens and Keywords", "url": "https://college.edu/notes/c-tokens", "content": "Tokens are the basic building blocks of C program. Types: Keywords (auto, break, case, char, const, continue, default, do, double, else, enum, extern, float, for, goto, if, int, long, register, return, short, signed, sizeof, static, struct, switch, typedef, union, unsigned, void, volatile, while). Identifiers: names given to variables, functions, arrays. Rules: start with letter/underscore, can contain letters/digits/underscore, no keywords."},
                        {"type": "external_notes", "title": "GeeksforGeeks - C Identifiers", "url": "https://www.geeksforgeeks.org/c/c-identifiers/", "content": "Identifiers are user-defined names for variables, functions, arrays etc. Rules: First character must be letter or underscore. Only letters, digits, underscores allowed. Case sensitive. No keywords as identifiers. No length limit (but first 31 characters are significant."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Keywords in C", "url": "https://www.geeksforgeeks.org/c/keywords-in-c/", "content": "Keywords are reserved words with predefined meanings. C89 has 32 keywords. C99 added: _Bool, _Complex, _Imaginary, inline, restrict. C11 added: _Alignas, _Alignof, _Atomic, _Generic, _Noreturn, _Static_assert, _Thread_local."},
                        {"type": "practice_questions", "title": "Practice - Identify Tokens", "url": "https://college.edu/practice/c-tokens", "content": "1. Which of the following are valid identifiers? _count, 1value, int, my-var, float1. 2. How many keywords are there in ANSI C? 3. Classify tokens in: int a = 10 + 20;"},
                    ]
                },
                {
                    "name": "Variables and Data Types",
                    "description": "Declaration and initialization of variables, data types (int, float, char, double, void), type modifiers (short, long, signed, unsigned), sizeof operator",
                    "tags": ["variables", "data-types", "int", "float", "char", "sizeof"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Variables and Data Types", "url": "https://college.edu/notes/c-variables", "content": "Variables: named memory locations to store data. Declaration: datatype variable_name; Initialization: int a = 10; Data Types: int(2/4 bytes), float(4 bytes), double(8 bytes), char(1 byte), void(no value). Type modifiers: short, long, signed, unsigned. sizeof() returns size in bytes."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Variables in C", "url": "https://www.geeksforgeeks.org/c/variables-in-c/", "content": "A variable is a name given to a memory location. Types: Local (declared inside function/block), Global (declared outside all functions), Static (retains value between function calls), External (declared with extern keyword). Rules for naming: start with letter/underscore, no special chars except underscore."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Data Types in C", "url": "https://www.geeksforgeeks.org/c/data-types-in-c/", "content": "Data types: int (2 or 4 bytes, -32768 to 32767 or -2147483648 to 2147483647), char (1 byte, -128 to 127), float (4 bytes, 6 decimal precision), double (8 bytes, 15 decimal precision), void (no value). Derived types: array, pointer, structure, union, enum."},
                        {"type": "video", "title": "YouTube - C Data Types Explained", "url": "https://www.youtube.com/watch?v=c_data_types"},
                        {"type": "pyq", "title": "PYQ 2023 - Variables and Data Types", "url": "https://college.edu/pyq/c-variables-2023", "content": "Q1: What is the difference between float and double? Q2: What is the size of int, char, float on a 32-bit system? Q3: Explain type conversion with example."},
                        {"type": "practice_questions", "title": "Practice - Data Types", "url": "https://college.edu/practice/c-datatypes", "content": "1. What will be the output: printf('%d', sizeof(int)); 2. Find the output: int a = 5/2; printf('%d', a); 3. What is the range of unsigned char?"},
                    ]
                },
                {
                    "name": "Operators in C",
                    "description": "Arithmetic, relational, logical, assignment, bitwise, unary, ternary, sizeof, comma operators. Operator precedence and associativity. Type conversion and typecasting",
                    "tags": ["operators", "precedence", "associativity", "type-conversion"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Operators", "url": "https://college.edu/notes/c-operators", "content": "Arithmetic: +, -, *, /, %. Relational: ==, !=, >, <, >=, <=. Logical: &&, ||, !. Assignment: =, +=, -=, *=, /=, %=. Bitwise: &, |, ^, ~, <<, >>. Unary: ++, --, +, -, !, ~. Ternary: condition ? expr1 : expr2. Precedence: () > unary > * / % > + - > << >> > relational > & ^ | > && || > ternary > assignment > comma."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Operators in C", "url": "https://www.geeksforgeeks.org/c/operators-in-c/", "content": "Operators are symbols that tell compiler to perform specific mathematical or logical operations. Types: Arithmetic, Relational, Logical, Bitwise, Assignment, Conditional, Special. Precedence determines evaluation order."},
                        {"type": "coding_problems", "title": "LeetCode - Operator Practice", "url": "https://leetcode.com/tag/operators", "content": "1. Swap two numbers without using third variable. 2. Check if a number is even or odd without using % operator. 3. Find the maximum of two numbers without using if-else."},
                        {"type": "pyq", "title": "PYQ 2022 - Operators", "url": "https://college.edu/pyq/c-operators-2022", "content": "Q1: What is the output of: int a=5, b=10; printf('%d', a>b?a:b); Q2: Explain bitwise operators with examples. Q3: What is the difference between ++i and i++?"},
                    ]
                },
                {
                    "name": "Input and Output in C",
                    "description": "Formatted input/output using printf() and scanf(), format specifiers (%d, %f, %c, %s, %ld, %lf), escape sequences, unformatted I/O (getchar, putchar, gets, puts)",
                    "tags": ["printf", "scanf", "format-specifiers", "io"],
                    "importance_score": 0.85,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - I/O Functions", "url": "https://college.edu/notes/c-io", "content": "printf(): formatted output. Format specifiers: %d(int), %f(float), %c(char), %s(string), %ld(long), %lf(double), %o(oct), %x(hex), %u(unsigned). Width/precision: %10d, %.2f. scanf(): formatted input. & operator needed for variables. Escape sequences: \\n, \\t, \\r, \\\\, \\', \\\", \\0."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Basic I/O in C", "url": "https://www.geeksforgeeks.org/c/basic-input-and-output-in-c/", "content": "printf() sends formatted output to stdout. scanf() reads formatted input from stdin. getchar() reads single character. putchar() writes single character. gets() reads line. puts() writes line. fprintf/fscanf for files."},
                        {"type": "practice_questions", "title": "Practice - I/O Operations", "url": "https://college.edu/practice/c-io", "content": "1. Write a program to input name, roll, marks and display them. 2. What is the difference between %d and %i? 3. Write format specifier for: (a) 10-digit left-justified integer (b) float with 2 decimal places."},
                    ]
                },
            ]
        },
        {
            "name": "Decision Control and Looping Statements",
            "number": 2,
            "description": "if-else, switch-case, goto, while, do-while, for loops, break, continue, nested loops",
            "topics": [
                {
                    "name": "Decision Making - if, if-else, else-if Ladder",
                    "description": "if statement, if-else, else-if ladder, nested if-else, conditional expressions, truthy/falsy values in C",
                    "tags": ["if-else", "conditional", "decision-making", "branching"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Decision Making", "url": "https://college.edu/notes/c-decision", "content": "if statement: if(condition) { statements; }. if-else: if(condition) { } else { }. else-if ladder: if(c1) {} else if(c2) {} else {}. Nested if: if(c1) { if(c2) {} }. Non-zero is true, zero is false."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Decision Making in C", "url": "https://www.geeksforgeeks.org/c/decision-making-in-c/", "content": "Decision making statements: if, if-else, nested if, if-else-if ladder, switch. The if statement evaluates expression in parentheses. If expression is true (nonzero), statement is executed."},
                        {"type": "coding_problems", "title": "Practice - Decision Making", "url": "https://college.edu/practice/c-decision", "content": "1. Find largest of three numbers. 2. Check if year is leap year. 3. Grade calculator (A/B/C/D/F based on marks). 4. Check if character is vowel or consonant."},
                        {"type": "pyq", "title": "PYQ 2023 - Decision Control", "url": "https://college.edu/pyq/c-decision-2023", "content": "Q1: Write a program to check if a number is positive, negative or zero. Q2: What is the difference between if-else and switch? Q3: Find output: int x=5; if(x=0) printf('Zero'); else printf('Non-zero');"},
                    ]
                },
                {
                    "name": "Switch Case Statement",
                    "description": "switch statement syntax, case labels, default, break statement in switch, fall-through behavior, applications",
                    "tags": ["switch-case", "break", "fall-through", "menu-driven"],
                    "importance_score": 0.85,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Switch Case", "url": "https://college.edu/notes/c-switch", "content": "switch(expression) { case val1: statements; break; case val2: statements; break; default: statements; }. Expression must be integer/char. Cases must be constants. Break prevents fall-through. Default is optional. Multiple cases can share code."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Switch Statement", "url": "https://www.geeksforgeeks.org/c/switch-statement-in-c/", "content": "Switch is a multiway branch statement. Expression must evaluate to integer. Each case value must be unique. Break transfers control after switch. Default handles no match. No duplicate cases allowed."},
                        {"type": "coding_problems", "title": "Practice - Switch Case", "url": "https://college.edu/practice/c-switch", "content": "1. Calculator using switch (+, -, *, /, %). 2. Day of week using switch. 3. Menu-driven program for array operations."},
                    ]
                },
                {
                    "name": "Loop Statements - while, do-while, for",
                    "description": "Entry-controlled loops (while, for), exit-controlled loop (do-while), loop components (initialization, condition, update), infinite loops, nested loops",
                    "tags": ["while-loop", "do-while", "for-loop", "loops", "iteration"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Loops", "url": "https://college.edu/notes/c-loops", "content": "while: while(condition) { body; } - entry controlled, may execute 0 times. do-while: do { body; } while(condition); - exit controlled, executes at least once. for: for(init; condition; update) { body; } - most compact. Nested loops: loop inside loop, inner executes fully for each outer iteration."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Loops in C", "url": "https://www.geeksforgeeks.org/c/c-loops/", "content": "Three types: for (when iterations known), while (when condition-based), do-while (when body must execute once). for(initialization; condition; updation) { body }. Infinite loops: while(1) or for(;;). Break exits loop, continue skips to next iteration."},
                        {"type": "coding_problems", "title": "Practice - Loops", "url": "https://college.edu/practice/c-loops", "content": "1. Print Fibonacci series up to n. 2. Find factorial of a number. 3. Print multiplication table. 4. Count digits in a number. 5. Reverse a number. 6. Check if number is palindrome. 7. Print pattern: * ** *** ****"},
                        {"type": "pyq", "title": "PYQ 2022 - Loops", "url": "https://college.edu/pyq/c-loops-2022", "content": "Q1: Difference between while and do-while. Q2: Write a program to find sum of digits of a number. Q3: What is the output: for(i=0;i<5;i++); printf('%d',i);"},
                        {"type": "practice_questions", "title": "Practice Set - Loop Programs", "url": "https://college.edu/practice/c-loop-programs", "content": "1. Print all prime numbers between 1 to n. 2. Find GCD and LCM of two numbers. 3. Print Pascal's triangle. 4. Sum of series: 1 + 1/2 + 1/3 + ... + 1/n. 5. Armstrong numbers between 100 to 1000."},
                    ]
                },
                {
                    "name": "Break, Continue and Goto Statements",
                    "description": "break to exit loop/switch, continue to skip iteration, goto for unconditional jump, drawbacks of goto, labeled statements",
                    "tags": ["break", "continue", "goto", "jump-statements"],
                    "importance_score": 0.75,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Jump Statements", "url": "https://college.edu/notes/c-jump", "content": "break: exits innermost loop or switch. continue: skips remaining body, goes to next iteration. goto: jumps to labeled statement. label_name: statement. goto label_name; Avoid goto - leads to spaghetti code. break and continue only affect innermost loop."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Break and Continue", "url": "https://www.geeksforgeeks.org/c/break-and-continue-statement-in-c/", "content": "break terminates loop/switch, control goes to next statement after loop. continue skips to loop's next iteration. In nested loops, break only exits innermost loop."},
                        {"type": "coding_problems", "title": "Practice - Break and Continue", "url": "https://college.edu/practice/c-break-continue", "content": "1. Find first number divisible by 7 in range using break. 2. Print odd numbers using continue. 3. Menu-driven loop that exits on user choice."},
                    ]
                },
            ]
        },
        {
            "name": "Subscripted Variables / Arrays",
            "number": 3,
            "description": "1D arrays, 2D arrays, multidimensional arrays, character arrays, strings, string handling functions",
            "topics": [
                {
                    "name": "One Dimensional Arrays",
                    "description": "Declaration, initialization, accessing elements, array traversal, array as function parameter, array bounds, advantages of arrays",
                    "tags": ["1d-array", "array-declaration", "array-initialization", "array-traversal"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - 1D Arrays", "url": "https://college.edu/notes/c-1d-array", "content": "Declaration: int arr[5]; Initialization: int arr[] = {1,2,3,4,5}; Access: arr[index] (0-based). Array name is pointer to first element. Size must be constant (C89). Passing array to function passes address (call by reference). Array elements stored contiguously."},
                        {"type": "external_notes", "title": "GeeksforGeeks - C Arrays", "url": "https://www.geeksforgeeks.org/c/c-arrays/", "content": "Array is collection of similar types stored at contiguous memory. Types: 1D, 2D, Multi-dimensional. Advantages: random access, cache friendly, less memory. Disadvantages: fixed size, insertion/deletion costly."},
                        {"type": "coding_problems", "title": "Practice - 1D Array", "url": "https://college.edu/practice/c-1d-array", "content": "1. Find largest/smallest element. 2. Reverse an array. 3. Find second largest element. 4. Remove duplicates from sorted array. 5. Rotate array by k positions."},
                        {"type": "pyq", "title": "PYQ 2023 - Arrays", "url": "https://college.edu/pyq/c-arrays-2023", "content": "Q1: What is the difference between arr and &arr? Q2: Write a program to sort array in ascending order. Q3: How are arrays stored in memory?"},
                    ]
                },
                {
                    "name": "Two Dimensional Arrays",
                    "description": "Declaration and initialization of 2D arrays, matrix operations, row-major and column-major storage, passing 2D array to function",
                    "tags": ["2d-array", "matrix", "row-major", "multidimensional"],
                    "importance_score": 0.9,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - 2D Arrays", "url": "https://college.edu/notes/c-2d-array", "content": "Declaration: int arr[3][4]; Initialization: int arr[2][3] = {{1,2,3},{4,5,6}}; Access: arr[row][col]. Stored in row-major order in C. Passing to function: void func(int arr[][4], int rows). Total elements = rows * cols."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Multidimensional Arrays", "url": "https://www.geeksforgeeks.org/c/multidimensional-arrays-in-c/", "content": "2D array is array of arrays. Stored contiguously in row-major order. arr[i][j] = *(arr[i] + j) = *(*(arr + i) + j). Can have 3D and higher dimensions."},
                        {"type": "coding_problems", "title": "Practice - Matrix Operations", "url": "https://college.edu/practice/c-matrix", "content": "1. Matrix addition and subtraction. 2. Matrix multiplication. 3. Transpose of matrix. 4. Find diagonal sum. 5. Check if matrix is identity matrix. 6. Spiral traversal of matrix."},
                    ]
                },
                {
                    "name": "Strings in C",
                    "description": "Character arrays, string initialization, null terminator, string input/output, string operations, array of strings",
                    "tags": ["strings", "character-array", "null-terminator", "string-io"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Strings", "url": "https://college.edu/notes/c-strings", "content": "String: character array terminated by '\\0'. Declaration: char str[6] = 'Hello'; or char str[] = 'Hello'; Input: scanf('%s', str) or gets(str). Output: printf('%s', str) or puts(str). String always needs space for null character."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Strings in C", "url": "https://www.geeksforgeeks.org/c/strings-in-c/", "content": "String is array of characters ending with null character '\\0'. Ways to declare: char str[] = {'H','i','\\0'}; char str[] = 'Hi'; char *str = 'Hi'; String literal stored in read-only memory."},
                        {"type": "coding_problems", "title": "Practice - Strings", "url": "https://college.edu/practice/c-strings", "content": "1. Find length of string without strlen. 2. Reverse a string. 3. Check palindrome string. 4. Count vowels and consonants. 5. Convert to uppercase/lowercase. 6. Find frequency of each character."},
                        {"type": "pyq", "title": "PYQ 2023 - Strings", "url": "https://college.edu/pyq/c-strings-2023", "content": "Q1: What is the difference between char *s = 'Hello' and char s[] = 'Hello'? Q2: Write a program to concatenate two strings without using strcat."},
                    ]
                },
                {
                    "name": "String Handling Functions",
                    "description": "Standard library string functions: strlen(), strcpy(), strcat(), strcmp(), strrev(), strupr(), strlwr(), strncpy(), strncmp(), strstr()",
                    "tags": ["string-functions", "strlen", "strcpy", "strcat", "strcmp"],
                    "importance_score": 0.9,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - String Functions", "url": "https://college.edu/notes/c-string-func", "content": "strlen(s): returns length excluding '\\0'. strcpy(dest, src): copies src to dest. strcat(dest, src): appends src to dest. strcmp(s1, s2): returns 0 if equal, <0 if s1<s2, >0 if s1>s2. strncpy/strncmp: with n limit. strstr(haystack, needle): finds substring. strrev(s): reverses (non-standard). strupr/strlwr: case conversion (non-standard)."},
                        {"type": "external_notes", "title": "GeeksforGeeks - String Functions", "url": "https://www.geeksforgeeks.org/c/string-functions-in-c/", "content": "Header: <string.h>. strlen() - length. strcpy() - copy. strcat() - concatenate. strcmp() - compare. strchr() - find char. strrchr() - last occurrence. strstr() - find substring. memcpy/memmove - memory copy. memset - fill memory."},
                        {"type": "coding_problems", "title": "Practice - String Functions", "url": "https://college.edu/practice/c-string-func", "content": "1. Implement your own strlen(). 2. Implement strcpy() without using library. 3. Extract substring from left, right, middle. 4. Replace character in string. 5. Count words in a sentence."},
                    ]
                },
            ]
        },
        {
            "name": "User Defined Functions",
            "number": 4,
            "description": "Function definition, declaration, calling, recursion, scope and lifetime, storage classes, call by value/reference",
            "topics": [
                {
                    "name": "Functions - Definition, Declaration and Calling",
                    "description": "Function prototype/declaration, function definition, function calling, return statement, parameter passing, function signature, advantages of functions",
                    "tags": ["functions", "prototype", "definition", "function-call", "return"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Functions Basics", "url": "https://college.edu/notes/c-functions", "content": "Function: reusable block of code. Prototype: return_type func_name(parameter_list); Definition: return_type func_name(params) { body; return value; }. Calling: func_name(arguments). void functions return nothing. main() is entry point. Functions must be declared before use (or use prototype)."},
                        {"type": "external_notes", "title": "GeeksforGeeks - C Functions", "url": "https://www.geeksforgeeks.org/c/c-functions/", "content": "Types: No argument no return, No argument with return, With argument no return, With argument with return. Advantages: reusability, modularity, debugging ease, abstraction. Function declaration vs definition: declaration is prototype, definition has body."},
                        {"type": "coding_problems", "title": "Practice - Functions", "url": "https://college.edu/practice/c-functions", "content": "1. Write function to find factorial. 2. Write function to check prime. 3. Write function to find GCD. 4. Menu-driven calculator using functions. 5. Write function to print Fibonacci series."},
                        {"type": "pyq", "title": "PYQ 2023 - Functions", "url": "https://college.edu/pyq/c-functions-2023", "content": "Q1: What is the difference between function declaration and definition? Q2: Explain parameter passing techniques. Q3: Write a function to find power of a number."},
                    ]
                },
                {
                    "name": "Scope and Lifetime of Variables - Storage Classes",
                    "description": "Local, global, static variables. Storage classes: auto, extern, static, register. Scope rules, block scope, function scope, file scope",
                    "tags": ["scope", "storage-classes", "auto", "static", "extern", "register"],
                    "importance_score": 0.9,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Storage Classes", "url": "https://college.edu/notes/c-storage", "content": "Storage classes determine scope, lifetime, default value, storage location. auto: default for local, stack, undefined default. static: retains value, initialized to 0, persists across calls. extern: global visibility across files, initialized to 0. register: stored in CPU register (hint), no address, auto-initialized."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Storage Classes in C", "url": "https://www.geeksforgeeks.org/c/storage-classes-in-c/", "content": "Four storage classes: auto (default local, automatic storage duration), static (persists between function calls), register (stored in register if possible), extern (declared in another file/scope). Scope: local (block), global (file), function prototype."},
                        {"type": "coding_problems", "title": "Practice - Storage Classes", "url": "https://college.edu/practice/c-storage", "content": "1. Demonstrate static variable behavior. 2. Show difference between auto and static. 3. Use extern to share variable between files."},
                    ]
                },
                {
                    "name": "Call by Value and Call by Reference",
                    "description": "Pass by value (copy of argument), pass by reference (using pointers), differences, when to use which, array passing",
                    "tags": ["call-by-value", "call-by-reference", "parameter-passing", "pointers"],
                    "importance_score": 0.9,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Parameter Passing", "url": "https://college.edu/notes/c-param-pass", "content": "Call by Value: function gets copy of actual parameter. Changes don't affect original. Call by Reference: function gets address (using pointers). Changes affect original. C only supports call by value, but simulates call by reference using pointers. Arrays always passed by reference (address of first element)."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Parameter Passing", "url": "https://www.geeksforgeeks.org/c/parameter-passing-techniques-in-c-cpp/", "content": "Pass by Value: formal parameter is copy. Original unchanged. Pass by Reference (via pointer): formal parameter is pointer to original. Dereferencing modifies original. Pass by Array: array name is pointer to first element."},
                        {"type": "coding_problems", "title": "Practice - Parameter Passing", "url": "https://college.edu/practice/c-param-pass", "content": "1. Swap two numbers using call by reference. 2. Write function to modify array elements. 3. Demonstrate call by value vs reference with example."},
                        {"type": "pyq", "title": "PYQ 2022 - Parameter Passing", "url": "https://college.edu/pyq/c-param-2022", "content": "Q1: What is the difference between call by value and call by reference? Q2: Can we pass arrays by value? Explain. Q3: Write a program to swap two numbers using pointers."},
                    ]
                },
                {
                    "name": "Recursion",
                    "description": "Recursive functions, base case, recursive case, recursion vs iteration, types of recursion (direct, indirect, tail, head), memory stack, applications",
                    "tags": ["recursion", "base-case", "recursive-case", "tail-recursion", "stack"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Recursion", "url": "https://college.edu/notes/c-recursion", "content": "Recursion: function calling itself. Base case: termination condition. Recursive case: calls itself with modified arguments. Types: Direct (A calls A), Indirect (A calls B, B calls A), Tail (recursive call is last), Head (recursive call is first). Stack: each call creates stack frame. Too many calls = stack overflow. Iteration is generally more efficient."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Recursion in C", "url": "https://www.geeksforgeeks.org/c/c-recursion/", "content": "Recursion is technique where function calls itself. Must have: base case (terminates), recursive case (calls itself), progress toward base case. Applications: factorial, fibonacci, tower of hanoi, tree traversals, backtracking. Recursion vs Iteration: recursion uses more memory but is more elegant for certain problems."},
                        {"type": "coding_problems", "title": "Practice - Recursion", "url": "https://college.edu/practice/c-recursion", "content": "1. Factorial using recursion. 2. Fibonacci using recursion. 3. Tower of Hanoi. 4. GCD using recursion. 5. Power function using recursion. 6. Reverse string using recursion. 7. Sum of digits using recursion."},
                        {"type": "pyq", "title": "PYQ 2023 - Recursion", "url": "https://college.edu/pyq/c-recursion-2023", "content": "Q1: What is recursion? Explain with example. Q2: What is the difference between tail and head recursion? Q3: Solve Tower of Hanoi for 3 disks."},
                    ]
                },
            ]
        },
        {
            "name": "Pointers in C",
            "number": 5,
            "description": "Pointer declaration, arithmetic, arrays and pointers, function pointers, dynamic memory allocation, pointer to pointer",
            "topics": [
                {
                    "name": "Introduction to Pointers",
                    "description": "What is pointer, declaring pointers, address-of (&) and dereference (*) operators, null pointer, void pointer, pointer initialization",
                    "tags": ["pointers", "address-of", "dereference", "null-pointer", "void-pointer"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Pointers Basics", "url": "https://college.edu/notes/c-pointers-basics", "content": "Pointer: variable that stores memory address. Declaration: int *ptr; Initialization: ptr = &var; Address-of: &var gives address. Dereference: *ptr gives value at address. NULL pointer: points to nothing (NULL). Void pointer: generic pointer (void *). Dangling pointer: points to freed memory. Wild pointer: uninitialized pointer."},
                        {"type": "external_notes", "title": "GeeksforGeeks - C Pointers", "url": "https://www.geeksforgeeks.org/c/c-pointers/", "content": "Pointer stores address of another variable. Size: 4 bytes (32-bit) or 8 bytes (64-bit). & (address-of) gets address. * (dereference) gets value. Pointer types must match variable type. NULL is defined as (void*)0 or 0. sizeof(any_pointer) is same regardless of type."},
                        {"type": "video", "title": "YouTube - Pointers in C Explained", "url": "https://www.youtube.com/watch?v=c_pointers"},
                        {"type": "pyq", "title": "PYQ 2023 - Pointers Basics", "url": "https://college.edu/pyq/c-ptr-basics-2023", "content": "Q1: What is a pointer? How is it different from a normal variable? Q2: What is the output: int x=10, *p=&x; printf('%d', *p); Q3: Explain dangling pointer with example."},
                    ]
                },
                {
                    "name": "Pointer Arithmetic",
                    "description": "Pointer increment/decrement, pointer addition/subtraction, pointer comparison, pointer difference, constant pointer, pointer to constant",
                    "tags": ["pointer-arithmetic", "pointer-increment", "constant-pointer", "pointer-to-constant"],
                    "importance_score": 0.9,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Pointer Arithmetic", "url": "https://college.edu/notes/c-ptr-arith", "content": "ptr++ increments by sizeof(type). ptr-- decrements by sizeof(type). ptr + n moves n elements. ptr1 - ptr2 gives number of elements between. Pointer comparison: ==, !=, <, >, <=, >=. Constant pointer: int * const ptr (can't change address). Pointer to const: const int *ptr (can't change value)."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Pointer Arithmetic", "url": "https://www.geeksforgeeks.org/c/pointer-arithmetics-in-c-with-examples/", "content": "Operations: Addition (ptr + n), Subtraction (ptr - n, ptr1 - ptr2), Increment (ptr++), Decrement (ptr--), Comparison. ptr + n adds n * sizeof(type) to address. Only meaningful on arrays or allocated memory."},
                        {"type": "coding_problems", "title": "Practice - Pointer Arithmetic", "url": "https://college.edu/practice/c-ptr-arith", "content": "1. Traverse array using pointer arithmetic. 2. Find array size using pointer arithmetic. 3. Demonstrate const pointer vs pointer to const."},
                    ]
                },
                {
                    "name": "Pointers and Arrays",
                    "description": "Array name as pointer, pointer to array, array of pointers, passing array to function using pointers, pointer and string relationship",
                    "tags": ["pointers-arrays", "array-of-pointers", "pointer-to-array", "string-pointer"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Pointers and Arrays", "url": "https://college.edu/notes/c-ptr-array", "content": "Array name is pointer to first element: arr == &arr[0]. arr[i] == *(arr+i). Passing array to function passes pointer. Array of pointers: int *arr[5] (array of 5 int pointers). Pointer to array: int (*ptr)[5] (pointer to array of 5 ints). String: char *str = 'Hello' or char str[] = 'Hello'."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Pointers and Arrays", "url": "https://www.geeksforgeeks.org/c/c-pointers/", "content": "arr[i] is equivalent to *(arr+i). Both use base address + offset. Array name decays to pointer in expressions (except sizeof and &). Pointer to array vs array of pointers are different."},
                        {"type": "coding_problems", "title": "Practice - Pointers and Arrays", "url": "https://college.edu/practice/c-ptr-array", "content": "1. Reverse array using pointers. 2. Sort array using pointers. 3. Pass 2D array to function using pointer to array. 4. Array of strings using char* array."},
                    ]
                },
                {
                    "name": "Function Pointers and Pointer to Pointer",
                    "description": "Function pointer declaration, callback functions, pointer to pointer (double pointer), void pointer, dynamic dispatch",
                    "tags": ["function-pointer", "double-pointer", "callback", "void-pointer"],
                    "importance_score": 0.8,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Advanced Pointers", "url": "https://college.edu/notes/c-ptr-advanced", "content": "Function pointer: return_type (*ptr)(params). Declaration: int (*add)(int,int) = &add_func; Call: (*add)(3,4) or add(3,4). Used for callbacks, function tables. Double pointer: int **pp; pp = &p; *pp gives p, **pp gives value. Used for 2D arrays, modifying pointer in function."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Function Pointers", "url": "https://www.geeksforgeeks.org/c/function-pointer-in-c/", "content": "Function pointer points to function. Declaration: return_type (*name)(param_types). Usage: callbacks, passing function as argument, creating function arrays. qsort() uses function pointer for comparison."},
                        {"type": "coding_problems", "title": "Practice - Function Pointers", "url": "https://college.edu/practice/c-func-ptr", "content": "1. Calculator using function pointers. 2. Sort array using function pointer comparator. 3. Implement qsort-like function."},
                    ]
                },
                {
                    "name": "Dynamic Memory Allocation",
                    "description": "malloc(), calloc(), realloc(), free(), memory leaks, heap vs stack, dynamic arrays, pointer to structure",
                    "tags": ["malloc", "calloc", "realloc", "free", "dynamic-memory", "heap"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Dynamic Memory", "url": "https://college.edu/notes/c-dma", "content": "malloc(size): allocates size bytes, returns void*, uninitialized. calloc(n, size): allocates n*size bytes, zero-initialized. realloc(ptr, new_size): resizes allocation. free(ptr): deallocates memory. Header: <stdlib.h>. Memory leak: allocated but never freed. Heap: dynamic allocation. Stack: local variables, automatic. Dangling pointer: pointer to freed memory."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Dynamic Memory Allocation", "url": "https://www.geeksforgeeks.org/c/dynamic-memory-allocation-in-c-using-malloc-calloc-free-and-realloc/", "content": "malloc: void* malloc(size_t size) - uninitialized memory. calloc: void* calloc(size_t n, size_t size) - zero-initialized. realloc: void* realloc(void* ptr, size_t size) - resize. free: void free(void* ptr) - deallocate. Check return for NULL. Don't use after free. Don't free twice."},
                        {"type": "coding_problems", "title": "Practice - Dynamic Memory", "url": "https://college.edu/practice/c-dma", "content": "1. Dynamic array using malloc. 2. Dynamic 2D array using malloc. 3. Implement realloc using malloc. 4. Dynamic string concatenation. 5. Dynamic linked list node creation."},
                        {"type": "pyq", "title": "PYQ 2023 - Dynamic Memory", "url": "https://college.edu/pyq/c-dma-2023", "content": "Q1: Difference between malloc and calloc. Q2: What is memory leak? How to prevent? Q3: Write a program to dynamically allocate and deallocate a 2D array."},
                        {"type": "book", "title": "Reference - Dynamic Memory in C", "url": "https://college.edu/books/c-dma"},
                    ]
                },
            ]
        },
    ]
}


PYTHON_SUBJECT = {
    "name": "Scripting Languages (Python)",
    "code": "CST203",
    "description": "Learn Python programming covering variables, control structures, functions, file I/O, regular expressions, and Django framework",
    "tags": ["python", "scripting", "programming"],
    "units": [
        {
            "name": "Introduction, Variables and Data Types",
            "number": 1,
            "description": "Python history, features, variables, numeric types, strings, lists, tuples, dictionaries, operators",
            "topics": [
                {
                    "name": "Introduction to Python",
                    "description": "History of Python by Guido van Rossum (1991), features (interpreted, dynamically typed, indentation-based), installation, basic syntax, interactive interpreter",
                    "tags": ["python-intro", "history", "features", "installation"],
                    "importance_score": 0.8,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python Introduction", "url": "https://college.edu/notes/python-intro", "content": "Python: high-level, interpreted, dynamically typed language by Guido van Rossum (1991). Features: easy syntax, indentation-based, extensive libraries, cross-platform, object-oriented, interpreted. Versions: Python 2 (legacy) vs Python 3 (current). Interactive mode: python3 interpreter. Script mode: python3 script.py."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Introduction", "url": "https://www.geeksforgeeks.org/python/python-introduction/"},
                        {"type": "video", "title": "NPTEL - Python Basics", "url": "https://nptel.ac.in/courses/python-basics"},
                        {"type": "pyq", "title": "PYQ 2023 - Python Basics", "url": "https://college.edu/pyq/python-intro-2023", "content": "Q1: Who developed Python and when? Q2: List any 5 features of Python. Q3: What is the difference between Python 2 and Python 3?"},
                    ]
                },
                {
                    "name": "Python Variables and Data Types",
                    "description": "Variable declaration, naming rules, dynamic typing, type() function, int, float, complex, bool, str, type conversion, type casting",
                    "tags": ["variables", "data-types", "int", "float", "string", "bool", "type-casting"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python Variables", "url": "https://college.edu/notes/python-variables", "content": "Variables: no declaration needed, dynamically typed. x = 10 (int), y = 3.14 (float), z = 'hello' (str), b = True (bool). Type checking: type(x). Naming: start with letter/underscore, case sensitive. Multiple assignment: a, b, c = 1, 2, 3. Type conversion: int(), float(), str(), bool()."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Variables", "url": "https://www.geeksforgeeks.org/python/python-variables/"},
                        {"type": "coding_problems", "title": "Practice - Python Variables", "url": "https://college.edu/practice/python-variables", "content": "1. Swap two variables. 2. Check type of different variables. 3. Type conversion exercises."},
                    ]
                },
                {
                    "name": "Python Strings",
                    "description": "String creation, indexing, slicing, string methods, formatting, f-strings, string operations, escape characters",
                    "tags": ["strings", "slicing", "string-methods", "f-strings", "formatting"],
                    "importance_score": 0.9,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python Strings", "url": "https://college.edu/notes/python-strings", "content": "Strings: immutable sequences of characters. Single/double/triple quotes. Indexing: s[0], s[-1]. Slicing: s[start:stop:step]. Methods: upper(), lower(), strip(), split(), join(), find(), replace(), count(), startswith(), endswith(). Formatting: f'Hello {name}', '{}'.format(), %s. Escape: \\n, \\t, \\\\."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Strings", "url": "https://www.geeksforgeeks.org/python/python-strings/"},
                        {"type": "coding_problems", "title": "Practice - Python Strings", "url": "https://college.edu/practice/python-strings", "content": "1. Reverse a string. 2. Check palindrome. 3. Count words in string. 4. Remove duplicates. 5. String formatting exercises."},
                    ]
                },
                {
                    "name": "Python Lists",
                    "description": "List creation, indexing, slicing, list methods, list comprehensions, nested lists, list operations",
                    "tags": ["lists", "list-methods", "list-comprehension", "slicing"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python Lists", "url": "https://college.edu/notes/python-lists", "content": "Lists: mutable, ordered, allows duplicates. Create: [] or list(). Methods: append(), extend(), insert(), remove(), pop(), sort(), reverse(), index(), count(). Slicing: l[start:stop:step]. List comprehension: [x for x in range(10)]. Nested lists: [[1,2],[3,4]]. Copy: l.copy() or l[:]. Concatenation: l1 + l2. Repetition: l * n."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Lists", "url": "https://www.geeksforgeeks.org/python/python-lists/"},
                        {"type": "coding_problems", "title": "Practice - Python Lists", "url": "https://college.edu/practice/python-lists", "content": "1. Find max/min without built-in. 2. Flatten nested list. 3. Remove duplicates. 4. List comprehension: squares, even numbers. 5. Sort list of tuples."},
                    ]
                },
                {
                    "name": "Python Tuples, Dictionaries and Sets",
                    "description": "Tuples (immutable), dictionaries (key-value), sets (unique elements), operations and methods",
                    "tags": ["tuples", "dictionaries", "sets", "key-value"],
                    "importance_score": 0.85,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Tuples, Dicts, Sets", "url": "https://college.edu/notes/python-data-structs", "content": "Tuples: immutable, ordered. t = (1, 2, 3). Methods: count(), index(). Packing/unpacking. Dictionaries: mutable, key-value. d = {'name': 'John'}. Methods: keys(), values(), items(), get(), update(), pop(). Sets: unordered, unique. s = {1, 2, 3}. Methods: add(), remove(), union(), intersection(), difference()."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Dictionaries", "url": "https://www.geeksforgeeks.org/python/python-dictionary/"},
                        {"type": "coding_problems", "title": "Practice - Data Structures", "url": "https://college.edu/practice/python-data-structs", "content": "1. Word frequency counter using dict. 2. Merge two dictionaries. 3. Find common elements using sets. 4. Convert list to dictionary."},
                    ]
                },
                {
                    "name": "Python Operators",
                    "description": "Arithmetic, comparison, logical, bitwise, assignment, membership, identity operators, operator precedence",
                    "tags": ["operators", "arithmetic", "comparison", "logical", "membership"],
                    "importance_score": 0.85,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python Operators", "url": "https://college.edu/notes/python-operators", "content": "Arithmetic: +, -, *, /, //, %, **. Comparison: ==, !=, >, <, >=, <=. Logical: and, or, not. Bitwise: &, |, ^, ~, <<, >>. Assignment: =, +=, -=, *=, /=, //=, **=. Membership: in, not in. Identity: is, is not. Precedence: ** > ~x > * / // % > + - > >> << > & > ^ | > comparison > not > and > or."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Operators", "url": "https://www.geeksforgeeks.org/python/python-operators/"},
                    ]
                },
            ]
        },
        {
            "name": "Control Structures",
            "number": 2,
            "description": "if-elif-else, for loop, while loop, break, continue, pass, nested loops",
            "topics": [
                {
                    "name": "Conditional Statements - if, elif, else",
                    "description": "if statement, if-else, if-elif-else, nested if, ternary operator, truthy/falsy values",
                    "tags": ["if-elif-else", "conditional", "ternary", "truthy-falsy"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python Conditionals", "url": "https://college.edu/notes/python-conditionals", "content": "if condition: ... elif condition: ... else: ... No braces, indentation-based. Ternary: x if condition else y. Falsy values: None, False, 0, 0.0, '', [], {}, set(). Nested if: if within if. match-case (Python 3.10+)."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python If-Else", "url": "https://www.geeksforgeeks.org/python/python-if-else/"},
                        {"type": "coding_problems", "title": "Practice - Python Conditionals", "url": "https://college.edu/practice/python-conditionals", "content": "1. Grade calculator. 2. Leap year check. 3. Largest of three numbers. 4. Menu-driven program."},
                    ]
                },
                {
                    "name": "For Loop and Iteration",
                    "description": "for loop with range(), iterating over sequences (list, string, tuple, dict, set), enumerate(), zip(), nested for loops",
                    "tags": ["for-loop", "range", "enumerate", "zip", "iteration"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python For Loop", "url": "https://college.edu/notes/python-for", "content": "for item in iterable: ... range(n), range(start, stop, step). Iterating: lists, strings, tuples, dicts, sets, files. enumerate(seq) gives (index, value). zip(seq1, seq2) pairs elements. Nested: for i in ...: for j in .... break/continue/else. List comprehension: [expr for item in iterable]."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python For Loop", "url": "https://www.geeksforgeeks.org/python/python-for-loops/"},
                        {"type": "coding_problems", "title": "Practice - Python For Loop", "url": "https://college.edu/practice/python-for", "content": "1. Print patterns (triangle, pyramid). 2. Fibonacci series. 3. Prime numbers in range. 4. Factorial. 5. Multiplication table."},
                    ]
                },
                {
                    "name": "While Loop",
                    "description": "while loop syntax, infinite while loop, while-else, loop control (break, continue, pass), sentinel values",
                    "tags": ["while-loop", "break", "continue", "pass", "infinite-loop"],
                    "importance_score": 0.85,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python While Loop", "url": "https://college.edu/notes/python-while", "content": "while condition: ... Executes while condition is True. while True: (infinite). while-else: else executes if loop completes normally (no break). break: exit loop. continue: skip to next iteration. pass: do nothing (placeholder)."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python While Loop", "url": "https://www.geeksforgeeks.org/python/python-while-loop/"},
                        {"type": "coding_problems", "title": "Practice - Python While Loop", "url": "https://college.edu/practice/python-while", "content": "1. Guess the number game. 2. Sum until sentinel. 3. Reverse number. 4. GCD using while."},
                    ]
                },
            ]
        },
        {
            "name": "Functions, Modules and Packages",
            "number": 3,
            "description": "Function definition, arguments, scope, lambda, modules, packages, import",
            "topics": [
                {
                    "name": "Python Functions",
                    "description": "def keyword, parameters, arguments, return, default arguments, keyword arguments, *args, **kwargs, docstrings",
                    "tags": ["functions", "def", "parameters", "args", "kwargs", "return"],
                    "importance_score": 0.95,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Python Functions", "url": "https://college.edu/notes/python-functions", "content": "def func_name(params): '''docstring''' body return value. Default args: def func(x=10). Keyword args: func(x=10, y=20). *args: variable positional args (tuple). **kwargs: variable keyword args (dict). Docstring: first string in function. pass: empty function body."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Functions", "url": "https://www.geeksforgeeks.org/python/python-functions/"},
                        {"type": "coding_problems", "title": "Practice - Python Functions", "url": "https://college.edu/practice/python-functions", "content": "1. Function with *args. 2. Function with **kwargs. 3. Recursive factorial/fibonacci. 4. Function returning multiple values. 5. Higher-order functions."},
                    ]
                },
                {
                    "name": "Variable Scope and Lambda",
                    "description": "Local, nonlocal, global scope. LEGB rule. Lambda functions. map(), filter(), reduce(). Closures",
                    "tags": ["scope", "global", "nonlocal", "lambda", "map-filter"],
                    "importance_score": 0.85,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Scope and Lambda", "url": "https://college.edu/notes/python-scope", "content": "LEGB: Local > Enclosing > Global > Built-in. global: modify global variable. nonlocal: modify enclosing variable. Lambda: lambda args: expression. Anonymous, single expression. map(func, iterable): apply func to each. filter(func, iterable): filter by condition. reduce(func, iterable): accumulate."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Lambda", "url": "https://www.geeksforgeeks.org/python/python-lambda-anonymous-functions/"},
                        {"type": "coding_problems", "title": "Practice - Lambda", "url": "https://college.edu/practice/python-lambda", "content": "1. Sort list of tuples using lambda. 2. Filter even numbers using lambda. 3. Map to square numbers. 4. Reduce to find sum."},
                    ]
                },
                {
                    "name": "Modules and Packages",
                    "description": "Importing modules, from-import, aliasing, creating modules, __name__, packages, __init__.py, pip",
                    "tags": ["modules", "packages", "import", "pip", "init"],
                    "importance_score": 0.8,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Modules", "url": "https://college.edu/notes/python-modules", "content": "Module: .py file with functions/classes. import module. from module import func. from module import *. import module as alias. __name__ == '__main__' for direct execution. Package: directory with __init__.py. pip install package_name. sys.path for module search."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Modules", "url": "https://www.geeksforgeeks.org/python/python-modules/"},
                    ]
                },
            ]
        },
        {
            "name": "File I/O, Text Processing, Regular Expressions",
            "number": 4,
            "description": "File operations, read/write, regular expressions with re module",
            "topics": [
                {
                    "name": "File Handling in Python",
                    "description": "open(), close(), read(), readline(), readlines(), write(), writelines(), with statement, file modes (r, w, a, rb, wb)",
                    "tags": ["file-handling", "open", "read", "write", "with-statement"],
                    "importance_score": 0.9,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - File I/O", "url": "https://college.edu/notes/python-file-io", "content": "open(filename, mode) returns file object. Modes: r (read), w (write, truncate), a (append), r+ (read+write), rb/wb (binary). Methods: read(), readline(), readlines(), write(), writelines(), tell(), seek(), close(). with open() as f: (auto-close). Context manager pattern."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python File I/O", "url": "https://www.geeksforgeeks.org/python/python-file-handling/"},
                        {"type": "coding_problems", "title": "Practice - File I/O", "url": "https://college.edu/practice/python-file", "content": "1. Read and display file contents. 2. Count characters, words, lines. 3. Copy file. 4. Append to file. 5. Process CSV file."},
                    ]
                },
                {
                    "name": "Regular Expressions in Python",
                    "description": "re module, re.match(), re.search(), re.findall(), re.finditer(), re.sub(), re.split(), compile(), patterns and metacharacters",
                    "tags": ["regex", "re-module", "match", "search", "findall", "patterns"],
                    "importance_score": 0.85,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Regex", "url": "https://college.edu/notes/python-regex", "content": "import re. Metacharacters: . ^ $ * + ? { } [ ] \\ | ( ). re.match(pattern, string): match at start. re.search(): first match anywhere. re.findall(): all matches as list. re.finditer(): iterator of match objects. re.sub(): substitute. re.split(): split by pattern. re.compile(): precompile pattern. Groups: () for capturing. Special: \\d digit, \\w word, \\s space, \\b boundary."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Python Regex", "url": "https://www.geeksforgeeks.org/python/python-regex/"},
                        {"type": "coding_problems", "title": "Practice - Regex", "url": "https://college.edu/practice/python-regex", "content": "1. Validate email. 2. Find all phone numbers. 3. Extract dates from text. 4. Replace patterns. 5. Password validation."},
                    ]
                },
            ]
        },
        {
            "name": "Frameworks - Django",
            "number": 5,
            "description": "MVC pattern, Django basics, URLs, templates, forms, models",
            "topics": [
                {
                    "name": "Django Framework Basics",
                    "description": "MVC/MTV pattern, Django installation, project creation, app creation, URL routing, views, templates, static files",
                    "tags": ["django", "mvc", "mtv", "urls", "views", "templates"],
                    "importance_score": 0.8,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Django Basics", "url": "https://college.edu/notes/django-basics", "content": "Django: high-level Python web framework. MTV: Model-Template-View. Install: pip install django. Create project: django-admin startproject. Create app: python manage.py startapp. urls.py: URL patterns. views.py: request handlers. templates/: HTML files. settings.py: configuration. Run: python manage.py runserver."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Django Tutorial", "url": "https://www.geeksforgeeks.org/python/django-tutorial/"},
                        {"type": "documentation", "title": "Django Official Documentation", "url": "https://docs.djangoproject.com/"},
                    ]
                },
                {
                    "name": "Django Templates and Forms",
                    "description": "Template language, template inheritance, filters, context, Django forms, form validation, model forms",
                    "tags": ["django-templates", "template-inheritance", "django-forms", "validation"],
                    "importance_score": 0.75,
                    "resources": [
                        {"type": "college_notes", "title": "Lecture Notes - Django Templates", "url": "https://college.edu/notes/django-templates", "content": "Templates: {{ variable }}, {% tag %}, {{ var|filter }}. Inheritance: {% extends 'base.html' %}, {% block name %}{% endblock %}. Filters: {{ name|upper }}, {{ date|date:'Y-m-d' }}. Forms: class MyForm(forms.Form). render(), is_valid(), cleaned_data. ModelForm: class Meta: model = MyModel."},
                        {"type": "external_notes", "title": "GeeksforGeeks - Django Templates", "url": "https://www.geeksforgeeks.org/python/django-templates/"},
                    ]
                },
            ]
        },
    ]
}


def create_subject(db, semester, subject_data):
    subject = Subject(
        name=subject_data["name"],
        code=subject_data["code"],
        semester_id=semester.id,
        description=subject_data["description"],
        tags=subject_data["tags"],
    )
    db.add(subject)
    db.flush()

    for unit_data in subject_data["units"]:
        unit = Unit(
            name=unit_data["name"],
            number=unit_data["number"],
            subject_id=subject.id,
            description=unit_data["description"],
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

            for res in topic_data.get("resources", []):
                resource = Resource(
                    topic_id=topic.id,
                    type=ResourceType(res["type"]),
                    title=res["title"],
                    url=res.get("url", ""),
                    content=res.get("content", ""),
                    metadata_={"source": "syllabus+gfg", "difficulty": "medium"},
                )
                db.add(resource)


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing = db.query(Subject).filter(Subject.code.in_(["CST201", "CST203"])).first()
        if existing:
            print("C/Python subjects already seeded. Skipping.")
            return

        semester = db.query(Semester).filter(Semester.number == 3).first()
        if not semester:
            semester = Semester(name="Semester 3", number=3)
            db.add(semester)
            db.flush()

        create_subject(db, semester, C_PROGRAMMING_SUBJECT)
        create_subject(db, semester, PYTHON_SUBJECT)

        db.commit()
        print("C and Python subjects seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

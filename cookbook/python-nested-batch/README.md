---
complexity: 9.5
---

# Nested Batch Flow Example

This example demonstrates Nested batch Flow using a simple school grades calculator.

## What this Example Does

Calculates average grades for:

1. Each student in a class
2. Each class in the school

## Structure

```
school/
├── class_a/
│   ├── student1.txt  (grades: 7.5, 8.0, 9.0)
│   └── student2.txt  (grades: 8.5, 7.0, 9.5)
└── class_b/
    ├── student3.txt  (grades: 6.5, 8.5, 7.0)
    └── student4.txt  (grades: 9.0, 9.5, 8.0)
```

## Running the Example

```bash
pip install -r requirements.txt
python main.py
```

## Expected Output

```
Processing class_a...
- student1: Average = 8.2
- student2: Average = 8.3
Class A Average: 8.25

Processing class_b...
- student3: Average = 7.3
- student4: Average = 8.8
Class B Average: 8.05

School Average: 8.15
```

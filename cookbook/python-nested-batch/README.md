# BrainyFlow Nested Flow Example

This example demonstrates nested Flows and the Trigger/Aggregate pattern for hierarchical processing using a simple school grades calculator.

## What this Example Does

Calculates average grades for:

1. Each student in a class
2. Each class in the school
3. The entire school

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

## How it Works

1. **School Flow (Outer Flow)**

   - Starts with `TriggerSchoolProcessingNode` which lists class folders and triggers the `Class Flow` for each class.
   - After all `Class Flow` instances complete, `AggregateSchoolResultsNode` calculates the overall school average.

2. **Class Flow (Nested Flow)**

   - Starts with `TriggerClassProcessingNode` which lists student files in a class and triggers the `Base Flow` for each student.
   - After all `Base Flow` instances for a class complete, `AggregateClassResultsNode` calculates the class average.

3. **Base Flow (Innermost Flow)**
   - Processes a single student's grade file.
   - Contains `LoadGrades` and `CalculateAverage` nodes.
   - `CalculateAverage` node stores the student's average in the global memory and triggers the next step in the `Class Flow` (the `AggregateClassResultsNode`).

## Running the Example

```bash
pip install -r requirements.txt
python main.py
```

## Expected Output

```
Processing school grades...

Processing class_a...
- student1.txt: Average = 8.17
- student2.txt: Average = 8.33
Class A Average: 8.25

Processing class_b...
- student3.txt: Average = 7.33
- student4.txt: Average = 8.83
Class B Average: 8.08

School Average: 8.17
```

## Key Concepts

1. **Nested Flows**: Using a Flow as a node within another Flow.
2. **Trigger/Aggregate Pattern**: Using a Trigger node to fan out work and an Aggregate node to collect results.
3. **Hierarchical Processing**: Processing data in a tree-like structure using nested flows and the fan-out pattern.
4. **Local vs Global Memory**: Using `forkingData` to pass context to nested flows (local memory) while aggregating results in the main flow's global memory.

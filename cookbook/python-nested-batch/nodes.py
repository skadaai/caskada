import os
from brainyflow import Node, Memory

class LoadGrades(Node):
    """Node that loads grades from a student's file."""

    async def prep(self, memory: Memory):
        """Get file path from memory."""
        class_name = memory.class_name
        student_file = memory.student_file
        return os.path.join("school", class_name, student_file)

    async def exec(self, file_path):
        """Load and parse grades from file."""
        with open(file_path, 'r') as f:
            # Each line is a grade
            grades = [float(line.strip()) for line in f]
        return grades

    async def post(self, memory: Memory, prep_res, grades):
        """Store grades in memory."""
        memory.grades = grades
        self.trigger("calculate")

class CalculateAverage(Node):
    """Node that calculates average grade."""

    async def prep(self, memory: Memory):
        """Get grades from memory."""
        return memory.grades

    async def exec(self, grades):
        """Calculate average."""
        return 0 if not grades else sum(grades) / len(grades)

    async def post(self, memory: Memory, prep_res, average):
        """Store and print result."""
        # Store in results dictionary
        if not hasattr(memory, "results"):
            memory.results = {}

        class_name = memory.class_name
        student = memory.student_file # Assuming student_file is the student name

        if class_name not in memory.results:
            memory.results[class_name] = {}

        memory.results[class_name][student] = average

        # Print individual result
        print(f"- {student}: Average = {average:.1f}")
        self.trigger("default")

import os
from caskada import Node

class LoadGrades(Node):
    """Node that loads grades from a student's file."""
    
    async def prep(self, shared):
        """Get file path from parameters."""
        return os.path.join("school", shared.class_name, shared.item)
    
    async def exec(self, file_path):
        """Load and parse grades from file."""
        with open(file_path, 'r') as f:
            # Each line is a grade
            grades = [float(line.strip()) for line in f]
        return grades
    
    async def post(self, shared, prep_res, grades):
        """Store grades in shared store."""
        self.trigger("calculate", {"grades": grades})

class CalculateAverage(Node):
    """Node that calculates average grade."""
    
    async def prep(self, shared):
        """Get grades from shared store."""
        return shared.class_name, shared["grades"]
    
    async def exec(self, prep_res):
        """Calculate average."""
        return sum(prep_res[1]) / len(prep_res[1])
    
    async def post(self, shared, prep_res, average):
        """Store and print result."""
        # Print individual result
        print(f"- {shared.item}: Average = {average:.1f}")
        self.trigger("default", {"average": average})
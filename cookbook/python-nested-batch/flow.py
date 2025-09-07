import os
from caskada import Flow, Node
from nodes import LoadGrades, CalculateAverage

def create_base_flow():
    """Create base flow for processing one student's grades."""
    # Create nodes
    load = LoadGrades()
    calc = CalculateAverage()
    
    # Connect nodes
    load - "calculate" >> calc
    
    # Create and return flow
    return Flow(start=load)

class ClassTrigger(Node):
    """Node for processing all students in a class."""
    
    async def prep(self, shared):
        """Generate parameters for each student in the class."""
        # Get class folder from parameters
        class_name = shared["item"]
        
        # List all student files
        class_path = os.path.join("school", class_name)
        students = [f for f in os.listdir(class_path) if f.endswith(".txt")]
        return class_name, students
        
    async def post(self, shared, prep_res, exec_res):
        # Return parameters for each student
        class_name, students = prep_res
        shared[f"{class_name}_students"] = {}
        shared[f"{class_name}_remaining_students"] = len(students)

        for student in students:
            self.trigger("default", {"class_name": class_name, "item": student})


class ClassReducer(Node):
    """Node for processing all students in a class."""
 
    async def post(self, shared, prep_res, exec_res):
        """Calculate and print class average."""
        class_name = shared["class_name"]
        shared[f"{class_name}_students"][shared.item] = {
            "grades": shared.grades,
            "average": shared.average
        }
        shared[f"{class_name}_remaining_students"] -= 1
        if not shared[f"{class_name}_remaining_students"] == 0:
            return self.trigger(None)

        class_students = shared[f"{class_name}_students"].values()
        class_average = sum(student["average"] for student in class_students) / len(class_students)
        
        print(f"Class {shared.class_name.split('_')[1].upper()} Average: {class_average:.2f}\n")
        self.trigger("default", {"item": class_average})

def create_class_flow():
    """Create flow for processing all students in a class."""
    # Create base flow for single student
    base_flow = create_base_flow()
    # Create class nodes
    class_trigger = ClassTrigger()
    class_reducer = ClassReducer()
    
    # Connect nodes
    class_trigger >> base_flow >> class_reducer
    
    # Create and return flow
    return Flow(start=class_trigger)


class SchoolTrigger(Node):
    """Node for processing all classes in the school."""
    
    async def prep(self, shared):
        """Generate parameters for each class."""
        # List all class folders
        classes = [d for d in os.listdir("school") if os.path.isdir(os.path.join("school", d))]
        return classes

    async def post(self, shared, prep_res, exec_res):
        shared[f"school_classes"] = {}
        shared[f"school_remaining_classes"] = len(prep_res)

        for class_name in prep_res:
            self.trigger("default", {"item": class_name})
    

class SchoolReducer(Node):
    """Node for processing all classes in the school."""
    async def post(self, shared, prep_res, exec_res):
        """Calculate and print school average."""

        shared[f"school_classes"][shared.class_name] = shared.item
        shared[f"school_remaining_classes"] -= 1
        if not shared[f"school_remaining_classes"] == 0:
            return self.trigger(None)

        classes_averages = shared[f"school_classes"].values()
        school_average = sum(classes_averages) / len(classes_averages)
        
        print(f"School Average: {school_average:.2f}")

def create_school_flow():
    """Create the complete school batch processing flow."""
    # Create class flow for single class
    class_flow = create_class_flow()
    # Create school nodes
    school_trigger = SchoolTrigger()
    school_reducer = SchoolReducer()
    
    # Connect nodes
    school_trigger >> class_flow >> school_reducer
    
    # Create and return flow
    return Flow(start=school_trigger)


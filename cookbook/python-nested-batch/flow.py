import os
from brainyflow import Flow, Node, Memory
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

class TriggerClassProcessingNode(Node):
    """Node to generate parameters for each student in a class and trigger processing."""

    async def prep(self, memory: Memory):
        """Generate parameters for each student in the class."""
        # Get class folder from memory
        class_folder = memory.class_name

        # List all student files
        class_path = os.path.join("school", class_folder)
        students = [f for f in os.listdir(class_path) if f.endswith(".txt")]

        # Return parameters for each student
        return [{"student_file": student, "class_name": class_folder} for student in students]

    async def post(self, memory: Memory, params_list: list, exec_res):
        """Trigger the base flow for each student."""
        memory.remaining_students = len(params_list) # Add counter for aggregation
        for params in params_list:
            # Trigger the base flow, passing parameters via forkingData
            self.trigger("process_student", forkingData=params)
        # The aggregation node will be triggered when remaining_students is 0

class AggregateClassResultsNode(Node):
    """Node to calculate and print class average."""

    async def prep(self, memory: Memory):
        """Get class name and results from memory."""
        class_name = memory.class_name
        class_results = memory.results.get(class_name, {})
        return class_name, class_results

    async def exec(self, inputs):
        """Calculate class average."""
        class_name, class_results = inputs
        if not class_results:
            return 0.0
        class_average = sum(class_results.values()) / len(class_results)
        return class_name, class_average

    async def post(self, memory: Memory, prep_res, exec_res):
        """Print class average."""
        class_name, class_average = exec_res
        print(f"Class {class_name.split('_')[1].upper()} Average: {class_average:.2f}\n")
        self.trigger("default") # Trigger next step in the school flow

class TriggerSchoolProcessingNode(Node):
    """Node to generate parameters for each class and trigger processing."""

    async def prep(self, memory: Memory):
        """Generate parameters for each class."""
        # List all class folders
        classes = [d for d in os.listdir("school") if os.path.isdir(os.path.join("school", d))]

        # Return parameters for each class
        return [{"class_name": class_name} for class_name in classes]

    async def post(self, memory: Memory, params_list: list, exec_res):
        """Trigger the class flow for each class."""
        memory.remaining_classes = len(params_list) # Add counter for aggregation
        for params in params_list:
            # Trigger the class flow, passing parameters via forkingData
            self.trigger("process_class", forkingData=params)
        # The aggregation node will be triggered when remaining_classes is 0

class AggregateSchoolResultsNode(Node):
    """Node to calculate and print school average."""

    async def prep(self, memory: Memory):
        """Get results from memory."""
        return memory.results or {}

    async def exec(self, results):
        """Calculate school average."""
        all_grades = []
        for class_results in results.values():
            all_grades.extend(class_results.values())

        if not all_grades:
            return 0.0
        school_average = sum(all_grades) / len(all_grades)
        return school_average

    async def post(self, memory: Memory, prep_res, school_average):
        """Print school average."""
        print(f"School Average: {school_average:.2f}")
        self.trigger("default") # End of the flow

def create_flow():
    """Create the complete nested batch processing flow."""
    # Create base flow for single student
    base_flow = create_base_flow()

    # Create nodes for class processing
    trigger_class = TriggerClassProcessingNode()
    aggregate_class = AggregateClassResultsNode()

    # Create the class flow (processes all students in one class)
    # The trigger_class node fans out to the base_flow for each student.
    # The aggregate_class node runs after all students in the class are processed (triggered by the last student's CalculateAverage node).
    trigger_class - "process_student" >> base_flow
    # The CalculateAverage node in the base_flow needs to trigger 'default' which will then trigger aggregate_class
    base_flow.get_node_by_class(CalculateAverage) - "default" >> aggregate_class # Connect CalculateAverage to aggregate_class

    class_flow = Flow(start=trigger_class) # Class flow starts with triggering student processing

    # Create nodes for school processing
    trigger_school = TriggerSchoolProcessingNode()
    aggregate_school = AggregateSchoolResultsNode()

    # Create the school flow (processes all classes)
    # The trigger_school node fans out to the class_flow for each class.
    # The aggregate_school node runs after all classes are processed (triggered by the last class_flow completion).
    trigger_school - "process_class" >> class_flow
    class_flow - "default" >> aggregate_school # Connect class_flow completion to aggregate_school

    school_flow = Flow(start=trigger_school) # School flow starts with triggering class processing

    return school_flow

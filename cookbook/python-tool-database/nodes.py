from brainyflow import Node, Memory # Import Memory
from tools.database import execute_sql, init_db

class InitDatabaseNode(Node):
    """Node for initializing the database"""
    
    async def exec(self, _):
        init_db()
        return "Database initialized"
        
    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        memory.db_status = exec_res # Use property access
        self.trigger("default") # Use trigger

class CreateTaskNode(Node):
    """Node for creating a new task"""
    
    async def prep(self, memory: Memory): # Use memory and add type hint
        return (
            memory.task_title if hasattr(memory, 'task_title') else "", # Use property access
            memory.task_description if hasattr(memory, 'task_description') else "" # Use property access
        )
        
    async def exec(self, inputs):
        title, description = inputs
        query = "INSERT INTO tasks (title, description) VALUES (?, ?)"
        execute_sql(query, (title, description))
        return "Task created successfully"
        
    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        memory.task_status = exec_res # Use property access
        self.trigger("default") # Use trigger

class ListTasksNode(Node):
    """Node for listing all tasks"""
    
    async def exec(self, _):
        query = "SELECT * FROM tasks"
        return execute_sql(query)
        
    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        memory.tasks = exec_res # Use property access
        self.trigger("default") # Use trigger

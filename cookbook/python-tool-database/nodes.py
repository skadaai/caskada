from brainyflow import Node
from tools.database import execute_sql, init_db

class InitDatabaseNode(Node):
    """Node for initializing the database"""
    
    async def exec(self, _):
        init_db()
        return "Database initialized"
        
    async def post(self, shared, prep_res, exec_res):
        shared["db_status"] = exec_res

class CreateTaskNode(Node):
    """Node for creating a new task"""
    
    async def prep(self, shared):
        return (
            getattr(shared, "task_title", ""),
            getattr(shared, "task_description", "")
        )
        
    async def exec(self, inputs):
        title, description = inputs
        query = "INSERT INTO tasks (title, description) VALUES (?, ?)"
        execute_sql(query, (title, description))
        return "Task created successfully"
        
    async def post(self, shared, prep_res, exec_res):
        shared["task_status"] = exec_res

class ListTasksNode(Node):
    """Node for listing all tasks"""
    
    async def exec(self, _):
        query = "SELECT * FROM tasks"
        return execute_sql(query)
        
    async def post(self, shared, prep_res, exec_res):
        shared["tasks"] = exec_res

from brainyflow import Node
from tools.search import SearchTool
from tools.parser import analyze_results
from typing import List, Dict

class SearchNode(Node):
    """Node to perform web search using SerpAPI"""
    
    async def prep(self, shared):
        return getattr(shared, "query"), getattr(shared, "num_results", 5)
        
    async def exec(self, inputs):
        query, num_results = inputs
        if not query:
            return []
            
        searcher = SearchTool()
        return searcher.search(query, num_results)
        
    async def post(self, shared, prep_res, exec_res):
        shared["search_results"] = exec_res

class AnalyzeResultsNode(Node):
    """Node to analyze search results using LLM"""
    
    async def prep(self, shared):
        return getattr(shared, "query"), getattr(shared, "search_results", [])
        
    async def exec(self, inputs):
        query, results = inputs
        if not results:
            return {
                "summary": "No search results to analyze",
                "key_points": [],
                "follow_up_queries": []
            }
            
        return analyze_results(query, results)
        
    async def post(self, shared, prep_res, exec_res):
        shared["analysis"] = exec_res
        
        # Print analysis
        print("\nSearch Analysis:")
        print("\nSummary:", exec_res["summary"])
        
        print("\nKey Points:")
        for point in exec_res["key_points"]:
            print(f"- {point}")
            
        print("\nSuggested Follow-up Queries:")
        for query in exec_res["follow_up_queries"]:
            print(f"- {query}")
            
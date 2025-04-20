from brainyflow import Node, Memory # Import Memory
from tools.search import SearchTool
from tools.parser import analyze_results
from typing import List, Dict

class SearchNode(Node):
    """Node to perform web search using SerpAPI"""

    async def prep(self, memory: Memory):
        return memory.query if hasattr(memory, 'query') else "", memory.num_results if hasattr(memory, 'num_results') else 5

    async def exec(self, inputs):
        query, num_results = inputs
        if not query:
            return []

        searcher = SearchTool()
        return searcher.search(query, num_results)

    async def post(self, memory: Memory, prep_res, exec_res):
        memory.search_results = exec_res
        self.trigger("default")

class AnalyzeResultsNode(Node):
    """Node to analyze search results using LLM"""

    async def prep(self, memory: Memory):
        return memory.query if hasattr(memory, 'query') else "", memory.search_results if hasattr(memory, 'search_results') else []

    async def exec(self, inputs):
        query, results = inputs
        if not results:
            return {
                "summary": "No search results to analyze",
                "key_points": [],
                "follow_up_queries": []
            }

        return analyze_results(query, results)

    async def post(self, memory: Memory, prep_res, exec_res):
        memory.analysis = exec_res

        # Print analysis
        print("\nSearch Analysis:")
        print("\nSummary:", exec_res.get("summary", "N/A"))

        print("\nKey Points:")
        for point in exec_res.get("key_points", []):
            print(f"- {point}")

        print("\nSuggested Follow-up Queries:")
        for query in exec_res.get("follow_up_queries", []):
            print(f"- {query}")

        self.trigger("default")

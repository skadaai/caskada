from brainyflow import Node, Memory
from tools.crawler import WebCrawler
from tools.parser import analyze_site
from typing import List, Dict

class CrawlWebsiteNode(Node):
    """Node to crawl a website and extract content"""
    
    async def prep(self, memory: Memory):
        return memory.base_url if hasattr(memory, 'base_url') else None, memory.max_pages if hasattr(memory, 'max_pages') else 10
        
    async def exec(self, inputs):
        base_url, max_pages = inputs
        if not base_url:
            return []
            
        crawler = WebCrawler(base_url, max_pages)
        return crawler.crawl()
        
    async def post(self, memory: Memory, prep_res, exec_res):
        memory.crawl_results = exec_res
        self.trigger("default")

# 1. Trigger Node (Fans out analysis work)
class TriggerAnalyzeContentNode(Node):
    """Node to trigger analysis for each crawled page"""
    
    async def prep(self, memory: Memory):
        results = memory.crawl_results if hasattr(memory, 'crawl_results') else []
        return results
        
    async def exec(self, results: list):
        # No main computation needed here, just return the count for info
        return len(results)

    async def post(self, memory: Memory, pages_to_process: list, page_count: int):
        print(f"Trigger: Triggering analysis for {page_count} pages.")
        # Initialize results list and counter in global memory
        memory.analyzed_results = [None] * page_count
        memory.remaining_analysis = page_count # Add counter
        # Trigger an 'analyze_one' action for each page
        for index, page in enumerate(pages_to_process):
            self.trigger('analyze_one', { "page_data": page, "index": index })
        # NOTE: 'aggregate_analysis' is now triggered by AnalyzeOnePageNode when the counter reaches zero.

# 2. Processor Node (Analyzes a single page)
class AnalyzeOnePageNode(Node):
    """Node to analyze a single crawled page"""
    
    async def prep(self, memory: Memory):
        # Read specific page data from local memory (passed via forkingData)
        return memory.page_data, memory.index

    async def exec(self, prep_res):
        page, index = prep_res
        # Analyze the content
        print(f"Processor: Analyzing {page.get('url', 'unknown')} (Index {index})")
        return analyze_site([page]) # analyze_site expects a list

    async def post(self, memory: Memory, prep_res, analysis_result: list):
        page, index = prep_res
        # Store individual analysis result in global memory at the correct index
        # analyze_site returns a list, take the first item
        memory.analyzed_results[index] = analysis_result[0] if analysis_result else None
        print(f"Processor: Finished analysis for {page.get('url', 'unknown')} (Index {index})")
        # Decrement counter and trigger aggregate if this is the last analysis
        memory.remaining_analysis -= 1
        if memory.remaining_analysis == 0:
            print("Processor: All analysis collected, triggering aggregate.")
            self.trigger('aggregate_analysis')
        else:
            self.trigger("default") # Continue in sequential flow (though aggregate_analysis handles the next step)

# 3. Reducer Node (Aggregates individual analysis results)
class AggregateAnalysisNode(Node):
    """Node to aggregate individual analysis results"""
    
    async def prep(self, memory: Memory):
        # Read the array of individual results (filter out None if any failed)
        results = [r for r in (memory.analyzed_results or []) if r is not None]
        return results

    async def exec(self, results: list):
        print(f"Reducer: Aggregating {len(results)} analysis results.")
        # No computation needed, just pass the aggregated list
        return results

    async def post(self, memory: Memory, prep_res, aggregated_results: list):
        # Store the final aggregated results
        memory.analyzed_results = aggregated_results
        print("Reducer: Analysis aggregation complete.")
        self.trigger("default") # Move to the next step (GenerateReportNode)


class GenerateReportNode(Node):
    """Node to generate a summary report of the analysis"""
    
    async def prep(self, memory: Memory):
        return memory.analyzed_results if hasattr(memory, 'analyzed_results') else []
        
    async def exec(self, results):
        if not results:
            return "No results to report"
            
        report = []
        report.append(f"Analysis Report\n")
        report.append(f"Total pages analyzed: {len(results)}\n")
        
        for page in results:
            report.append(f"\nPage: {page.get('url', 'N/A')}")
            report.append(f"Title: {page.get('title', 'N/A')}")
            
            analysis = page.get("analysis", {})
            report.append(f"Summary: {analysis.get('summary', 'N/A')}")
            report.append(f"Topics: {', '.join(analysis.get('topics', []))}")
            report.append(f"Content Type: {analysis.get('content_type', 'unknown')}")
            report.append("-" * 80)
            
        return "\n".join(report)
        
    async def post(self, memory: Memory, prep_res, exec_res):
        memory.report = exec_res
        print("\nReport generated:")
        print(exec_res)
        self.trigger("default")

from caskada import Node
from tools.crawler import WebCrawler
from tools.parser import analyze_site

class CrawlWebsiteNode(Node):
    """Node to crawl a website and extract content"""
    
    async def prep(self, shared):
        return getattr(shared, "base_url"), getattr(shared, "max_pages", 10)
        
    async def exec(self, inputs):
        base_url, max_pages = inputs
        if not base_url:
            return []
            
        crawler = WebCrawler(base_url, max_pages)
        return crawler.crawl()
        
    async def post(self, shared, prep_res, exec_res):
        shared["items"] = exec_res


class AnalyzeContentNode(Node):
    """Node to analyze crawled content"""
    
    async def prep(self, memory):
        return memory.index, memory.item
        
    async def exec(self, prep_res):
        return analyze_site(prep_res[1])
    
    async def post(self, shared, prep_res, exec_res):
        self.trigger("default", {"item": exec_res})
        
        
class GenerateReportNode(Node):
    """Node to generate a summary report of the analysis"""
    
    async def prep(self, shared):
        return getattr(shared, "output", [])
        
    async def exec(self, results):
        if not results:
            return "No results to report"
            
        report = []
        report.append(f"Analysis Report\n")
        report.append(f"Total pages analyzed: {len(results)}\n")
        
        for page in results:
            report.append(f"\nPage: {page['url']}")
            report.append(f"Title: {page['title']}")
            
            analysis = page.get("analysis", {})
            report.append(f"Summary: {analysis.get('summary', 'N/A')}")
            report.append(f"Topics: {', '.join(analysis.get('topics', []))}")
            report.append(f"Content Type: {analysis.get('content_type', 'unknown')}")
            report.append("-" * 80)
            
        return "\n".join(report)
        
    async def post(self, shared, prep_res, exec_res):
        shared["report"] = exec_res
        print("\nReport generated:")
        print(exec_res)

from brainyflow import Flow
from mapreduce import mapreduce
from nodes import CrawlWebsiteNode, AnalyzeContentNode, GenerateReportNode


def create_flow() -> Flow:
    """Create and configure the crawling flow
    
    Returns:
        Flow: Configured flow ready to run
    """
    # Create nodes
    crawl = CrawlWebsiteNode()
    analyze = AnalyzeContentNode()
    report = GenerateReportNode()
    
    # Connect nodes
    crawl >> mapreduce(analyze) >> report
    
    # Create flow starting with crawl
    return Flow(start=crawl)

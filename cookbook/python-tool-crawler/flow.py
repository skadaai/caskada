from brainyflow import Flow, ParallelFlow
from nodes import CrawlWebsiteNode, TriggerAnalyzeContentNode, AnalyzeOnePageNode, AggregateAnalysisNode, GenerateReportNode

def create_flow() -> Flow:
    """Create and configure the crawling flow
    
    Returns:
        Flow: Configured flow ready to run
    """
    # Create nodes
    crawl = CrawlWebsiteNode()
    trigger_analyze = TriggerAnalyzeContentNode()
    analyze_one = AnalyzeOnePageNode()
    aggregate_analysis = AggregateAnalysisNode()
    report = GenerateReportNode()
    
    # Connect nodes
    crawl >> trigger_analyze # After crawling, trigger the analysis fan-out
    trigger_analyze - "analyze_one" >> analyze_one # Trigger analysis for each page
    analyze_one - "aggregate_analysis" >> aggregate_analysis # Trigger aggregation after all analysis is done
    aggregate_analysis >> report # After aggregation, generate the report
    
    # Create flow starting with crawl
    # Use ParallelFlow for concurrent analysis of pages
    return ParallelFlow(start=crawl)

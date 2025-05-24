from typing import Dict, List
from utils.call_llm import call_llm

def analyze_content(content: Dict) -> Dict:
    """Analyze webpage content using LLM
    
    Args:
        content (Dict): Webpage content with url, title and text
        
    Returns:
        Dict: Analysis results including summary and topics
    """
    prompt = f"""
Analyze this webpage content:

Title: {content['title']}
URL: {content['url']}
Content: {content['text'][:2000]}  # Limit content length

Please provide:
1. A brief summary (2-3 sentences)
2. Main topics/keywords (up to 5)
3. Content type (article, product page, etc)

Output in YAML format:
```yaml
summary: >
    brief summary here
topics:
    - topic 1
    - topic 2
content_type: type here
```

IMPORTANT: Make sure to:
1. Use proper indentation (4 spaces) for all multi-line fields
2. Use the | character for multi-line text fields
3. Keep single-line fields without the | character
4. Your answer must be wrapped in yaml code block or it will result in an error. Do not forget to include the ```yaml sequence at the beginning and end it with ```.
"""
    
    try:
        response = call_llm(prompt)
        assert "```yaml" in response, "Response must contain yaml block"
        # Extract YAML between code fences
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        
        import yaml
        analysis = yaml.safe_load(yaml_str)
        
        # Validate required fields
        assert "summary" in analysis
        assert "topics" in analysis
        assert "content_type" in analysis
        assert isinstance(analysis["topics"], list)
        
        return analysis
        
    except Exception as e:
        print(f"Error analyzing content: {str(e)}")
        return {
            "summary": "Error analyzing content",
            "topics": [],
            "content_type": "unknown"
        }

def analyze_site(content: Dict) -> Dict:
    """Analyze all crawled pages
    
    Args:
        crawl_results (Dict): Crawled page contents
        
    Returns:
        Dict: Original content with added analysis
    """
    if content and content.get("text"):
        analysis = analyze_content(content)
        content["analysis"] = analysis
        return content
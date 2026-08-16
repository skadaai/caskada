"""Offline DuckDuckGo fixture used only by the external cookbook harness."""


class DDGS:
    def text(self, query, max_results=5):
        return [
            {
                "title": f"Cookbook result {index + 1}",
                "href": f"https://example.test/{index + 1}",
                "body": f"Offline result for {query}",
            }
            for index in range(max_results)
        ]

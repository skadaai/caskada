"""Offline SerpAPI fixture used only by the external cookbook harness."""


class GoogleSearch:
    def __init__(self, params):
        self.params = params

    def get_dict(self):
        return {
            "organic_results": [
                {
                    "title": f"Cookbook result {index + 1}",
                    "snippet": f"Offline result for {self.params['q']}",
                    "link": f"https://example.test/{index + 1}",
                }
                for index in range(self.params.get("num", 5))
            ]
        }

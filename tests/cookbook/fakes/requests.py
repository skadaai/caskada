"""Tiny requests fixture for the crawler cookbook.

The LLM SDKs used by the cookbooks use httpx, so shadowing requests here is
limited to examples that explicitly import requests.
"""


class Response:
    status_code = 200

    def __init__(self, url):
        page = "two" if url.endswith("/page-2") else "one"
        link = "" if page == "two" else '<a href="/page-2">Next page</a>'
        self.text = f"<html><title>Cookbook page {page}</title><body>Offline Caskada content.{link}</body></html>"

    def raise_for_status(self):
        return None

    def json(self):
        return {
            "web": {
                "results": [
                    {
                        "title": "Cookbook result",
                        "url": "https://example.test/result",
                        "description": "Offline result",
                    }
                ]
            }
        }


def get(url, **_kwargs):
    return Response(url)

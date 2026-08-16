"""Small protocol-level fake for cookbook tests.

It deliberately implements only the OpenAI and Anthropic endpoints used by the
cookbooks. The examples still use their real SDKs; only the network boundary is
replaced.
"""

from __future__ import annotations

import io
import json
import time
import wave
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from typing import Any, Iterator


def _flatten_content(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(_flatten_content(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(_flatten_content(item) for item in value.values())
    return ""


def response_for(prompt: str) -> str:
    """Return deterministic content matching the schema requested by a prompt."""
    lowered = prompt.lower()

    if "meticulous ai assistant" in lowered and "next_thought_needed" in lowered:
        return """```yaml
current_thinking: |
  Cookbook smoke solution
planning:
  - description: Conclusion
    status: Done
    result: Verified by the smoke fixture
next_thought_needed: false
```"""
    if "extract `name`" in lowered and "skill_indexes" in lowered:
        return """```yaml
name: Jane Cookbook
email: jane@example.test
experience:
  - title: Engineer
    company: Caskada
skill_indexes:
  - 5
  - 6
```"""
    if "create a simple outline" in lowered:
        return """```yaml
sections:
  - Why the topic matters
  - A practical example
  - What to do next
```"""
    if "containing the sql query" in lowered or "containing the corrected sql" in lowered:
        return """```yaml
sql: |
  SELECT category, COUNT(*) AS total_products FROM products GROUP BY category
```"""
    if "model context protocol" in lowered and "tool:" in lowered:
        return """```yaml
thinking: Use the addition tool.
tool: add
reason: The question asks for a sum.
parameters:
  a: 2
  b: 3
```"""
    if "evaluate if the following user query is related to travel" in lowered:
        return """```yaml
valid: true
reason: This is a travel-planning question.
```"""
    if "evaluate the following resume" in lowered and "candidate_name" in lowered:
        return """```yaml
candidate_name: Cookbook Candidate
qualifies: true
reasons:
  - Meets the education requirement
  - Has relevant experience
```"""
    if "analyze these search results" in lowered:
        return """```yaml
summary: Cookbook search summary
key_points:
  - The fake search result was parsed
  - The analysis flow completed
follow_up_queries:
  - caskada examples
  - caskada documentation
```"""
    if "analyze this webpage content" in lowered:
        return """```yaml
summary: Cookbook page summary
topics:
  - caskada
  - testing
content_type: article
```"""
    if "return strictly using the following yaml structure" in lowered and "answer: 0.123" in lowered:
        return """```yaml
thinking: The fixture produces a stable answer.
answer: 0.5
```"""
    if "### next action" in lowered or "## next action" in lowered:
        return """```yaml
thinking: The fixture has enough context to answer directly.
action: answer
reason: No external search is necessary for the smoke test.
answer: Cookbook smoke response
search_query: caskada smoke test
searchQuery: caskada smoke test
```"""
    if "directly reply a single word" in lowered:
        return "nostalgic"
    if "generate hint for" in lowered:
        return "A fond backward feeling"
    if "please translate the following markdown" in lowered:
        return "# Caskada\n\nTranslated cookbook smoke fixture.\n"

    return "Cookbook smoke response"


def _wav_bytes() -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24_000)
        wav.writeframes(b"\x00\x00" * 240)
    return buffer.getvalue()


class _Handler(BaseHTTPRequestHandler):
    server_version = "CaskadaCookbookFake/1"

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("content-length", "0"))
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        encoded = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        if self.path.endswith("/audio/speech"):
            self._json_body()
            audio = _wav_bytes()
            self.send_response(200)
            self.send_header("content-type", "audio/wav")
            self.send_header("content-length", str(len(audio)))
            self.end_headers()
            self.wfile.write(audio)
            return

        if self.path.endswith("/audio/transcriptions"):
            length = int(self.headers.get("content-length", "0"))
            self.rfile.read(length)
            self._send_json({"text": "cookbook voice fixture"})
            return

        body = self._json_body()

        if self.path.endswith("/embeddings"):
            inputs = body.get("input", "")
            count = len(inputs) if isinstance(inputs, list) else 1
            self._send_json(
                {
                    "object": "list",
                    "model": body.get("model", "fake-embedding"),
                    "data": [
                        {"object": "embedding", "index": index, "embedding": [0.1] * 8}
                        for index in range(count)
                    ],
                    "usage": {"prompt_tokens": 1, "total_tokens": 1},
                }
            )
            return

        messages = body.get("messages", [])
        prompt = _flatten_content(messages)
        content = response_for(prompt)

        if self.path.endswith("/messages"):
            blocks: list[dict[str, Any]] = []
            if body.get("thinking"):
                blocks.append({"type": "thinking", "thinking": "Fixture reasoning", "signature": "fixture"})
            blocks.append({"type": "text", "text": content})
            self._send_json(
                {
                    "id": "msg_cookbook_fixture",
                    "type": "message",
                    "role": "assistant",
                    "model": body.get("model", "fake-anthropic"),
                    "content": blocks,
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 1, "output_tokens": 1},
                }
            )
            return

        if body.get("stream"):
            chunks = [content[index : index + 12] for index in range(0, len(content), 12)]
            self.send_response(200)
            self.send_header("content-type", "text/event-stream")
            self.end_headers()
            for chunk in chunks:
                event = {
                    "id": "chatcmpl-cookbook-fixture",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": body.get("model", "fake-openai"),
                    "choices": [{"index": 0, "delta": {"content": chunk}, "finish_reason": None}],
                }
                self.wfile.write(f"data: {json.dumps(event)}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()
            return

        self._send_json(
            {
                "id": "chatcmpl-cookbook-fixture",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": body.get("model", "fake-openai"),
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": content},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            }
        )


@contextmanager
def fake_api_server() -> Iterator[str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

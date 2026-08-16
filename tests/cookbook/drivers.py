"""Special black-box contracts for cookbooks without a finite CLI entry point."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path


# Drivers live outside the staged cookbook, so explicitly give imports the same
# project-local resolution they get from `python main.py`.
sys.path.insert(0, str(Path.cwd()))


async def _a2a() -> None:
    from common.types import Message, SendTaskRequest, TaskSendParams, TaskState, TextPart
    from task_manager import CaskadaTaskManager

    request = SendTaskRequest(
        id="cookbook-request",
        params=TaskSendParams(
            id="cookbook-task",
            message=Message(role="user", parts=[TextPart(text="What is Caskada?")]),
            acceptedOutputModes=["text"],
        ),
    )
    response = await CaskadaTaskManager().on_send_task(request)
    assert response.error is None
    assert response.result is not None
    assert response.result.status.state == TaskState.COMPLETED
    assert response.result.artifacts
    assert response.result.artifacts[0].parts[0].text == "Cookbook smoke response"

    # Import the documented server entry point as well, so stale A2A server
    # dependencies and type declarations cannot escape the smoke test.
    import a2a_server  # noqa: F401

    print("A2A contract passed")


async def _fastapi_hitl() -> None:
    import server
    from flow import create_feedback_flow

    route_paths = {route.path for route in server.app.routes}
    assert {"/", "/submit", "/feedback/{task_id}", "/stream/{task_id}"} <= route_paths

    review_event = asyncio.Event()
    review_event.set()
    shared = {
        "task_input": "cookbook input",
        "processed_output": None,
        "feedback": "approved",
        "review_event": review_event,
        "sse_queue": asyncio.Queue(),
        "final_result": None,
        "task_id": "cookbook-task",
    }
    await create_feedback_flow().run(shared)
    assert shared["final_result"] == "Processed: cookbook input"
    print("FastAPI HITL contract passed")


async def _streamlit_hitl() -> None:
    expected = "Dummy rephrased text for the following input: cookbook input"
    from streamlit.testing.v1 import AppTest

    logging.getLogger("streamlit").setLevel(logging.ERROR)
    app = AppTest.from_file(str(Path.cwd() / "app.py")).run(timeout=10)
    assert not app.exception
    app.text_area[0].input("cookbook input").run(timeout=10)
    app.button[0].click().run(timeout=10)
    assert not app.exception
    assert app.session_state["stage"] == "awaiting_review"
    assert app.session_state["processed_output"] == expected

    app.button[1].click().run(timeout=10)
    assert not app.exception
    assert app.session_state["stage"] == "completed"
    assert app.session_state["final_result"] == expected

    print("Streamlit HITL contract passed")


async def _visualization() -> None:
    from async_flow import order_pipeline
    from visualize import flow_to_json, visualize_flow

    data = flow_to_json(order_pipeline)
    assert len(data["nodes"]) == 9
    assert len(data["flows"]) >= 3

    html_path = Path(
        visualize_flow(
            order_pipeline,
            "Cookbook Smoke",
            serve=False,
            output_dir="smoke-viz",
        )
    )
    json_path = html_path.with_suffix(".json")
    assert html_path.is_file()
    assert json_path.is_file()
    written = json.loads(json_path.read_text(encoding="utf-8"))
    assert len(written["nodes"]) == 9
    print("Visualization contract passed")


DRIVERS = {
    "a2a": _a2a,
    "fastapi_hitl": _fastapi_hitl,
    "streamlit_hitl": _streamlit_hitl,
    "visualization": _visualization,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("driver", choices=sorted(DRIVERS))
    args = parser.parse_args()
    asyncio.run(DRIVERS[args.driver]())


if __name__ == "__main__":
    main()

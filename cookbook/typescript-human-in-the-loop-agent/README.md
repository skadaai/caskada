# TypeScript Human In The Loop Agent Example

This example demonstrates how to build a question-answering agent using TypeScript and BrainyFlow. The agent will ask for human permission before searching the web for information and provide answers based on the search results.

## Overview

This agent demonstrates the following capabilities:
- Decision-making based on context
- Web searching for information
- Prompt user asking for permission before perform any tool calling task
- Generating comprehensive answers

### Step and Usage

```bash
# from BrainyFlow root directory
cd cookbook/typescript-human-in-the-loop-agent

cp .env.example .env # add your API key

npm install
npm run agent -- "this is your question"
```

Default question is "who is the ceo of microsoft?" if you did not provide any argument after `npm run agent`

## Features

- Performs web searches to gather information
- Collects and processes information from search results
- Answers user questions based on the gathered information

## How It Works

The agent flow comprises three nodes:

1. **DecideNode**: The core of the agent flow that determines whether it can answer the question directly or needs to search for more information.
2. **ApprovalNode**: This node will prompt user for permission before perform any tool calling.
2. **SearchNode**: Executes web searches when the DecideNode determines that more information is needed.
3. **AnswerNode**: Generates a comprehensive answer when the DecideNode determines that sufficient context is available.

The flow starts with the DecideNode, which decides whether to search (triggering ApprovalNode) or answer (triggering AnswerNode) based on the current context. This decision is made in the `post` method, which returns either "search" or "answer".

Before the application performs any tool calling task, the ApprovalNode will prompt the user and ask for permission. If the user approves (by answering "yes"), it returns a "search" action to proceed with the tool call. If the user disapproves (by answering "no"), it returns "done" and exits the app. For any other response, it returns to the DecideNode to determine the next step.

After completing a search, the SearchNode's `post` method returns results to the DecideNode via the "decide" action. This allows the DecideNode to determine whether to search again or provide a final answer when the context is sufficient.

```mermaid
graph TD
    A[DecideNode] -->|"search"| B[ApprovalNode]
    B -->|"search"| D[SearchNode]
    D -->|"decide"| A
    A -->|"answer"| C[AnswerNode]
```
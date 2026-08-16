# Cookbook smoke tests

This suite treats each cookbook directory as a standalone application. Test
logic, fake services, scripted input, and assertions stay here so the cookbook
projects remain concise examples.

Validate that every cookbook has a contract:

```bash
python tests/cookbook/runner.py validate
```

Run one project with its current environment:

```bash
python tests/cookbook/runner.py run python-batch-flow
```

Reproduce CI, including the installation instructions from the cookbook:

```bash
python tests/cookbook/runner.py run python-batch-flow --install
```

Each run uses a temporary copy with the same `cookbook/<project>` repository
layout. OpenAI and Anthropic SDKs talk to a local protocol fake, search and
audio boundaries use fixtures, and non-local network connections are blocked.
The process must exit before its timeout and satisfy the observable stdout and
file assertions in `catalog.json`.

When adding a cookbook, add its contract to `catalog.json`. CI intentionally
fails if a cookbook directory is missing from the catalog.

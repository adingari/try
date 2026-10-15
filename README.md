# Tryout (`try`)

Run a task across AI models, compare the results, and keep the evidence.

Two commands will matter:

- `try run` sends a task through one pipeline (one model, or a worker plus a supervisor) and logs what happened.
- `try eval` runs the same task through several pipelines, asks you to judge the blinded outputs, and reports quality against cost.

Specs state the expected result before anything runs, so the comparison can't be rewritten afterward.

Home: gettry.ai

## Status

Pre-alpha. There is no working command yet. What exists:

- Repo security scaffolding (see [SECURITY.md](SECURITY.md)): allowlist `.gitignore`, secret scanning, a local tripwire for personal strings, and a preflight script.

Nothing else is built.

# Security

## Reporting a problem

Use GitHub's private vulnerability reporting (the Security tab of this repo). Please don't open a public issue for a vulnerability.

## Status

Pre-alpha. The rules below are design rules for the tool. Most are not implemented yet, and the README says which are.

## Design rules

1. **Your data stays outside the repo.** Specs with real inputs, run logs, outputs, and reports live in `~/.try/`. This repo holds code, docs, and synthetic examples only.
2. **Publishing is explicit.** Nothing becomes public unless you run `try publish`, which lists every file it will copy, scans them, and asks first. Specs marked `sensitivity: private` (the default) cannot be published.
3. **Keys come from the environment or the macOS Keychain.** They never sit in a file in this repo, and they are stripped from anything the tool logs.
4. **Workers get no secrets.** Any worker with tools (shell, Blender) runs in a scoped folder with a clean environment. The harness holds the keys.
5. **Inputs are untrusted.** A document or image can contain hidden instructions, so workers that act on inputs never share an environment with credentials.
6. **No telemetry.** The tool talks to the model vendors you configure and nothing else.
7. **Few dependencies, pinned versions, official vendor SDKs only.**

## What you should know before using it

Your input files are sent to the model vendors you pick. Each has its own retention and training terms, and free tiers often permit training on your inputs. Check them before sending anything personal.

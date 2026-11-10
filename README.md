# AI Security Playground

A small, local, educational red-team demo for common security failure modes in AI-enabled applications.

It compares a deliberately vulnerable **mock email assistant** with a protected version, runs five deterministic attack scenarios, shows evidence, and exports Markdown/JSON reports.

> **Important:** This is a teaching simulation, not a general-purpose vulnerability scanner, penetration-testing product, or security certification. It uses fake data and simulated tool calls. Do not point it at production systems or use real credentials.

## What it demonstrates

1. Direct prompt injection
2. Indirect prompt injection in an email
3. System-prompt disclosure attempts
4. Unauthorized tool execution
5. Sensitive-data disclosure attempts

The protected demo illustrates application-layer controls: untrusted-input handling, server-side authorization, approval gates, and secret minimization. The examples are deterministic so the live demo works without an API key or internet access.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Quick start

```bash
uv sync
uv run streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

Run automated tests:

```bash
uv run pytest
```

No LLM API key is required. The deterministic mock is intentional: it makes the demo reproducible. An optional live-LLM adapter is deliberately out of MVP scope; see **Extending the demo** below.

## Demo flow (5–7 minutes)

1. Start the app and choose **Compare both**.
2. Click **Run security test suite**.
3. Show the vulnerable target failing selected tests and the protected target passing them.
4. Select **Vulnerable · Unauthorized tool use** and inspect the attempted `send_email` action.
5. Select the protected counterpart and show that server-side authorization denies the action.
6. Download the Markdown report.

The full 20-minute talk can add the threat model, trust boundaries, limitations, and mitigations.

## Project layout

```text
.
├── .claude/
│   └── skills/
│       └── ai-security-playground/
│           └── SKILL.md
├── app.py
├── attacks/
│   └── attack_cases.json
├── engine/
│   ├── __init__.py
│   ├── evaluator.py
│   ├── report.py
│   └── runner.py
├── target/
│   ├── __init__.py
│   └── agents.py
├── tests/
│   ├── test_agents.py
│   └── test_runner.py
├── pyproject.toml
└── README.md
```

## Safety model and honest interpretation

- The vulnerable target is intentionally unsafe and only simulates outcomes. It does not send email, access files, or make network requests.
- The protected target demonstrates controls at the application boundary. A prompt saying "do not do this" is not an authorization system.
- The evaluator uses explicit scenario outcomes, not a language model judge. This avoids nondeterministic results in a short live demo.
- A passing result means this specific simulated test was blocked. It does **not** prove the application is secure.
- Prompt injection cannot be reliably solved by prompt wording alone. Use least privilege, isolate untrusted content, validate tool arguments, enforce authorization outside the model, minimize secrets in context, require human approval for consequential actions, and log decisions.

## Claude Code skill

The project includes a Claude Code project skill at:

`.claude/skills/ai-security-playground/SKILL.md`

Claude Code can use it when working in this repository. It instructs the coding agent to inspect AI entry points, map trust boundaries, propose safe tests, and avoid destructive or unauthorized actions. The skill is advisory; it does not magically scan or secure an application.

## Extending the demo

For a follow-up iteration, you could:
- Add a real local demo target behind an explicit opt-in.
- Add a provider adapter for an LLM API, with secrets loaded from environment variables.
- Add more attack cases from a maintained test corpus.
- Add target-specific assertions for actual tool-call traces.
- Add CI execution and machine-readable SARIF output.

Keep real tests inside a disposable local environment and use synthetic data.

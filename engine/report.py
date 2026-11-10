from __future__ import annotations


def build_markdown_report(results: list[dict], ran_at: str = "") -> str:
    lines = [
        "# AI Security Playground — Test Report",
        "",
        f"- Run: {ran_at or 'Not specified'}",
        "- Scope: deterministic local simulation using synthetic data",
        "- Important: this report is educational and is not a security certification.",
        "",
        "| Target | Attack | Result | Severity | Evidence |",
        "|---|---|---|---|---|",
    ]
    for item in results:
        evidence = item["evidence"].replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {item['target']} | {item['attack']} | {item['outcome']} | "
            f"{item['severity']} | {evidence} |"
        )
    lines.extend(["", "## Recommended controls", ""])
    lines.extend(
        [
            "- Treat retrieved and user-supplied content as untrusted data.",
            "- Enforce tool authorization outside the LLM.",
            "- Require human approval for consequential actions.",
            "- Keep secrets out of model context and scope data access server-side.",
            "- Validate tool arguments and retain auditable logs.",
        ]
    )
    return "\n".join(lines) + "\n"

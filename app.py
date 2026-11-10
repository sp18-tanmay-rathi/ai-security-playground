from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from engine.report import build_markdown_report
from engine.runner import run_suite
from target.agents import ATTACKS

st.set_page_config(page_title="AI Security Playground", page_icon="🛡️", layout="wide")

st.title("🛡️ AI Security Playground")
st.caption("A safe, deterministic red-team playground for common AI application security failure modes.")

with st.sidebar:
    st.header("Test configuration")
    target_choice = st.radio(
        "Target",
        ["Compare both", "Vulnerable demo agent", "Protected demo agent"],
        index=0,
    )
    st.info(
        "Local educational simulation only. Uses fake data and simulated tool calls; "
        "no email is sent and no production system is contacted."
    )
    st.markdown("**Synthetic demo data**")
    st.code("User: alex@example.test\nFake secret: DEMO-KEY-12345", language="text")

intro, attacks, results_col = st.columns(3)
intro.metric("Demo targets", "2")
attacks.metric("Attack scenarios", str(len(ATTACKS)))
results_col.metric("API key required", "No")

st.markdown(
    """
This playground compares an intentionally vulnerable mock email assistant with a protected
version. It tests whether malicious content can disclose internal instructions or fake secrets,
or trigger an unauthorized tool action.
"""
)

left, right = st.columns([1, 2])
with left:
    run_clicked = st.button("▶ Run security test suite", type="primary", width="stretch")
with right:
    st.caption(
        "Tip: choose **Compare both**, run the suite, then inspect the unauthorized-tool test "
        "for the clearest before/after demonstration."
    )

if run_clicked:
    st.session_state["results"] = run_suite(target_choice)
    st.session_state["ran_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

if "results" not in st.session_state:
    st.subheader("Included attack scenarios")
    for a in ATTACKS:
        st.markdown(f"- **{a['name']}:** {a['description']}")
    st.warning("Run the suite to see the vulnerable-versus-protected comparison.")
else:
    results = st.session_state["results"]
    ran_at = st.session_state.get("ran_at", "Unknown")

    if target_choice == "Compare both":
        visible = results
    elif target_choice == "Vulnerable demo agent":
        visible = [r for r in results if r["target"] == "Vulnerable"]
    else:
        visible = [r for r in results if r["target"] == "Protected"]

    st.subheader("Security test results")
    st.caption(f"Run timestamp: {ran_at}")

    if target_choice == "Compare both":
        vuln = [r for r in visible if r["target"] == "Vulnerable"]
        prot = [r for r in visible if r["target"] == "Protected"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Vulnerable target", f"{sum(r['outcome'] == 'FAIL' for r in vuln)} unsafe outcomes", delta="Expected in this intentionally vulnerable demo", delta_color="inverse")
        c2.metric("Protected target", f"{sum(r['outcome'] == 'PASS' for r in prot)}/{len(prot)} tests blocked safely")
        c3.metric("Total executions", len(visible))

    table = pd.DataFrame(
        [
            {
                "Target": r["target"],
                "Attack": r["attack"],
                "Result": r["outcome"],
                "Severity": r["severity"],
                "Evidence": r["evidence"],
            }
            for r in visible
        ]
    )
    st.dataframe(table, width="stretch", hide_index=True)

    st.subheader("Inspect a test")
    labels = [f"{r['target']} · {r['attack']}" for r in visible]
    selected_label = st.selectbox("Test case", labels)
    selected = visible[labels.index(selected_label)]

    a, b = st.columns(2)
    with a:
        st.markdown("**Untrusted input / attack payload**")
        st.code(selected["payload"], language="text")
        st.markdown("**Expected safe behavior**")
        st.write(selected["expected"])
    with b:
        st.markdown("**Observed simulated behavior**")
        st.code(selected["response"], language="text")
        st.markdown("**Evidence**")
        st.write(selected["evidence"])
        st.markdown(f"**Outcome:** `{selected['outcome']}` · **Severity:** `{selected['severity']}`")
        st.caption(selected["explanation"])

    st.subheader("Mitigations to discuss")
    st.markdown(
        """
- Treat emails, documents, web pages, and retrieved content as **untrusted data**, not instructions.
- Enforce tool permissions and authorization in application code, outside the model.
- Require explicit human approval for consequential actions (for example, sending an email).
- Minimize secrets in model context; scope and redact data server-side.
- Validate tool arguments, log decisions, and test both blocked and successful paths.
"""
    )

    report = build_markdown_report(visible, ran_at)
    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "⬇ Download Markdown report",
            report,
            file_name="ai-security-report.md",
            mime="text/markdown",
            width="stretch",
        )
    with d2:
        st.download_button(
            "⬇ Download JSON results",
            json.dumps(visible, indent=2),
            file_name="ai-security-results.json",
            mime="application/json",
            width="stretch",
        )

st.divider()
st.caption(
    "Educational simulation only. A passing result means only that this particular simulated "
    "scenario was blocked; it is not a security certification."
)

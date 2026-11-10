from __future__ import annotations

from engine.evaluator import evaluate
from target.agents import ATTACKS, run_agent


def run_suite(target_choice: str = "Compare both") -> list[dict]:
    """Run the fixed attack corpus against one or both local mock targets."""
    targets = {
        "Compare both": ["Vulnerable", "Protected"],
        "Vulnerable demo agent": ["Vulnerable"],
        "Protected demo agent": ["Protected"],
    }.get(target_choice)
    if targets is None:
        raise ValueError(f"Unknown target choice: {target_choice}")

    results = []
    for target_name in targets:
        for attack in ATTACKS:
            observation = run_agent(target_name, attack)
            evaluated = evaluate(observation)
            results.append(
                {
                    "target": target_name,
                    "attack": attack["name"],
                    "payload": attack["payload"],
                    "expected": attack["safe_expected"],
                    "response": observation["response"],
                    "evidence": observation["evidence"],
                    "unsafe": observation["unsafe"],
                    "outcome": evaluated["outcome"],
                    "severity": evaluated["severity"],
                    "explanation": observation["explanation"],
                }
            )
    return results

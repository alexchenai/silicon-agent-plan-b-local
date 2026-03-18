"""Orchestrator agent for Silicon-Agent Plan B (Local stack via Ollama)."""

import requests
from dataclasses import dataclass, field
from typing import Literal

OLLAMA_URL = "http://localhost:11434"
ORCHESTRATOR_MODEL = "mistral:7b-instruct-q4_K_M"

ORCHESTRATOR_SYSTEM = """You are the Silicon-Agent Orchestrator managing autonomous RTL design.
You manage DesignState and dispatch specialist agents. Never write RTL yourself.
Priority: fix FAILING blocks first. Max 8 retries per block then escalate."""


@dataclass
class DesignState:
    project_phase: Literal["spec", "rtl", "verify", "pnr"] = "spec"
    block_registry: dict = field(default_factory=dict)
    spec_context: list = field(default_factory=list)
    rtl_artifacts: dict = field(default_factory=dict)
    error_log: list = field(default_factory=list)
    iteration_counts: dict = field(default_factory=dict)


def orchestrate_local(state: DesignState, target_block: str) -> dict:
    """Run orchestration using local Mistral model."""
    response = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": ORCHESTRATOR_MODEL,
        "system": ORCHESTRATOR_SYSTEM,
        "prompt": f"State: {state}. Target: {target_block}. Next action?",
        "stream": False
    })
    return {"decision": response.json().get("response", ""), "state": state}

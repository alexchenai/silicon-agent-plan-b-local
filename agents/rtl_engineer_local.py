"""RTL Engineer agent using DeepSeek-Coder-33B via Ollama."""

import requests

OLLAMA_URL = "http://localhost:11434"
RTL_MODEL = "deepseek-coder:33b-instruct-q4_K_M"

RTL_SYSTEM = """You are a senior RTL Engineer. Generate synthesizable SystemVerilog-2017.
Rules: always_ff for sequential, always_comb for combinational, AXI-Stream interfaces,
active-low reset (rst_n), non-blocking assignments (<=) in sequential blocks only.
Target: Yosys/OpenLane synthesis at 100 MHz. Output ONLY the SystemVerilog file."""


def generate_rtl_local(spec_description: str, interface_defs: str, error_context: str = "") -> str:
    """Generate SystemVerilog using local DeepSeek-Coder model."""
    prompt = f"Specification:\n{spec_description}\n\nInterfaces:\n{interface_defs}"
    if error_context:
        prompt += f"\n\nFix these errors:\n{error_context}"
    
    response = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": RTL_MODEL,
        "system": RTL_SYSTEM,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 8192, "temperature": 0.1}
    })
    return response.json().get("response", "")

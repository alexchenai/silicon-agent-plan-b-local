"""Download required Ollama models for Plan B local stack."""

import subprocess
import sys

MODELS = [
    "mistral:7b-instruct-q4_K_M",
    "deepseek-coder:33b-instruct-q4_K_M",
    "codellama:13b-code-q4_K_M",
]


def download_model(model_name: str):
    print(f"Pulling {model_name}...")
    result = subprocess.run(["ollama", "pull", model_name], capture_output=False)
    if result.returncode != 0:
        print(f"Failed to pull {model_name}")
        sys.exit(1)
    print(f"Successfully downloaded {model_name}")


if __name__ == "__main__":
    print("Downloading models for Silicon-Agent Plan B...")
    print(f"Required disk space: ~40 GB")
    print(f"Required VRAM: 24 GB (RTX 4090 or equivalent)")
    print()
    
    for model in MODELS:
        download_model(model)
    
    print("\nAll models downloaded. Run main.py to start the workflow.")

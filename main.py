"""Entry point for Silicon-Agent Plan B local sovereign swarm."""

import argparse
from dotenv import load_dotenv
from agents.orchestrator_local import DesignState, orchestrate_local
from agents.rtl_engineer_local import generate_rtl_local

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Silicon-Agent Plan B: Local Sovereign Stack")
    parser.add_argument("--target", required=True, help="Target block name")
    parser.add_argument("--spec", required=True, help="3GPP spec reference")
    parser.add_argument("--max-retries", type=int, default=8, help="Max retries per block")
    args = parser.parse_args()
    
    print(f"Starting Silicon-Agent Plan B (local) for block: {args.target}")
    print(f"Spec reference: {args.spec}")
    print(f"All inference running locally via Ollama - no cloud API calls")
    
    state = DesignState(
        project_phase="spec",
        block_registry={args.target: "PENDING"},
        spec_context=[args.spec]
    )
    
    for iteration in range(args.max_retries):
        result = orchestrate_local(state, args.target)
        print(f"Iteration {iteration + 1}: {result['decision'][:100]}...")
        
        if state.block_registry.get(args.target) == "PASSED":
            print("Block design complete!")
            break
    else:
        print("Max retries reached. Check error log.")


if __name__ == "__main__":
    main()

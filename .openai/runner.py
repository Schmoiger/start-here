import os
import json
import httpx
from pathlib import Path

def run_agent(agent_name: str, user_prompt: str):
    base_dir = Path(__file__).parent
    prompt_file = base_dir / "prompts" / f"{agent_name}.txt"
    if not prompt_file.exists():
        raise FileNotFoundError(f"System prompt for {agent_name} not found.")
        
    system_prompt = prompt_file.read_text()
    
    tools_file = base_dir / "tools.json"
    tools = []
    if tools_file.exists():
        tools = json.loads(tools_file.read_text())
        
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o", # Can be resolved via models.yaml
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "tools": tools
    }
    
    response = httpx.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60.0)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        res = run_agent(sys.argv[1], sys.argv[2])
        print(json.dumps(res, indent=2))
    else:
        print("Usage: python runner.py <agent_name> <user_prompt>")

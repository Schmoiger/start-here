import json
from pathlib import Path
from typing import Any

from context.scripts.generators.adapters.core.models import CanonicalAgent


def generate_system_prompts(context: dict[str, Any], output_dir: Path) -> None:
    """Translates canonical agents into OpenAI system prompts."""
    agents: dict[str, CanonicalAgent] = context.get("agents", {})
    prompts_dir = output_dir / ".openai" / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    
    for agent_name, agent in agents.items():
        prompt_path = prompts_dir / f"{agent_name}.txt"
        
        lines = [
            f"You are {agent.name.replace('-', ' ').title()}.",
            f"Role: {agent.description}",
            ""
        ]
        
        if agent.standards:
            lines.append("STANDARDS:")
            for std in agent.standards:
                lines.append(f"- {std}")
            lines.append("")
            
        if agent.rules:
            lines.append("RULES:")
            for rule in agent.rules:
                lines.append(f"- {rule}")
            lines.append("")
            
        prompt_path.write_text("\n".join(lines))


def generate_tool_schemas(context: dict[str, Any], output_dir: Path) -> None:
    """Generates OpenAI Function Calling JSON schemas for agent tools."""
    tools_dir = output_dir / ".openai"
    tools_dir.mkdir(parents=True, exist_ok=True)
    
    # Based on feedback: use models.yaml as the central registry (stubbed here)
    schema = {
        "type": "function",
        "function": {
            "name": "registry_lookup",
            "description": "Looks up models and tools from models.yaml",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
    
    tools_path = tools_dir / "tools.json"
    tools_path.write_text(json.dumps([schema], indent=2))


def generate_runner_harness(output_dir: Path) -> None:
    """Generates a lightweight Python execution harness using httpx."""
    runner_dir = output_dir / ".openai"
    runner_dir.mkdir(parents=True, exist_ok=True)
    runner_path = runner_dir / "runner.py"
    
    content = '''import os
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
'''
    runner_path.write_text(content)

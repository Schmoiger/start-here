# Framework Adapters

Agent definitions in this directory are markdown files designed to work across multiple AI frameworks. This guide shows how to adapt them for different orchestration systems.

## Agent Definition Format

All agents use this structure:

```markdown
---
name: agent-name
description: Brief role description
model: opus|sonnet|haiku
allowed_tools:
  - Write
  - Edit
  - Read
standards:
  - tech-standards.md
rules:
  - conventional-commits.mdc
---

You are a [role]. Your job is to [responsibility].

## Workflow
1. Read standards listed above
2. Follow rules in frontmatter
3. Execute task
...
```

The frontmatter lists Claude Code-specific tools, but the core agent logic (system prompt body) is framework-agnostic.

---

## Claude Code (Native)

**Method**: Task tool spawns agents with prompt injection

**Usage**:
```python
# Orchestrator spawns agent
Task(
    subagent_type="python-coder",
    prompt="Read context/agents/python-coder.md\n\nThen: implement authentication"
)
```

**What happens**:
1. Task tool starts new agent session
2. Agent reads definition file (standards, rules, system prompt)
3. Agent executes task with tools from `allowed_tools`

**Tool mapping**: Direct (Write → Write, Edit → Edit, etc.)

---

## LangGraph

**Method**: Load agent markdown as node system message

**Usage**:
```python
from langgraph.graph import StateGraph
from pathlib import Path

def load_agent(name: str) -> str:
    """Load agent definition from context/agents/{name}.md"""
    return Path(f"context/agents/{name}.md").read_text()

def python_coder_node(state):
    agent_prompt = load_agent("python-coder")
    task_prompt = f"{agent_prompt}\n\n## Task\n\n{state['task']}"

    # Call LLM with agent prompt + task
    response = llm.invoke(task_prompt)
    return {"output": response}

# Build graph
workflow = StateGraph(State)
workflow.add_node("python-coder", python_coder_node)
workflow.add_edge("start", "python-coder")
```

**Tool mapping**:
```python
# Map allowed_tools to LangGraph tools
tool_map = {
    "Write": write_file_tool,
    "Edit": edit_file_tool,
    "Read": read_file_tool,
    "Glob": glob_files_tool,
    "Grep": grep_content_tool,
    "Bash": subprocess_tool
}

# Extract tools from frontmatter and bind to LLM
import yaml
frontmatter = yaml.safe_load(agent_def.split("---")[1])
tools = [tool_map[t] for t in frontmatter["allowed_tools"]]
llm_with_tools = llm.bind_tools(tools)
```

---

## CrewAI

**Method**: Load agent markdown as backstory

**Usage**:
```python
from crewai import Agent, Task, Crew
from pathlib import Path

def load_agent(name: str) -> str:
    return Path(f"context/agents/{name}.md").read_text()

# Create agent
python_coder = Agent(
    role="Python Developer",
    goal="Write clean, tested Python code following standards",
    backstory=load_agent("python-coder"),
    tools=[WriteFileTool(), EditFileTool(), ReadFileTool()],
    verbose=True
)

# Create task
task = Task(
    description="Implement user authentication with FastAPI",
    agent=python_coder,
    expected_output="Working auth endpoints with tests"
)

# Create crew
crew = Crew(agents=[python_coder], tasks=[task])
result = crew.kickoff()
```

**Tool mapping**:
```python
from crewai_tools import FileWriterTool, FileReadTool

# Map allowed_tools to CrewAI tools
tool_map = {
    "Write": FileWriterTool(),
    "Edit": FileWriterTool(),  # CrewAI uses same tool for write/edit
    "Read": FileReadTool(),
    "Glob": DirectorySearchTool(),
    "Grep": FileSearchTool()
}
```

---

## AutoGen

**Method**: Load agent markdown as system_message

**Usage**:
```python
from autogen import AssistantAgent, UserProxyAgent
from pathlib import Path

def load_agent(name: str) -> str:
    return Path(f"context/agents/{name}.md").read_text()

# Create agent
python_coder = AssistantAgent(
    name="python_coder",
    system_message=load_agent("python-coder"),
    llm_config={
        "model": "gpt-4",
        "functions": [write_file, edit_file, read_file]
    }
)

# Create user proxy
user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "workspace"}
)

# Start conversation
user_proxy.initiate_chat(
    python_coder,
    message="Implement user authentication with FastAPI"
)
```

**Tool mapping**:
```python
# Define functions matching OpenAI function calling spec
def write_file(path: str, content: str) -> str:
    """Write content to file"""
    Path(path).write_text(content)
    return f"Wrote {len(content)} chars to {path}"

# Register with agent
llm_config = {
    "functions": [
        {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                }
            }
        }
    ]
}
```

---

## Cursor IDE

**Method**: Copy agent markdown to `.cursorrules`

**Usage**:
```bash
# Copy agent definition to Cursor context
cp context/agents/python-coder.md .cursorrules

# Or create .cursor/rules/python-coder.md
mkdir -p .cursor/rules
cp context/agents/python-coder.md .cursor/rules/
```

**Note**: Cursor is single-agent. User manually switches between agents by changing `.cursorrules` content.

**Tool mapping**: Built-in (Cursor has native file operations)

---

## Aider

**Method**: Merge agent definition into system prompt

**Usage**:
```bash
# Aider doesn't support multi-agent natively
# Load agent as additional context via --read flag
aider --read context/agents/python-coder.md \
      --read context/standards/tech-standards.md \
      --message "Implement user authentication"

# Or use architect mode for design agents
aider --architect \
      --read context/agents/solution-architect.md
```

**Tool mapping**: Built-in (Aider has git-aware file operations)

---

## Continue.dev

**Method**: Load agent as slash command or context provider

**Usage** (in `~/.continue/config.json`):
```json
{
  "slashCommands": [
    {
      "name": "python",
      "description": "Python coding mode",
      "prompt": "{{ file:context/agents/python-coder.md }}\n\nTask: {{input}}"
    },
    {
      "name": "architect",
      "description": "Architecture design mode",
      "prompt": "{{ file:context/agents/solution-architect.md }}\n\nTask: {{input}}"
    }
  ]
}
```

**Usage in IDE**:
```
/python Implement user authentication with FastAPI
```

**Tool mapping**: Built-in (Continue has file operations)

---

## Windsurf

**Method**: Similar to Cursor (context files)

**Usage**:
```bash
# Copy to Windsurf rules
cp context/agents/python-coder.md .windsurfrules
```

**Tool mapping**: Built-in

---

## Tool Mapping Reference

Claude Code tools → Framework equivalents:

| Claude Tool | LangGraph | CrewAI | AutoGen | Cursor/Aider/Continue |
|-------------|-----------|--------|---------|----------------------|
| **Write** | `write_file()` | `FileWriterTool()` | `write_file()` func | Built-in |
| **Edit** | `edit_file()` | `FileWriterTool()` | `edit_file()` func | Built-in |
| **Read** | `read_file()` | `FileReadTool()` | `read_file()` func | Built-in |
| **Glob** | `glob.glob()` | `DirectorySearchTool()` | `glob()` func | Built-in |
| **Grep** | `grep_content()` | `FileSearchTool()` | `grep()` func | Built-in |
| **Bash** | `subprocess.run()` | `ShellTool()` | `execute_code()` | Built-in |

**Note**: For frameworks without native tools, implement Python functions and register them with the LLM.

---

## Handling Frontmatter

Most frameworks don't parse YAML frontmatter automatically. Two approaches:

### Option 1: Strip Frontmatter
```python
def load_agent_without_frontmatter(name: str) -> str:
    content = Path(f"context/agents/{name}.md").read_text()
    # Remove YAML frontmatter (between --- markers)
    parts = content.split("---")
    return "---".join(parts[2:]) if len(parts) > 2 else content
```

### Option 2: Parse Frontmatter for Metadata
```python
import yaml

def load_agent_with_metadata(name: str):
    content = Path(f"context/agents/{name}.md").read_text()
    parts = content.split("---")

    if len(parts) < 3:
        return {"prompt": content, "metadata": {}}

    metadata = yaml.safe_load(parts[1])
    prompt = "---".join(parts[2:])

    return {
        "prompt": prompt,
        "metadata": metadata,
        "model": metadata.get("model", "sonnet"),
        "tools": metadata.get("allowed_tools", [])
    }
```

---

## Best Practices

1. **Keep agent definitions framework-agnostic**: System prompt should work across all frameworks
2. **Tool mapping is framework-specific**: Implement tool adapters for each framework
3. **Frontmatter is optional metadata**: Core logic is in markdown body
4. **Standards/rules are portable**: Load referenced files the same way as agent definitions

## Questions?

See:
- `context/agents/TEMPLATE.md` - Template for creating new agents
- `context/README.md` - Complete context system documentation
- Root `README.md` - Deployment guide

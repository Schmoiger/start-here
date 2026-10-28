from dataclasses import dataclass, field


@dataclass
class CanonicalRule:
    name: str
    key_points: str


@dataclass
class CanonicalStandard:
    name: str
    path: str


@dataclass
class CanonicalSkill:
    name: str
    description: str
    globs: list[str] = field(default_factory=list)
    body: str = ""


@dataclass
class CanonicalAgent:
    name: str
    description: str
    model: str
    #: Tool names only. The loader normalises the frontmatter `tools:` form
    #: (plain strings, `name: purpose` mappings, or a top-level mapping) to
    #: a flat list of names — see context/templates/agent-template.md.
    mcp_tools: list[str] = field(default_factory=list)
    standards: list[str] = field(default_factory=list)
    rules: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)


@dataclass
class CanonicalPersona:
    name: str
    description: str
    traits: list[str] = field(default_factory=list)


@dataclass
class Phase:
    id: str
    name: str
    agents: list[str]
    validation: list[str] = field(default_factory=list)


@dataclass
class WorkflowDAG:
    name: str
    description: str
    phases: list[Phase] = field(default_factory=list)

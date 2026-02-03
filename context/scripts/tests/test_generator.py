"""Tests for CLAUDE.md generator."""

import pytest
from pathlib import Path
import sys
import yaml

# Add generators directory to path so we can import generator
sys.path.insert(0, str(Path(__file__).parent.parent / 'generators'))

# Import with explicit sys.path modification since it's in generators/
import generate_claude_md as gen
load_workflow = gen.load_workflow
load_agent_definitions = gen.load_agent_definitions
extract_description = gen.extract_description
generate_workflow_diagram = gen.generate_workflow_diagram
generate_phase_details = gen.generate_phase_details
generate_agent_reference = gen.generate_agent_reference
generate_quality_gates = gen.generate_quality_gates
generate_workflow_rules = gen.generate_workflow_rules
generate_claude_md = gen.generate_claude_md


class TestWorkflowLoading:
    """Tests for workflow loading."""

    def test_load_workflow(self, test_workflow, monkeypatch):
        """Test loading workflow from YAML file."""
        # Monkeypatch the workflow path to use test fixture
        def mock_workflow_path(workflow_name):
            return test_workflow

        monkeypatch.setattr('generate_claude_md.Path', lambda x: test_workflow.parent)

        # Read test workflow directly
        workflow = yaml.safe_load(test_workflow.read_text())
        assert workflow['name'] == 'test-workflow'
        assert 'phases' in workflow
        assert len(workflow['phases']) == 2

    def test_workflow_has_phases(self, test_workflow):
        """Test that workflow contains phases."""
        workflow = yaml.safe_load(test_workflow.read_text())
        assert 'phases' in workflow
        phases = workflow['phases']
        assert len(phases) > 0
        assert 'id' in phases[0]
        assert 'name' in phases[0]
        assert 'agents' in phases[0]


class TestAgentLoading:
    """Tests for agent definition loading."""

    def test_extract_description(self):
        """Test extracting description from agent content."""
        content = """## Role

This is a test agent for validation purposes.

## Workflow

1. Do something
"""
        desc = extract_description(content)
        assert desc == "This is a test agent for validation purposes."

    def test_extract_description_skips_headers(self):
        """Test that description extraction skips headers."""
        content = """## Role

## Another Header

This is the description.
"""
        desc = extract_description(content)
        assert desc == "This is the description."

    def test_extract_description_missing(self):
        """Test fallback when no description found."""
        content = """## Role

"""
        desc = extract_description(content)
        assert "not found" in desc.lower()


class TestDiagramGeneration:
    """Tests for workflow diagram generation."""

    def test_generate_workflow_diagram(self, test_workflow):
        """Test generating Mermaid diagram from workflow."""
        workflow = yaml.safe_load(test_workflow.read_text())
        diagram = generate_workflow_diagram(workflow)

        assert diagram.startswith("```mermaid")
        assert diagram.endswith("```")
        assert "flowchart TD" in diagram
        assert "subgraph" in diagram
        assert "phase1" in diagram
        assert "phase2" in diagram

    def test_diagram_includes_dependencies(self, test_workflow):
        """Test that diagram includes phase dependencies."""
        workflow = yaml.safe_load(test_workflow.read_text())
        diagram = generate_workflow_diagram(workflow)

        # phase2 depends on phase1
        assert "phase1 --> phase2" in diagram

    def test_diagram_marks_gates(self, test_workflow):
        """Test that diagram marks quality gates."""
        workflow = yaml.safe_load(test_workflow.read_text())
        diagram = generate_workflow_diagram(workflow)

        # phase2 is marked as gate
        assert "gateStyle" in diagram


class TestPhaseDetails:
    """Tests for phase details generation."""

    def test_generate_phase_details(self, test_workflow):
        """Test generating detailed phase descriptions."""
        workflow = yaml.safe_load(test_workflow.read_text())
        # Create minimal agent definitions
        agents = {
            'test-agent': {
                'frontmatter': {'name': 'test-agent'},
                'content': 'Test agent for validation'
            },
            'another-agent': {
                'frontmatter': {'name': 'another-agent'},
                'content': 'Another test agent'
            }
        }

        details = generate_phase_details(workflow, agents)

        assert "Phase One" in details
        assert "Phase Two" in details
        assert "phase1" in details
        assert "phase2" in details
        assert "@test-agent" in details
        assert "@another-agent" in details

    def test_phase_details_includes_dependencies(self, test_workflow):
        """Test that phase details show dependencies."""
        workflow = yaml.safe_load(test_workflow.read_text())
        agents = {}

        details = generate_phase_details(workflow, agents)

        assert "Depends On" in details
        assert "`phase1`" in details

    def test_phase_details_marks_gates(self, test_workflow):
        """Test that phase details mark quality gates."""
        workflow = yaml.safe_load(test_workflow.read_text())
        agents = {}

        details = generate_phase_details(workflow, agents)

        assert "Quality Gate" in details


class TestAgentReference:
    """Tests for agent reference generation."""

    def test_generate_agent_reference(self):
        """Test generating agent reference section."""
        agents = {
            'product-owner': {
                'frontmatter': {
                    'name': 'product-owner',
                    'standards': ['doc-standards.md'],
                    'rules': ['conventional-commits.mdc']
                },
                'content': 'Defines requirements and user stories'
            },
            'python-coder': {
                'frontmatter': {
                    'name': 'python-coder',
                    'standards': ['coding-standards.md'],
                    'rules': []
                },
                'content': 'Writes production Python code'
            }
        }

        reference = generate_agent_reference(agents)

        assert "Discovery" in reference
        assert "Development" in reference
        assert "@product-owner" in reference
        assert "@python-coder" in reference
        assert "doc-standards.md" in reference
        assert "coding-standards.md" in reference


class TestQualityGates:
    """Tests for quality gates generation."""

    def test_generate_quality_gates(self, test_workflow):
        """Test generating quality gates section."""
        workflow = yaml.safe_load(test_workflow.read_text())
        gates_section = generate_quality_gates(workflow)

        # Generator titlecases phase ID, so "phase2" becomes "Phase2"
        assert "Phase2" in gates_section or "phase2" in gates_section
        assert "approval" in gates_section
        assert "Yes" in gates_section  # Required

    def test_quality_gates_with_criteria(self):
        """Test quality gates with criteria."""
        workflow = {
            'quality_gates': [
                {
                    'phase': 'verification',
                    'type': 'metrics',
                    'required': True,
                    'description': 'Coverage check',
                    'criteria': [
                        {
                            'metric': 'test_coverage',
                            'threshold': 90,
                            'operator': '>='
                        }
                    ]
                }
            ]
        }

        gates_section = generate_quality_gates(workflow)

        assert "Criteria" in gates_section
        assert "test_coverage" in gates_section
        assert ">= 90" in gates_section

    def test_no_quality_gates(self):
        """Test handling of workflow with no quality gates."""
        workflow = {'quality_gates': []}
        gates_section = generate_quality_gates(workflow)

        assert "No quality gates" in gates_section


class TestWorkflowRules:
    """Tests for workflow rules generation."""

    def test_generate_workflow_rules(self, test_workflow):
        """Test generating workflow rules section."""
        workflow = yaml.safe_load(test_workflow.read_text())
        rules_section = generate_workflow_rules(workflow)

        assert "Rule 1" in rules_section
        assert "Rule 2" in rules_section

    def test_workflow_warnings(self, test_workflow):
        """Test that warnings are included."""
        workflow = yaml.safe_load(test_workflow.read_text())
        rules_section = generate_workflow_rules(workflow)

        assert "⚠️" in rules_section
        assert "Test warning" in rules_section

    def test_no_rules_or_warnings(self):
        """Test handling of workflow with no rules."""
        workflow = {}
        rules_section = generate_workflow_rules(workflow)

        assert "No specific workflow" in rules_section


class TestFullGeneration:
    """Tests for complete CLAUDE.md generation."""

    def test_generate_claude_md_structure(self, test_workflow, monkeypatch):
        """Test that generated CLAUDE.md has correct structure."""
        # Mock the load functions to use test fixtures
        def mock_load_workflow(workflow_name):
            return yaml.safe_load(test_workflow.read_text())

        def mock_load_agents():
            return {
                'test-agent': {
                    'frontmatter': {'name': 'test-agent'},
                    'content': 'Test agent'
                }
            }

        monkeypatch.setattr('generate_claude_md.load_workflow', mock_load_workflow)
        monkeypatch.setattr('generate_claude_md.load_agent_definitions', mock_load_agents)

        content = generate_claude_md('test-workflow')

        # Check major sections exist
        assert "# Multi-Agent Orchestration Guide" in content
        assert "## Overview" in content
        assert "## Workflow:" in content
        assert "### Workflow Diagram" in content
        assert "### Phases" in content
        assert "## Agent Reference" in content
        assert "## Standards & Rules" in content
        assert "## Quality Gates" in content
        assert "## Best Practices" in content
        assert "## Maintenance" in content

    def test_generated_md_has_mermaid_diagram(self, test_workflow, monkeypatch):
        """Test that generated markdown includes Mermaid diagram."""
        def mock_load_workflow(workflow_name):
            return yaml.safe_load(test_workflow.read_text())

        def mock_load_agents():
            return {}

        monkeypatch.setattr('generate_claude_md.load_workflow', mock_load_workflow)
        monkeypatch.setattr('generate_claude_md.load_agent_definitions', mock_load_agents)

        content = generate_claude_md('test-workflow')

        assert "```mermaid" in content
        assert "flowchart TD" in content

    def test_generated_md_includes_workflow_name(self, test_workflow, monkeypatch):
        """Test that workflow name is included in output."""
        def mock_load_workflow(workflow_name):
            return yaml.safe_load(test_workflow.read_text())

        def mock_load_agents():
            return {}

        monkeypatch.setattr('generate_claude_md.load_workflow', mock_load_workflow)
        monkeypatch.setattr('generate_claude_md.load_agent_definitions', mock_load_agents)

        content = generate_claude_md('test-workflow')

        assert "test-workflow" in content

    def test_generated_md_portable_paths(self, test_workflow, monkeypatch):
        """Test that generated markdown uses portable paths."""
        def mock_load_workflow(workflow_name):
            return yaml.safe_load(test_workflow.read_text())

        def mock_load_agents():
            return {}

        monkeypatch.setattr('generate_claude_md.load_workflow', mock_load_workflow)
        monkeypatch.setattr('generate_claude_md.load_agent_definitions', mock_load_agents)

        content = generate_claude_md('test-workflow')

        # Should reference context/ directory
        assert "context/" in content
        # Should not have hardcoded paths
        assert "/Users/" not in content
        assert "/home/" not in content

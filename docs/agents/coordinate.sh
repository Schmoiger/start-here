#!/usr/bin/env bash
# Agent Coordinator for multi-agent workflow
# Usage: ./coordinate.sh "python-coder" "build a validation function"
# Or manually invoke agents in Claude Code with @agent-name syntax

set -e

AGENT_NAME="${1:-orchestrator}"
TASK_DESCRIPTION="${2:-}"

# Colour codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Colour

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if artifacts directory exists
ensure_artifacts_dir() {
    if [ ! -d "./artifacts" ]; then
        log_warning "Creating ./artifacts directory"
        mkdir -p ./artifacts
    fi
}

# Create subdirectories for each agent's work
init_agent_dirs() {
    ensure_artifacts_dir
    
    log_info "Initialising agent directories..."
    mkdir -p ./artifacts/python
    mkdir -p ./artifacts/typescript
    mkdir -p ./artifacts/test-results
    mkdir -p ./artifacts/ui-test-results/screenshots
    mkdir -p ./artifacts/security-audit
    mkdir -p ./artifacts/gcp/terraform
    
    # Create requirements template if not present
    if [ ! -f "./artifacts/requirements.md" ]; then
        cat > ./artifacts/requirements.md << 'EOF'
# Project Requirements

## Overview
Define your project requirements, acceptance criteria, and constraints here.

## Acceptance Criteria
- [ ] Component 1
- [ ] Component 2

## Technical Constraints
- Python 3.10+
- TypeScript with strict mode
- pytest for testing
- GCP Cloud Run for hosting

## API Contract
See ./artifacts/api-contract.json for interface definitions.
EOF
        log_success "Created requirements.md template"
    fi
}

# List available agents
list_agents() {
    log_info "Available agents:"
    echo "  - python-coder       : Write production Python code"
    echo "  - typescript-coder   : Write production TypeScript"
    echo "  - functional-tester  : Write and run tests"
    echo "  - ui-tester          : Test UI with Chrome DevTools"
    echo "  - security-tester    : Security audit and threat modelling"
    echo "  - gcp-devops         : Configure GCP infrastructure"
    echo ""
    echo "Usage in Claude Code:"
    echo "  @python-coder write a function that validates emails"
    echo "  @typescript-coder create an API client for the backend"
    echo "  @functional-tester write tests for the email validator"
}

# Show coordinator workflow
show_workflow() {
    cat << 'EOF'
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT COORDINATION FLOW                       │
└─────────────────────────────────────────────────────────────────┘

1. DESIGN PHASE
   ├─ Create ./artifacts/requirements.md with project specs
   └─ Define API contracts in ./artifacts/api-contract.json

2. DEVELOPMENT PHASE
   ├─ @python-coder creates backend modules
   └─ @typescript-coder creates frontend code

3. TESTING PHASE
   ├─ @functional-tester writes pytest + vitest tests
   ├─ @ui-tester tests user workflows
   └─ All tests write results to ./artifacts/test-results/

4. SECURITY PHASE
   └─ @security-tester performs threat modelling and audits

5. INFRASTRUCTURE PHASE
   └─ @gcp-devops creates Terraform configurations

┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT SHARING via ./artifacts/              │
└─────────────────────────────────────────────────────────────────┘

All agents read/write to ./artifacts/ for context sharing:

./artifacts/
├─ requirements.md         (shared spec)
├─ api-contract.json       (interface definitions)
├─ python/                 (Python code)
│  ├─ *.py
│  ├─ requirements.txt
│  └─ README.md
├─ typescript/             (TypeScript code)
│  ├─ *.ts
│  ├─ package.json
│  └─ README.md
├─ test-results/           (test outputs)
├─ ui-test-results/        (UI test screenshots & logs)
├─ security-audit/         (findings, threat model)
└─ gcp/terraform/          (infrastructure-as-code)

EOF
}

# Main entry point
main() {
    case "${AGENT_NAME}" in
        list|--list|-l)
            init_agent_dirs
            list_agents
            ;;
        workflow|--workflow|-w)
            show_workflow
            ;;
        init|--init|-i)
            init_agent_dirs
            log_success "Agent environment initialised"
            ;;
        *)
            if [ -z "$TASK_DESCRIPTION" ]; then
                echo "Agent Coordinator - Multi-agent orchestration for Claude Code"
                echo ""
                echo "Usage:"
                echo "  $0 list              - List available agents"
                echo "  $0 init              - Initialise agent directories"
                echo "  $0 workflow          - Show coordination workflow"
                echo ""
                echo "In Claude Code, invoke agents directly:"
                echo "  @python-coder write a validation function"
                echo "  @typescript-coder create an API client"
                echo ""
                exit 0
            else
                log_warning "Direct CLI invocation not yet implemented"
                log_info "Use Claude Code to invoke agents:"
                log_info "@${AGENT_NAME} ${TASK_DESCRIPTION}"
                exit 1
            fi
            ;;
    esac
}

main "$@"

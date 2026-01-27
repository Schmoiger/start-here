#!/usr/bin/env bash
# Agent Coordinator for multi-agent workflow
# Usage: ./coordinate.sh init       - Set up directories
#        ./coordinate.sh list       - List available agents
#        ./coordinate.sh workflow   - Show TDD workflow
# Or manually invoke agents in Claude Code with @agent-name syntax

set -e

AGENT_NAME="${1:-orchestrator}"
TASK_DESCRIPTION="${2:-}"

# Colour codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
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

log_phase() {
    echo -e "${CYAN}[PHASE]${NC} $1"
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

    # Phase 0: Discovery
    # (files created directly in ./artifacts/)

    # Phase 1: Design
    mkdir -p ./artifacts/database/migrations
    mkdir -p ./artifacts/api
    mkdir -p ./artifacts/design/visuals

    # Phase 2-3: Development
    mkdir -p ./artifacts/python/tests
    mkdir -p ./artifacts/typescript/tests

    # Phase 4-5: Testing
    mkdir -p ./artifacts/test-results
    mkdir -p ./artifacts/ui-test-results/screenshots
    mkdir -p ./artifacts/security-audit

    # Phase 6: Deploy
    mkdir -p ./artifacts/gcp/terraform

    # Phase 7: Documentation (per doc-standards.md)
    mkdir -p ./artifacts/docs/build
    mkdir -p ./artifacts/docs/specs
    mkdir -p ./artifacts/docs/guides

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

    log_success "Agent environment initialised"
}

# List available agents by phase
list_agents() {
    echo ""
    log_phase "Phase 0: Discovery"
    echo "  @product-owner       - Requirements gathering and user stories"
    echo ""

    log_phase "Phase 1: Design"
    echo "  @solution-architect  - System architecture and API contracts"
    echo "  @database-designer   - Database schema and migrations"
    echo "  @api-designer        - OpenAPI specifications"
    echo "  @ui-designer         - UI wireframes, components, design tokens"
    echo "  @visual-designer     - Visual assets using AI tools"
    echo ""

    log_phase "Phase 2: Tests First (TDD Red)"
    echo "  @functional-tester   - Write failing tests from requirements"
    echo ""

    log_phase "Phase 3: Development (TDD Green)"
    echo "  @python-coder        - Write Python code to pass tests"
    echo "  @typescript-coder    - Write TypeScript code to pass tests"
    echo ""

    log_phase "Phase 4: Review"
    echo "  @tech-lead           - Architecture compliance gate"
    echo "  @code-reviewer       - Deep bug hunting"
    echo ""

    log_phase "Phase 5: Testing"
    echo "  @functional-tester   - Run all tests, verify coverage"
    echo "  @ui-tester           - Test UI with Chrome DevTools"
    echo "  @security-tester     - Security audit and threat modelling"
    echo ""

    log_phase "Phase 6: Deploy"
    echo "  @gcp-devops          - Configure GCP infrastructure"
    echo ""

    log_phase "Phase 7: Documentation"
    echo "  @documentation       - API references and guides"
    echo ""

    echo "Usage in Claude Code:"
    echo "  @product-owner define requirements for a task management API"
    echo "  @functional-tester write failing tests for the task API"
    echo "  @python-coder implement the task service (make tests pass)"
}

# Show TDD workflow
show_workflow() {
    cat << 'EOF'

TDD WORKFLOW (Test-Driven Development)
======================================

Tests are written BEFORE implementation.

Phase 0: Discovery
    @product-owner
    Output: requirements.md, user-stories.md, open-questions.md
                |
                v
Phase 1: Design (parallel)
    @solution-architect  -> architecture.md, api-contract.json
    @database-designer   -> schema.sql, migrations/
    @api-designer        -> openapi.yaml
    @ui-designer         -> design-tokens.json, wireframes.md
    @visual-designer     -> design/visuals/
                |
                v
Phase 2: Tests First (TDD RED)
    @functional-tester
    Output: Failing tests based on requirements
    All tests SHOULD FAIL initially
                |
                v
Phase 3: Development (TDD GREEN)
    @python-coder        -> ./artifacts/python/
    @typescript-coder    -> ./artifacts/typescript/
    Goal: Make all tests pass
                |
                v
Phase 4: Review (GATE)
    @tech-lead reviews (architecture, standards)
        |
        +-- CHANGES REQUIRED --> Back to Phase 3
        |
        +-- APPROVED --> @code-reviewer (bugs, edge cases)
                |
                v
Phase 5: Testing (parallel)
    @functional-tester   -> coverage report
    @ui-tester           -> ui-test-results/
    @security-tester     -> security-audit/
                |
                v
Phase 6: Deploy
    @gcp-devops          -> gcp/terraform/
                |
                v
Phase 7: Documentation
    @documentation       -> docs/

COVERAGE REQUIREMENTS
=====================
Minimum: 90% (build fails below)
Target:  100%
Gaps:    Document in test-gaps.md

TDD CYCLE
=========
1. RED:    @functional-tester writes failing tests
2. GREEN:  @python-coder/@typescript-coder makes tests pass
3. REFACTOR: Clean up while tests pass
4. REPEAT: Next requirement

EOF
}

# Show artifacts directory structure
show_structure() {
    cat << 'EOF'

ARTIFACTS DIRECTORY STRUCTURE
=============================

./artifacts/
├── requirements.md              # Product owner
├── user-stories.md              # Product owner
├── open-questions.md            # Product owner
├── architecture.md              # Solution architect
├── api-contract.json            # Solution architect
├── data-model.md                # Solution architect
├── database/
│   ├── schema.sql               # Database designer
│   ├── migrations/              # Database designer
│   └── er-diagram.md            # Database designer
├── api/
│   ├── openapi.yaml             # API designer
│   └── api-design-guide.md      # API designer
├── design/
│   ├── design-tokens.json       # UI designer
│   ├── components.md            # UI designer
│   ├── wireframes.md            # UI designer
│   └── visuals/                 # Visual designer
├── python/
│   ├── *.py                     # Python coder
│   ├── requirements.txt
│   ├── README.md
│   └── tests/                   # Functional tester
├── typescript/
│   ├── *.ts                     # TypeScript coder
│   ├── package.json
│   ├── README.md
│   └── tests/                   # Functional tester
├── test-results/                # Functional tester
├── test-gaps.md                 # Functional tester (if coverage < 100%)
├── ui-test-results/             # UI tester
│   └── screenshots/
├── security-audit/              # Security tester
│   └── prompt-injection-assessment.md
├── gcp/
│   └── terraform/               # GCP DevOps
├── tech-review.md               # Tech lead
├── code-review.md               # Code reviewer
└── docs/                        # Documentation (per doc-standards.md)
    ├── build/
    │   ├── bugs.md              # Bug tracking
    │   ├── tasks.md             # Task tracking
    │   └── todo.md              # Technical debt
    ├── specs/
    │   ├── product.md           # Product/UX docs
    │   ├── requirements.md      # EARS requirements
    │   └── design.md            # Architecture decisions
    └── guides/
        ├── getting-started.md   # Setup guide
        └── developer-guide.md   # Dev workflows

EOF
}

# Main entry point
main() {
    case "${AGENT_NAME}" in
        list|--list|-l)
            list_agents
            ;;
        workflow|--workflow|-w)
            show_workflow
            ;;
        structure|--structure|-s)
            show_structure
            ;;
        init|--init|-i)
            init_agent_dirs
            ;;
        *)
            if [ -z "$TASK_DESCRIPTION" ]; then
                echo "Agent Coordinator - Multi-agent TDD orchestration for Claude Code"
                echo ""
                echo "Usage:"
                echo "  $0 init              - Initialise agent directories"
                echo "  $0 list              - List available agents by phase"
                echo "  $0 workflow          - Show TDD workflow"
                echo "  $0 structure         - Show artifacts directory structure"
                echo ""
                echo "In Claude Code, invoke agents directly:"
                echo "  @product-owner define requirements for a task API"
                echo "  @functional-tester write failing tests for the task API"
                echo "  @python-coder implement the task service"
                echo ""
                echo "See CLAUDE.md for full orchestration guide."
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

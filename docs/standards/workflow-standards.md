# Within Eve Technology Developer Workflow

## Overview
The developer workflow follows a structured approach to ensure quality and consistency across all projects.

## 1. Create Git Branch
Create and switch to a new feature branch following the branch naming conventions. Add gitignore that inherits monorepo gitignore (see `README.md`)

**Branch Naming:**
- `feature/feature-name` for new features
- `bugfix/bugref-name` for bug fixes

**Commands:**
```bash
git checkout -b feature/feature-name
git push -u origin feature/feature-name
```

## 2. Project Setup
Set up project folder with blank files according to documentation standards.

**Files to create:**
- `docs/specs/product.md` - Product specification
- `docs/specs/requirements.md` - Requirements specification
- `docs/specs/design.md` - Design specification
- `docs/build/tasks.md` - Task breakdown
- README.md and other project files as per standards

## 3. Write Specifications
Write the specs documents in this order:

1. **Product Spec** (`docs/specs/product.md`)
   - Define the product vision, goals, and user stories
   - Identify key stakeholders and success criteria

2. **Requirements Spec** (`docs/specs/requirements.md`)
   - Detail functional and non-functional requirements
   - Specify acceptance criteria and constraints

3. **Design Spec** (`docs/specs/design.md`)
   - Outline technical architecture and design decisions
   - Define data models, APIs, and user interfaces

## 4. Check Specs Against Standards
Validate all specifications against the following standards:

- **Documentation Standards** (`docs/common/standards/`)
  - Ensure consistency with existing patterns
  - Verify adherence to formatting and structure guidelines

- **Technical Standards** (`docs/common/standards/tech-standards.md`)
  - Confirm technical decisions align with approved patterns
  - Validate architectural choices

## 5. Write Tasks
Break down the specifications into actionable development tasks in `docs/build/tasks.md`.

**Task Structure:**
- Clear, measurable objectives
- Estimated effort and dependencies
- Acceptance criteria
- References to relevant specification sections

## 6. Check Tasks Against Rules
Validate tasks against the established rules and guidelines:

- **Development Rules** (`docs/common/rules/`)
  - Ensure tasks comply with coding standards
  - Verify testing requirements are included
  - Confirm security considerations are addressed

- **Quality Gates**
  - Unit testing plans
  - Integration testing requirements
  - Code review criteria
  - Deployment readiness checklists

## 7. Update Documentation
Update both project and monorepo-level documentation to reflect completed work.

**Project Documentation:**
- `README.md` - Update with implementation details, usage guides, and deployment instructions
- `docs/` - Update guides, API references, and user documentation
- Configuration files documentation

**Monorepo Documentation:**
- `README.md` - Update workspace description
- `docs/common/schema/` - Update API schemas and data models

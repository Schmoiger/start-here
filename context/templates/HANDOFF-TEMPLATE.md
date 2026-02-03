# {Service Name} Handoffs

Intra-domain handoffs within the {service-name} context domain.

**Last Updated**: {ISO 8601 timestamp with timezone}

---

## Current Phase: {TDD RED | TDD GREEN | Review | Integration}

### Latest Handoff

**From**: @{agent-name}
**To**: @{agent-name}
**Timestamp**: {ISO 8601 timestamp with timezone}
**Tasks**: {TASK-ID} through {TASK-ID}
**Status**: ✅ Complete | 🚧 In Progress | ⚠️ Blocked

**Summary**:
{Brief description of what was completed}

**Notes for Next Agent**:
- {Important information}
- {Files to review}
- {Known issues or gotchas}

**Artifacts**:
- Code: `{path}`
- Tests: `{path}`
- Fixtures: `{path}`
- Documentation: `{path}`

**Blockers**: None | {List blockers}

**Commit**: {commit-hash} - {commit message}

---

## Handoff History

### From: @{agent-name}
**To**: @{agent-name}
**Timestamp**: {timestamp}
**Tasks**: {TASK-ID} through {TASK-ID}
**Summary**: {summary}
**Commit**: {hash}

---

## Integration Checklist

Before marking service as "Ready for Integration":

- [ ] All TDD RED tasks complete (tests written and failing)
- [ ] All TDD GREEN tasks complete (implementation done, tests passing)
- [ ] Tech lead review approved
- [ ] Test coverage >= 90%
- [ ] API endpoints match OpenAPI spec
- [ ] Mock client created in `artifacts/shared/mocks/`
- [ ] Example responses in `artifacts/shared/fixtures/`
- [ ] Cross-domain handoff file created in `artifacts/shared/handoffs/{service}-api.md`
- [ ] Integration status updated in `artifacts/shared/handoffs/integration-status.md`

---

## Revision History

| Timestamp | Agent | Phase | Tasks | Status |
|-----------|-------|-------|-------|--------|
| {timestamp} | @{agent} | {phase} | {tasks} | {status} |

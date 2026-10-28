---
name: gcp-deployment
description: Procedural guidance for deploying to GCP — Terraform validate and plan before apply, staging before production, Cloud Run Functions Gen 2, Firebase Hosting, Workload Identity, and a mandatory rollback plan.
globs: ["**/*.tf", "**/terraform/**", "artefacts/gcp/**"]
---

# GCP Deployment Skill

**Applies to**: cloud and production deployment tasks (`deploy.yaml`). Local Supabase work belongs to `supabase-operations.md`.

---

## Preconditions

1. The build workflow's `local-deployment` phase has completed and been validated — never deploy code that has not run locally.
2. The deployment target, project, and region are stated in the task. Do not infer them.
3. A rollback plan exists **before** the first `apply`.

---

## Infrastructure as Code

All infrastructure is Terraform (build-standards.md). Never make console changes that are not reflected in code — a manual fix is drift that the next `apply` will revert.

```bash
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```

Read the `plan` output before applying: the resource count and the destroy list are the blast radius. A plan that destroys a data store requires explicit human approval, not just a production approval.

---

## Platform Shape

| Layer | Service | Notes |
|-------|---------|-------|
| Backend | Cloud Run Functions Gen 2 | Stateless; scaling configured in Terraform |
| Frontend | Firebase Hosting | Static build artefacts only |
| Identity | Workload Identity | No long-lived service-account keys |
| Region | `europe-west2` | All resources unless the task states otherwise |
| Access | Least privilege | Scoped IAM roles per service, not project-wide |

Encryption at rest and in transit is non-negotiable; both are defaults on the services above, and disabling either is an architectural decision, not a deployment shortcut.

---

## Staging Before Production

1. Apply to the staging project first
2. Run health checks and smoke tests against the staging URLs — verify the deployed revision, not the pipeline status
3. Capture the evidence (command output, response bodies)
4. **Halt for explicit human approval** before applying to production
5. Apply the same plan to production; do not hand-edit between environments

---

## Rollback

Document the reverse operation before deploying:

- **Revision rollback** — redeploy the previous Cloud Run revision
- **Terraform revert** — `git revert` the configuration change and apply the resulting plan
- **Data** — a deployment that includes a migration needs a matching down migration or a documented restore point

A deployment with no rollback plan is not complete (`deploy.yaml` §validation).

---

## Deliverables

- Terraform: `{project-root}/artefacts/gcp/terraform/`
- Deployment guide: `{project-root}/artefacts/gcp/deployment-guide.md`
- Security checklist: `{project-root}/artefacts/gcp/security-checklist.md`

Validate markdown outputs with:

```bash
uv run python context/scripts/validators/verify_typst_formatting.py {files}
```

---

## Why

Cloud deployments fail expensively and asymmetrically: the cost of a bad `apply` is paid by users, while the cost of reading a `plan` is paid in seconds. Staging-first, approval-gated production, and a written rollback convert an irreversible risk into a reversible one.

---
name: supabase-operations
description: Procedural guidance for Supabase migrations, queries, and maintenance via MCP
globs: ["**/migrations/*.sql", "**/supabase/**", "**/database_service/**", "**/stores/**"]
---

# Supabase Operations Skill

**Applies to**: every database operation against the Supabase project — queries, migrations, and deployments.

---

## 1. Non-Negotiable Invariants

**Tooling**

- **Always use the Supabase MCP tools** for queries and migrations — `mcp__supabase__execute_sql` and `mcp__supabase__apply_migration`.
- **Never** use `supabase db push`, `supabase db query`, `supabase db reset`, or `psql`. Schema state is asserted by querying the catalogue, not by a CLI dry run.
- **One whitelisted CLI exception**: `supabase functions deploy <name>`. The MCP server exposes no edge-function deployment tool, so this is the only `supabase` command permitted.
- **Never** assume Docker is running.

**Migration auditing** — after every `apply_migration`, insert an audit row into `schema_migrations`:

```sql
INSERT INTO schema_migrations (migration_file, applied_at)
VALUES ('<filename>.sql', now()) ON CONFLICT DO NOTHING;
```

**Timestamp bloat** — updating `fetched_at`/`computed_at` on every upsert creates dead tuples even when the payload is unchanged. Update timestamps **only** when the values actually change.

---

## 2. Supabase MCP Tool Mapping

Use the following MCP tools for Supabase operations:

| Action | Correct | Wrong |
|--------|---------|-------|
| Query | `mcp__supabase__execute_sql` | `supabase db query`, `psql` |
| Migration | `mcp__supabase__apply_migration` + insert into `schema_migrations` | `supabase db push` |
| Edge function deploy | `supabase functions deploy <name>` (whitelisted — no MCP equivalent) | dashboard edits |
| Logs | `mcp__supabase__get_logs` | CLI |
| Advisors | `mcp__supabase__get_advisors` | — |
| VACUUM | `mcp__supabase__execute_sql` | asyncpg in app code |

---

## 3. Migration Execution and Indexes

`apply_migration` runs inside a transaction — `CONCURRENTLY` DDL will silently create an invalid index or error. Use plain forms in migration files; use `execute_sql` for concurrent operations on live tables:

| | Migration file | `execute_sql` |
|-|---------------|---------------|
| Drop index | `DROP INDEX IF EXISTS idx` | `DROP INDEX CONCURRENTLY IF EXISTS idx` |
| Create index | `CREATE INDEX idx ON ...` | `CREATE INDEX CONCURRENTLY idx ON ...` |

---

## 4. Autovacuum Tuning

Default `scale_factor = 0.20` means vacuum triggers after 20% dead tuples — too late for large upsert-heavy tables. Tune per-table (Supabase blocks server-level GUC changes):

```sql
ALTER TABLE <table> SET (
    autovacuum_vacuum_scale_factor = 0.01,
    autovacuum_vacuum_threshold = 100,
    autovacuum_analyze_scale_factor = 0.005
);
```

Apply to any table > 1M rows with frequent upserts. Never add `VACUUM` to application code — run on demand via `execute_sql` after bulk loads only.

---

## 5. Diagnostics and Gotchas

### Replication Slots

Stale slots (consumer gone, slot not dropped) silently accumulate WAL until disk fills. Check when diagnosing disk growth:

```sql
SELECT slot_name, active,
  pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS wal_behind
FROM pg_replication_slots;
```

### PostgREST Transactions

All app queries run inside a transaction — VACUUM and `CONCURRENTLY` DDL require `execute_sql` or a direct connection.

---

## 6. Deployment Procedure (Local/Staging)

Use this procedure for the `schema-migration` and `local-deployment` build phases, and any staging deployment.

1. **Pending-migration check** — list migration files in `{project-root}/supabase/migrations/` and compare against `schema_migrations` via `mcp__supabase__execute_sql`:
   ```sql
   SELECT migration_file FROM schema_migrations ORDER BY migration_file;
   ```
   Every unapplied file is either work to do or drift to report; do not proceed while the difference is unexplained.

2. **Apply migrations** — `mcp__supabase__apply_migration` in filename order, inserting the audit row each time (§1). A migration that fails mid-file leaves a partial schema: stop, report, and provide the down migration.

3. **Deploy edge functions** — `supabase functions deploy <name>` for each changed function. This is the only permitted CLI command (§1). If it fails, capture the output verbatim in the log and stop; do not retry against a different target.

4. **Validate RLS** — assert that every table exposed through PostgREST has row-level security enabled and a policy that matches the intended access model:
   ```sql
   SELECT schemaname, tablename, policyname, cmd, roles
   FROM pg_policies
   WHERE schemaname = 'public';
   ```
   A table with RLS enabled and no policy is deny-all — confirm that is intentional before reporting success.

5. **Smoke test** — exercise the key API endpoints and record the status code and a one-line body summary for each. A 200 from a health endpoint does not prove the migration landed; query the schema as part of the smoke test.

6. **Write the deployment log** incrementally to `{project-root}/artefacts/supabase/deployment-log.md`:

   ```markdown
   ## {date} — {environment}

   - **Migrations applied**: `{filename}` … (or "none")
   - **Functions deployed**: `{name}` … (or "none")
   - **Schema assertion**: `{query}` → `{expected result}`
   - **RLS**: `{tables checked}`, `{policies asserted}`
   - **Smoke tests**: `{endpoint}` → `{status}` …
   - **Rollback**: `{down migration path or function revision}`
   ```

7. **Document rollback** — for each migration, the down migration or the manual revert; for each function, the previous revision to redeploy. A deployment with no rollback step is not complete.

---

## 7. Why

Migrations are the one class of change that cannot be fixed by redeploying the previous commit — the data has already moved. Checking pending state before applying, asserting the schema afterwards, and writing the rollback down before deploying are what keep a recoverable failure from becoming an unrecoverable one.

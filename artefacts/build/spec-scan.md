# Spec Scan: start-here
Generated: 2026-10-30T14:12:07Z · mode: both · 57 files · languages: python

## Scan Warnings
- pytest: 198 collected (uv)

## Existing Spec Documents
| Path | Kind |
|---|---|
| `.githooks/README.md` | readme |
| `README.md` | readme |
| `artefacts/README.md` | readme |
| `artefacts/api/api-design-guide.md` | api |
| `artefacts/architecture/api-catalogue.md` | architecture |
| `artefacts/architecture/architecture-decision.md` | architecture |
| `artefacts/architecture/architecture.md` | architecture |
| `artefacts/architecture/data-model.md` | architecture |
| `artefacts/design/accessibility.md` | design |
| `artefacts/design/components.md` | design |
| `artefacts/design/user-flows.md` | design |
| `artefacts/design/visuals-manifest.md` | design |
| `artefacts/design/wireframes.md` | design |
| `artefacts/product/open-questions.md` | requirements |
| `artefacts/product/requirements.md` | requirements |
| `artefacts/product/user-stories.md` | requirements |
| `context/README.md` | readme |
| `context/scripts/tests/README.md` | readme |
| `context/scripts/validators/README.md` | readme |
| `context/skills/requirements-elicitation.md` | requirements |
| `context/templates/requirements-template.md` | requirements |
| `context/workflows/README.md` | readme |
| `tests/context-unit-tests/README.md` | readme |

## Repository Map (symbols)
- `context/scripts/code-specs/spec_indexer.py` (1112 lines): const LANG_BY_SUFFIX(54), const DOC_GLOBS(65), const DOC_BASENAME_PATTERNS(77), const EXCLUDED_DIRS(88), const ROUTE_METHOD_ATTRS(111), const _JSX_TAG_RE(115), const _TS_IMPORT_NAMED(118), const _TS_IMPORT_DEFAULT(121), const _TS_FUNC(124), const _TS_ARROW(127), const _TS_CLASS(131), const _TS_IFACE(132), const _TS_TYPE(133), const _TS_REQUIRE(134), class Symbol(144), method Symbol.to_jsonb(152), class FileRecord(164), method FileRecord.to_jsonb(171), class ApiEntry(182), method ApiEntry.to_jsonb(189), class ColumnDef(200), method ColumnDef.to_jsonb(204), class TableDef(209), method TableDef.to_jsonb(215), class UiComponent(225), method UiComponent.to_jsonb(233), class TestNode(245), method TestNode.to_jsonb(249), class DocRecord(254), method DocRecord.to_jsonb(258), function rel(267), function language_of(272), function find_target_files(277), function _unparse(335), function _decorator_names(342), function _route_from_decorator(350), function _method_body(375), function analyze_python(386), function _destructured_props(458), function _is_component(471), function analyze_tsjs(475), const _SQL_CREATE(562), const _SQL_SKIP_COLUMN(566), function analyze_sql(573), function _run(611), function collect_tests(619), function discover_docs(677), function analyze_openapi(709), const MAX_MAP_ROWS(747), const MAX_API_ROWS(748), const MAX_UI_ROWS(749), const MAX_TEST_ROWS(750), const MAX_SCHEMA_ROWS(751), function _default_out_dir(754), function render_spec_scan(759), function run_scan(852), const _CITATION_RE(952), function _line_text(957), function run_verify(971), function main(1039)
- `context/scripts/generators/adapters/claude/generator.py` (92 lines): function _extract_model_mappings(8), function generate_claude_md(34), function generate_subagent_prompts(60)
- `context/scripts/generators/adapters/cline/generator.py` (151 lines): function _extract_cline_model_mappings(10), function generate_cline_md(39), function generate_cline_rules(71), function generate_cline_skills(97)
- `context/scripts/generators/adapters/core/agents_md.py` (149 lines): function _trim_purpose(11), function generate_workflow_table(19), function generate_agent_dispatch_all(31), function generate_skill_table(60), function generate_agents_md(73)
- `context/scripts/generators/adapters/core/budget.py` (31 lines): class DeliveryStrategy(4), class TokenEstimator(10), method TokenEstimator.__init__(15), method TokenEstimator.estimate_tokens(18), method TokenEstimator.recommend_strategy(24)
- `context/scripts/generators/adapters/core/loader.py` (125 lines): function extract_frontmatter(14), function normalise_tools(22), function load_canonical_context(49)
- `context/scripts/generators/adapters/core/models.py` (58 lines): class CanonicalRule(5), class CanonicalStandard(11), class CanonicalSkill(17), class CanonicalAgent(25), class CanonicalPersona(39), class Phase(46), class WorkflowDAG(54)
- `context/scripts/generators/adapters/core/tools.py` (22 lines): class CapabilityRegistry(1), method CapabilityRegistry.__init__(6), method CapabilityRegistry.register_capability(9), method CapabilityRegistry.get_mapping(17)
- `context/scripts/generators/adapters/gemini/generator.py` (135 lines): function generate_skills(9), function _extract_model_mappings(85), function generate_gemini_md(111)
- `context/scripts/generators/adapters/github/generator.py` (180 lines): function generate_prompts(8), function generate_copilot_instructions(44), function generate_scoped_instructions(66), function generate_workflows(143)
- `context/scripts/generators/adapters/openai/generator.py` (133 lines): function generate_system_prompts(8), function generate_tool_schemas(46), function generate_runner_harness(75)
- `context/scripts/generators/generate_adapters.py` (468 lines): const _REPO_ROOT(24), const SUPPORTED_TARGETS(55), const TARGET_ALIASES(57), const IGNORED_BLOCK(74), function ensure_root_gitignore(91), function normalize_target(128), function load_configured_targets(137), function get_adapter_projections(163), function run_generation(226), function build_parser(308), function main(428)
- `context/scripts/prepare-commit-msg.py` (848 lines): class ExtractionResult(40), function format_tokens(51), function short_model(60), function get_git_repo_root(68), function get_watermark_path(79), function read_watermark(84), function write_watermark(95), function _decode_varint(109), function parse_protobuf_fields(125), class BaseExtractor(163), method BaseExtractor.is_available(167), method BaseExtractor.find_active_session(171), method BaseExtractor.extract_delta(175), class AntigravityExtractor(180), method AntigravityExtractor.__init__(184), method AntigravityExtractor.is_available(191), method AntigravityExtractor.find_active_session(194), method AntigravityExtractor.extract_delta(219), class CopilotExtractor(298), method CopilotExtractor.__init__(302), method CopilotExtractor.is_available(311), method CopilotExtractor.find_active_session(314), method CopilotExtractor.extract_delta(349), class ClaudeExtractor(421), method ClaudeExtractor.is_available(425), method ClaudeExtractor.find_active_session(428), method ClaudeExtractor.extract_delta(443), class CodexExtractor(514), method CodexExtractor.is_available(518), method CodexExtractor.find_active_session(521), method CodexExtractor.extract_delta(524), class ClineExtractor(528), method ClineExtractor.__init__(546), method ClineExtractor.is_available(560), method ClineExtractor._load_session_meta(564), method ClineExtractor.find_active_session(572), method ClineExtractor.extract_delta(597), const EXTRACTORS(681), function select_extractor(694), function _set_trailer_field(724), function update_commit_message(731), function main(779)
- `context/scripts/tests/conftest.py` (125 lines): function fixtures_dir(8), function valid_commit(14), function invalid_commit_no_scope(20), function invalid_commit_too_long(26), function invalid_commit_past_tense(32), function valid_commit_with_agent_session(38), function merge_commit(44), function valid_requirements(50), function invalid_requirements(56), function valid_british_english(62), function invalid_british_english(68), function valid_metrics(74), function invalid_metrics(80), function valid_interruptions(86), function invalid_interruptions(92), function test_workflow(98), function valid_agent(104), function invalid_agent_no_frontmatter(110), function invalid_agent_hardcoded_paths(116), function invalid_agent_missing_sections(122)
- `context/scripts/tests/test_adapter_drift.py` (172 lines): function test_adapter_drift_clean_repo(8), function test_adapter_drift_detects_modified_file(16), function test_adapter_drift_detects_missing_file(47), function test_adapter_drift_detects_orphaned_file(76), function test_adapter_drift_with_agent_targets_file(110), function test_adapter_drift_cline_managed_dirs(138)
- `context/scripts/tests/test_adapters_core.py` (219 lines): class TestAdaptersCoreModels(20), method TestAdaptersCoreModels.test_canonical_agent_dataclass(21), method TestAdaptersCoreModels.test_canonical_skill_dataclass(34), class TestAdaptersCoreLoader(52), method TestAdaptersCoreLoader.setUp(53), method TestAdaptersCoreLoader.tearDown(107), method TestAdaptersCoreLoader.test_load_canonical_context(110), method TestAdaptersCoreLoader.test_missing_agent_validation(130), class TestToolNormalisation(145), method TestToolNormalisation._load_tools(148), method TestToolNormalisation.test_annotated_mapping_form(158), method TestToolNormalisation.test_plain_string_form(166), method TestToolNormalisation.test_scalar_string_form(170), method TestToolNormalisation.test_top_level_mapping_form(174), method TestToolNormalisation.test_legacy_mcp_tools_key(178), method TestToolNormalisation.test_absent_tools(183), class TestAdaptersCoreTools(187), method TestAdaptersCoreTools.test_capability_registry_extensibility(188), class TestAdaptersCoreBudget(202), method TestAdaptersCoreBudget.test_token_estimator(203)
- `context/scripts/tests/test_agent_validator.py` (471 lines): const CONTEXT_ACQUISITION_BODY(11), class TestAgentValidator(21), method TestAgentValidator.test_valid_agent(24), method TestAgentValidator.test_no_frontmatter(29), method TestAgentValidator.test_hardcoded_paths(35), method TestAgentValidator.test_missing_required_sections(41), method TestAgentValidator.test_context_acquisition_section_passes(47), method TestAgentValidator.test_legacy_required_sections_rejected(75), method TestAgentValidator.test_agent_template_scaffold_passes_validation(96), method TestAgentValidator.test_invalid_yaml_frontmatter(128), method TestAgentValidator.test_missing_required_fields(143), method TestAgentValidator.test_relative_paths_flagged(156), method TestAgentValidator.test_reminders_without_attribution(174), method TestAgentValidator.test_proper_attribution_passes(193), method TestAgentValidator.test_project_root_placeholders_allowed(215), method TestAgentValidator.test_nonexistent_standards_flagged(235), method TestAgentValidator.test_nonexistent_rules_flagged(249), method TestAgentValidator.test_nonexistent_skills_flagged(262), method TestAgentValidator.test_canonical_interruption_log_path_passes(275), method TestAgentValidator.test_legacy_interruption_log_path_rejected(291), method TestAgentValidator.test_interruption_log_wildcard_allowed(307), method TestAgentValidator.test_body_table_source_should_fail_when_file_does_not_exist(323), method TestAgentValidator.test_body_table_source_should_fail_when_section_does_not_exist(343), method TestAgentValidator.test_body_table_source_should_pass_when_citations_resolve(363), method TestAgentValidator.test_body_citation_should_fail_when_file_does_not_exist(383), method TestAgentValidator.test_body_citation_should_fail_when_section_does_not_exist(401), method TestAgentValidator.test_body_citation_should_pass_when_section_resolves(419), method TestAgentValidator.test_body_citation_error_should_report_file_line_number_when_it_fails(435), method TestAgentValidator.test_body_table_without_source_column_should_be_ignored(456)
- `context/scripts/tests/test_claude_adapter.py` (45 lines): function test_generate_claude_md(10), function test_generate_subagent_prompts(23)
- `context/scripts/tests/test_cli_dispatcher.py` (189 lines): function test_target_normalization(15), function test_cli_parser_flags(38), function test_dry_run_leaves_disk_untouched(64), function test_smart_update_preserves_unchanged_files(86), function test_generation_execution_speed_benchmark(132), function test_ensure_root_gitignore(146), function test_load_configured_targets(175)
- `context/scripts/tests/test_cline_adapter.py` (84 lines): class TestClineAdapter(16), method TestClineAdapter.setUp(19), method TestClineAdapter.tearDown(41), method TestClineAdapter.test_generate_cline_md(44), method TestClineAdapter.test_generate_cline_rules(55), method TestClineAdapter.test_generate_cline_skills(67)
- `context/scripts/tests/test_e2e_compilation.py` (213 lines): function test_e2e_full_compilation_all_targets(13), function test_e2e_deterministic_reproducibility(104), function test_e2e_synthetic_context_compilation(146)
- `context/scripts/tests/test_gemini_adapter.py` (81 lines): class TestGeminiAdapter(15), method TestGeminiAdapter.setUp(16), method TestGeminiAdapter.tearDown(33), method TestGeminiAdapter.test_generate_skills(36), method TestGeminiAdapter.test_generate_skills_escapes_colon_in_description(53), method TestGeminiAdapter.test_generate_gemini_md(68)
- `context/scripts/tests/test_github_adapter.py` (128 lines): function test_generate_copilot_instructions(12), function test_generate_prompts(25), function test_generate_scoped_instructions(49), function test_generate_scoped_instructions_with_exclude_agent(80), function test_generate_workflows(108)
- `context/scripts/tests/test_openai_adapter.py` (61 lines): function test_generate_system_prompts(12), function test_generate_tool_schemas(38), function test_generate_runner_harness(51)
- `context/scripts/tests/test_packaging.py` (49 lines): function test_pyproject_toml_exists(8), function test_generator_entrypoint_parser(20), function test_drift_validator_callable(38)
- `context/scripts/tests/test_runtime_telemetry.py` (620 lines): const EXTRACTORS(45), function test_format_tokens(54), function test_protobuf_wire_format_parsing(63), function _encode_varint(76), function _encode_field(90), function test_antigravity_synthetic_extraction(101), function test_copilot_synthetic_extraction(161), function test_commit_message_updating(217), function test_live_antigravity_storage_sanity(244), function test_live_copilot_storage_sanity(285), function test_live_claude_storage_sanity(322), function _make_cline_session(360), function test_cline_extract_delta_counts_assistant_metrics(380), function test_cline_extract_delta_accepts_wrapped_messages(414), function test_cline_extract_delta_session_switch_resets(438), function test_cline_extract_delta_falls_back_to_session_model(462), function test_cline_extract_delta_error_paths(478), function test_cline_find_active_session_matches_repo_and_picks_newest(502), function test_cline_registry_and_selection(529), function test_short_model_strips_provider_prefix(540), function test_update_commit_message_injects_tool_and_model(547), function test_update_commit_message_removes_stale_tokens(562), function test_live_cline_storage_sanity(577)
- `context/scripts/tests/test_validators.py` (1254 lines): class TestConventionalCommits(65), method TestConventionalCommits.test_valid_commit(68), method TestConventionalCommits.test_invalid_no_scope(75), method TestConventionalCommits.test_invalid_too_long(82), method TestConventionalCommits.test_invalid_past_tense(89), method TestConventionalCommits.test_valid_with_agent_session(96), method TestConventionalCommits.test_merge_commit_allowed(102), method TestConventionalCommits.test_empty_commit_fails(108), method TestConventionalCommits.test_invalid_type(115), method TestConventionalCommits.test_invalid_scope_uppercase(122), method TestConventionalCommits.test_coauthor_format(129), method TestConventionalCommits.test_agent_session_requires_coauthor(138), method TestConventionalCommits.test_agent_session_tokens_mega_suffix(147), method TestConventionalCommits.test_agent_session_tokens_lowercase_suffix(156), method TestConventionalCommits.test_agent_session_hook_appended_form(165), method TestConventionalCommits.test_agent_session_malformed_tokens_fails(174), class TestAgentSessionCorroboration(185), method TestAgentSessionCorroboration._cline_session_for_repo(193), method TestAgentSessionCorroboration._agent_commit(212), method TestAgentSessionCorroboration.test_model_corroborated_for_cline(219), method TestAgentSessionCorroboration.test_model_contradicting_runtime_fails(228), method TestAgentSessionCorroboration.test_unconfirmable_model_fails(238), method TestAgentSessionCorroboration.test_third_party_tool_not_adjudicated(247), class TestEARSNotation(253), method TestEARSNotation.test_valid_requirements(256), method TestEARSNotation.test_invalid_requirements(261), method TestEARSNotation.test_ubiquitous_pattern(267), method TestEARSNotation.test_event_pattern(272), method TestEARSNotation.test_state_pattern(276), method TestEARSNotation.test_optional_pattern(280), method TestEARSNotation.test_forbidden_pattern(284), method TestEARSNotation.test_complex_pattern(288), method TestEARSNotation.test_non_ears_requirement(294), method TestEARSNotation.test_code_blocks_ignored(299), class TestBritishEnglish(315), method TestBritishEnglish.test_valid_british_english(318), method TestBritishEnglish.test_invalid_american_english(323), method TestBritishEnglish.test_color_vs_colour(330), method TestBritishEnglish.test_behavior_vs_behaviour(342), method TestBritishEnglish.test_organize_vs_organise(353), method TestBritishEnglish.test_code_blocks_ignored(364), method TestBritishEnglish.test_inline_code_ignored(379), class TestMetricsLogging(389), method TestMetricsLogging.test_valid_metrics(392), method TestMetricsLogging.test_invalid_metrics(397), method TestMetricsLogging.test_metrics_log_location_under_build(402), method TestMetricsLogging.test_metrics_log_requires_jsonl_suffix(406), method TestMetricsLogging.test_metrics_log_rejects_repository_root(411), method TestMetricsLogging.test_missing_required_field(416), method TestMetricsLogging.test_invalid_timestamp(429), method TestMetricsLogging.test_invalid_event(442), method TestMetricsLogging.test_invalid_token_source(455), method TestMetricsLogging.test_missing_tokens_fields(468), method TestMetricsLogging.test_handoff_requires_to_field(481), method TestMetricsLogging.test_empty_file_valid(495), method TestMetricsLogging.test_invalid_json(503), class TestInterruptionsLogging(513), method TestInterruptionsLogging._question(517), method TestInterruptionsLogging.test_valid_interruptions(532), method TestInterruptionsLogging.test_invalid_interruptions(537), method TestInterruptionsLogging.test_missing_required_field(542), method TestInterruptionsLogging.test_null_outcome_fields_allowed(549), method TestInterruptionsLogging.test_invalid_type(554), method TestInterruptionsLogging.test_invalid_timestamp(560), method TestInterruptionsLogging.test_agent_at_prefix_rejected(566), method TestInterruptionsLogging.test_invalid_decision(572), method TestInterruptionsLogging.test_invalid_impact(588), method TestInterruptionsLogging.test_options_must_be_array(605), method TestInterruptionsLogging.test_mixed_tasks_rejected(623), method TestInterruptionsLogging.test_legacy_filename_rejected(633), method TestInterruptionsLogging.test_duplicate_ids_rejected(640), method TestInterruptionsLogging.test_resolution_ref_must_resolve(647), method TestInterruptionsLogging.test_resolution_record_resolves(669), method TestInterruptionsLogging.test_empty_file_valid(690), method TestInterruptionsLogging.test_invalid_json(696), method TestInterruptionsLogging.test_interruptions_path_detection(703), method TestInterruptionsLogging.test_interruption_log_requires_jsonl_suffix(709), method TestInterruptionsLogging.test_main_auto_detects_interruptions_log(715), method TestInterruptionsLogging.test_main_auto_detects_metrics_log(728), class TestTypstFormatting(753), method TestTypstFormatting.test_valid_formatting(756), method TestTypstFormatting.test_mermaid_insufficient_blank_lines(772), method TestTypstFormatting.test_section_heading_without_separator(793), method TestTypstFormatting.test_typst_skip_blocks_ignored(812), method TestTypstFormatting.test_headings_in_code_blocks_ignored(824), class TestWorkspaceOutputLocations(842), method TestWorkspaceOutputLocations.test_valid_output_paths(845), method TestWorkspaceOutputLocations.test_invalid_artefact_subdir(856), method TestWorkspaceOutputLocations.test_invalid_test_result_name(863), class TestUIDev(871), method TestUIDev.test_important_forbidden(874), method TestUIDev.test_raw_hex_forbidden(882), method TestUIDev.test_css_files_restriction(890), class TestSupabase(901), method TestSupabase.test_supabase_import_outside_database_service(904), method TestSupabase.test_supabase_import_inside_database_service_allowed(913), method TestSupabase.test_migration_audit_row_required(921), class TestTestingInvariants(939), method TestTestingInvariants.test_forbidden_interaction_mock(942), method TestTestingInvariants.test_exempt_interaction_mock(950), class TestTypeScriptEnvironment(958), method TestTypeScriptEnvironment.test_package_lock_flagged(961), method TestTypeScriptEnvironment.test_tsconfig_strictness(969), method TestTypeScriptEnvironment.test_workspaces_validation(982), class TestUITesting(996), method TestUITesting.test_banned_dependencies_flagged(999), method TestUITesting.test_puppeteer_core_allowed(1013), class TestSecrets(1025), method TestSecrets.test_private_key_flagged(1028), method TestSecrets.test_env_file_with_secret_flagged(1036), class TestSubrepoFreshness(1045), method TestSubrepoFreshness.test_find_subrepos(1048), method TestSubrepoFreshness.test_query_upstream_head_success(1070), method TestSubrepoFreshness.test_query_upstream_head_failure(1081), method TestSubrepoFreshness.test_subrepo_fresh_when_commit_matches(1092), method TestSubrepoFreshness.test_subrepo_stale_with_changes_fails(1112), method TestSubrepoFreshness.test_subrepo_stale_without_changes_passes(1134), method TestSubrepoFreshness.test_subrepo_check_all_forces_stale_detection(1154), method TestSubrepoFreshness.test_subrepo_unreachable_network_handling(1174), method TestSubrepoFreshness.test_main_cli_success(1197), class TestLoggingTemplateDocs(1219), method TestLoggingTemplateDocs.test_template_documents_metrics_schema(1229), method TestLoggingTemplateDocs.test_template_documents_interruption_schema(1235), method TestLoggingTemplateDocs.test_agent_template_references_logging_template(1249)
- `context/scripts/validators/adapter_drift.py` (164 lines): const _REPO_ROOT(20), function check_adapter_drift(31), function main(116)
- `context/scripts/validators/agent_definitions.py` (355 lines): const REPO_ROOT(32), const CONTEXT_DIR(33), const AGENTS_DIR(34), const SKIPPED_FILES(36), const CONTEXT_ACQUISITION_HEADING(39), const INTERRUPTIONS_PATH_PATTERN(43), const INTERRUPTION_LOG_NAME_PATTERN(44), const SOURCE_COLUMN_NAME(51), const PLACEHOLDER_CITATIONS(54), const CITATION_PATTERN(55), const CITATION_SEARCH_DIRS(58), const HEADING_PATTERN(67), const TABLE_SEPARATOR_PATTERN(68), function _normalise_title(71), function _without_number(77), function _headings(82), function _is_prefix(95), function _section_resolves(100), function _resolve_context_file(124), function _source_cells(137), function _validate_body_citations(160), function validate_agent_definition(200), function main(311)
- `context/scripts/validators/framework_docs_staleness.py` (98 lines): const REFERENCE_DOC(18), const BRIEF_DOC(19), const FRAMEWORK_DOCS(20), const BYPASS_MARKER(21), function get_staged_files(24), function get_commit_message(34), function is_context_change(41), function main(47)
- `context/scripts/validators/secrets.py` (110 lines): const REPO_ROOT(17), const RESTRICTED_PATTERNS(19), const EXEMPT_DIRS(29), const EXEMPT_MARKERS(30), function is_exempt_path(33), function scan_file_for_secrets(39), function main(78)
- `context/scripts/validators/subrepo_freshness.py` (236 lines): class SubrepoConfig(23), function find_subrepos(33), function get_modified_files(65), function query_upstream_head(109), function check_subrepo_freshness(131), function main(196)
- `context/scripts/validators/supabase.py` (114 lines): const PYTHON_IMPORT_PATTERN(17), const TS_IMPORT_PATTERN(18), const ALLOWED_IMPORT_DIRS(21), const MIGRATION_AUDIT_PATTERN(24), function is_allowed_supabase_location(30), function check_supabase_imports(36), function check_migration_audit(56), function main(72)
- `context/scripts/validators/tech_writing.py` (245 lines): const SPELLING_RULES(19), const DATE_PATTERN(36), function validate_british_english(42), const EARS_PATTERNS(104), function is_ears_requirement(114), function validate_requirements_file(123), function main(165)
- `context/scripts/validators/testing.py` (138 lines): const PY_INTERACTION_PATTERNS(19), const TS_INTERACTION_PATTERNS(27), const EXEMPT_MARKERS(33), const IGNORED_DIRS(34), function is_test_file(37), function check_forbidden_mocks(50), function validate_test_files(88), function main(106)
- `context/scripts/validators/typescript_environment.py` (176 lines): const REPO_ROOT(19), function check_package_lock(22), function _parse_json_with_comments(35), function check_tsconfig_strictness(50), function check_workspaces(76), function check_banned_npm_in_scripts(116), function main(134)
- `context/scripts/validators/ui_dev.py` (210 lines): const REPO_ROOT(20), const FRONTEND_SRC(21), const IMPORTANT_PATTERN(24), const RAW_HEX_PATTERN(27), const ALLOWED_SPACING(30), const CONCRETE_COLOUR_PATTERN(42), const HEROICONS_IMPORT_PATTERN(50), const DISALLOWED_SPACING_PATTERN(53), function check_important(61), function check_raw_hex(72), function check_css_files(90), function check_concrete_colours(107), function check_heroicons_import(118), function check_spacing(131), function is_test_or_spec(146), function main(150)
- `context/scripts/validators/ui_testing.py` (99 lines): const REPO_ROOT(16), const BANNED_PACKAGES(18), function is_exempt_package(26), function check_forbidden_ui_test_deps(38), function main(64)
- `context/scripts/validators/verify_typst_formatting.py` (230 lines): function get_repo_root(24), const TYPST_DIRS(38), function is_typst_doc(41), function get_staged_markdown_files(46), function get_tracked_markdown_files(61), function check_and_fix_file(71), function main(180)
- `context/scripts/validators/workspace_conventions.py` (674 lines): const VALID_OUTPUT_TOP_DIRS(24), const VALID_ARTEFACT_SUBDIRS(25), const TEST_RESULT_PATTERN(27), const REVIEW_PATTERN(28), const IMPL_DOC_PATTERN(29), function validate_output_path(32), function validate_output_paths(88), const VALID_COMMIT_TYPES(98), const COMMIT_SUBJECT_PATTERN(99), const COAUTHOR_PATTERN(100), const AGENT_SESSION_PATTERN(103), const TOOL_FIELD_PATTERN(125), const MODEL_FIELD_PATTERN(126), const _RUNTIME_TELEMETRY_MODULE(133), function _load_runtime_telemetry(136), function corroborate_agent_session(150), function validate_commit_message(196), const REQUIRED_METRICS_FIELDS(271), const VALID_METRICS_EVENTS(272), const VALID_TOKEN_SOURCES(273), function validate_metrics_entry(276), function validate_metrics_file(324), const INTERRUPTIONS_DIRNAME(354), const INTERRUPTION_BASE_FIELDS(356), const VALID_INTERRUPTION_TYPES(357), const VALID_INTERRUPTION_IMPACTS(358), const VALID_INTERRUPTION_DECISIONS(359), const INTERRUPTION_TYPE_FIELDS(361), const INTERRUPTION_NULLABLE_FIELDS(370), const INTERRUPTION_TS_PATTERN(372), function is_interruptions_log(375), function validate_interruptions_entry(381), function validate_interruptions_file(461), function _auto_detect(538), function main(585)
- `tests/context-unit-tests/conftest.py` (13 lines): function pytest_configure(8)
- `tests/context-unit-tests/test_doc_format.py` (247 lines): const DOCS_ROOT(14), const AGENTS_DIR(15), class TestAgentFrontmatter(18), method TestAgentFrontmatter.agent_files(22), method TestAgentFrontmatter.test_all_agents_have_frontmatter(30), method TestAgentFrontmatter.test_frontmatter_is_valid_yaml(41), method TestAgentFrontmatter.test_required_frontmatter_fields(64), method TestAgentFrontmatter.test_name_matches_filename(93), class TestAgentStructure(123), method TestAgentStructure.agent_files(127), method TestAgentStructure.test_has_task_placeholder(135), method TestAgentStructure.test_has_constraints_section(155), class TestStandardsFormat(174), method TestStandardsFormat.standards_files(178), method TestStandardsFormat.test_standards_have_introduction(182), class TestRulesFormat(197), method TestRulesFormat.rules_files(201), method TestRulesFormat.test_rules_have_frontmatter(205), class TestMarkdownLinks(221), method TestMarkdownLinks.all_markdown_files(225), method TestMarkdownLinks.test_no_broken_link_syntax(229)
- `tests/context-unit-tests/test_llm_consistency.py` (180 lines): function collect_docs(22), function build_consistency_prompt(48), function call_llm(89), class TestLLMConsistency(117), method TestLLMConsistency.consistency_result(121), method TestLLMConsistency.test_no_errors(127), method TestLLMConsistency.test_status_pass(141), method TestLLMConsistency.test_print_warnings(152)
- `tests/context-unit-tests/test_references.py` (264 lines): const BASE_DIR(18), const DOCS_ROOT(19), const AGENTS_DIR(20), function extract_file_references(23), function resolve_path(48), class TestAgentReferences(86), method TestAgentReferences.agent_files(90), method TestAgentReferences.test_context_path_references(98), class TestStandardsReferences(142), method TestStandardsReferences.standards_files(146), method TestStandardsReferences.test_doc_references_exist(150), class TestAgentDomainConsistency(184), method TestAgentDomainConsistency.test_all_domain_agents_exist(187), class TestReadmeLinks(225), method TestReadmeLinks.test_docs_readme_links(228)

## API Surface
None detected (no route decorators / OpenAPI docs found).

## Data Model
None detected (no SQL migrations / OpenAPI schemas found).

## UI Components
None detected (no TS/JSX component definitions found).

## Test Inventory (candidate features)
- context/scripts/tests/test_adapter_drift.py::test_adapter_drift_clean_repo
- context/scripts/tests/test_adapter_drift.py::test_adapter_drift_detects_modified_file
- context/scripts/tests/test_adapter_drift.py::test_adapter_drift_detects_missing_file
- context/scripts/tests/test_adapter_drift.py::test_adapter_drift_detects_orphaned_file
- context/scripts/tests/test_adapter_drift.py::test_adapter_drift_with_agent_targets_file
- context/scripts/tests/test_adapter_drift.py::test_adapter_drift_cline_managed_dirs
- context/scripts/tests/test_adapters_core.py::TestAdaptersCoreModels::test_canonical_agent_dataclass
- context/scripts/tests/test_adapters_core.py::TestAdaptersCoreModels::test_canonical_skill_dataclass
- context/scripts/tests/test_adapters_core.py::TestAdaptersCoreLoader::test_load_canonical_context
- context/scripts/tests/test_adapters_core.py::TestAdaptersCoreLoader::test_missing_agent_validation
- context/scripts/tests/test_adapters_core.py::TestToolNormalisation::test_absent_tools
- context/scripts/tests/test_adapters_core.py::TestToolNormalisation::test_annotated_mapping_form
- context/scripts/tests/test_adapters_core.py::TestToolNormalisation::test_legacy_mcp_tools_key
- context/scripts/tests/test_adapters_core.py::TestToolNormalisation::test_plain_string_form
- context/scripts/tests/test_adapters_core.py::TestToolNormalisation::test_scalar_string_form
- context/scripts/tests/test_adapters_core.py::TestToolNormalisation::test_top_level_mapping_form
- context/scripts/tests/test_adapters_core.py::TestAdaptersCoreTools::test_capability_registry_extensibility
- context/scripts/tests/test_adapters_core.py::TestAdaptersCoreBudget::test_token_estimator
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_valid_agent
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_no_frontmatter
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_hardcoded_paths
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_missing_required_sections
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_context_acquisition_section_passes
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_legacy_required_sections_rejected
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_agent_template_scaffold_passes_validation
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_invalid_yaml_frontmatter
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_missing_required_fields
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_relative_paths_flagged
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_reminders_without_attribution
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_proper_attribution_passes
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_project_root_placeholders_allowed
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_nonexistent_standards_flagged
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_nonexistent_rules_flagged
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_nonexistent_skills_flagged
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_canonical_interruption_log_path_passes
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_legacy_interruption_log_path_rejected
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_interruption_log_wildcard_allowed
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_body_table_source_should_fail_when_file_does_not_exist
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_body_table_source_should_fail_when_section_does_not_exist
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_body_table_source_should_pass_when_citations_resolve
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_body_citation_should_fail_when_file_does_not_exist
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_body_citation_should_fail_when_section_does_not_exist
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_body_citation_should_pass_when_section_resolves
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_body_citation_error_should_report_file_line_number_when_it_fails
- context/scripts/tests/test_agent_validator.py::TestAgentValidator::test_body_table_without_source_column_should_be_ignored
- context/scripts/tests/test_claude_adapter.py::test_generate_claude_md
- context/scripts/tests/test_claude_adapter.py::test_generate_subagent_prompts
- context/scripts/tests/test_cli_dispatcher.py::test_target_normalization
- context/scripts/tests/test_cli_dispatcher.py::test_cli_parser_flags
- context/scripts/tests/test_cli_dispatcher.py::test_dry_run_leaves_disk_untouched
- context/scripts/tests/test_cli_dispatcher.py::test_smart_update_preserves_unchanged_files
- context/scripts/tests/test_cli_dispatcher.py::test_generation_execution_speed_benchmark
- context/scripts/tests/test_cli_dispatcher.py::test_ensure_root_gitignore
- context/scripts/tests/test_cli_dispatcher.py::test_load_configured_targets
- context/scripts/tests/test_cline_adapter.py::TestClineAdapter::test_generate_cline_md
- context/scripts/tests/test_cline_adapter.py::TestClineAdapter::test_generate_cline_rules
- context/scripts/tests/test_cline_adapter.py::TestClineAdapter::test_generate_cline_skills
- context/scripts/tests/test_e2e_compilation.py::test_e2e_full_compilation_all_targets
- context/scripts/tests/test_e2e_compilation.py::test_e2e_deterministic_reproducibility
- context/scripts/tests/test_e2e_compilation.py::test_e2e_synthetic_context_compilation
- context/scripts/tests/test_gemini_adapter.py::TestGeminiAdapter::test_generate_gemini_md
- context/scripts/tests/test_gemini_adapter.py::TestGeminiAdapter::test_generate_skills
- context/scripts/tests/test_gemini_adapter.py::TestGeminiAdapter::test_generate_skills_escapes_colon_in_description
- context/scripts/tests/test_github_adapter.py::test_generate_copilot_instructions
- context/scripts/tests/test_github_adapter.py::test_generate_prompts
- context/scripts/tests/test_github_adapter.py::test_generate_scoped_instructions
- context/scripts/tests/test_github_adapter.py::test_generate_scoped_instructions_with_exclude_agent
- context/scripts/tests/test_github_adapter.py::test_generate_workflows
- context/scripts/tests/test_openai_adapter.py::test_generate_system_prompts
- context/scripts/tests/test_openai_adapter.py::test_generate_tool_schemas
- context/scripts/tests/test_openai_adapter.py::test_generate_runner_harness
- context/scripts/tests/test_packaging.py::test_pyproject_toml_exists
- context/scripts/tests/test_packaging.py::test_generator_entrypoint_parser
- context/scripts/tests/test_packaging.py::test_drift_validator_callable
- context/scripts/tests/test_runtime_telemetry.py::test_format_tokens
- context/scripts/tests/test_runtime_telemetry.py::test_protobuf_wire_format_parsing
- context/scripts/tests/test_runtime_telemetry.py::test_antigravity_synthetic_extraction
- context/scripts/tests/test_runtime_telemetry.py::test_copilot_synthetic_extraction
- context/scripts/tests/test_runtime_telemetry.py::test_commit_message_updating
- context/scripts/tests/test_runtime_telemetry.py::test_live_antigravity_storage_sanity
- context/scripts/tests/test_runtime_telemetry.py::test_live_copilot_storage_sanity
- context/scripts/tests/test_runtime_telemetry.py::test_live_claude_storage_sanity
- context/scripts/tests/test_runtime_telemetry.py::test_cline_extract_delta_counts_assistant_metrics
- context/scripts/tests/test_runtime_telemetry.py::test_cline_extract_delta_accepts_wrapped_messages
- context/scripts/tests/test_runtime_telemetry.py::test_cline_extract_delta_session_switch_resets
- context/scripts/tests/test_runtime_telemetry.py::test_cline_extract_delta_falls_back_to_session_model
- context/scripts/tests/test_runtime_telemetry.py::test_cline_extract_delta_error_paths
- context/scripts/tests/test_runtime_telemetry.py::test_cline_find_active_session_matches_repo_and_picks_newest
- context/scripts/tests/test_runtime_telemetry.py::test_cline_registry_and_selection
- context/scripts/tests/test_runtime_telemetry.py::test_short_model_strips_provider_prefix
- context/scripts/tests/test_runtime_telemetry.py::test_update_commit_message_injects_tool_and_model
- context/scripts/tests/test_runtime_telemetry.py::test_update_commit_message_removes_stale_tokens
- context/scripts/tests/test_runtime_telemetry.py::test_live_cline_storage_sanity
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_valid_commit
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_invalid_no_scope
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_invalid_too_long
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_invalid_past_tense
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_valid_with_agent_session
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_merge_commit_allowed
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_empty_commit_fails
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_invalid_type
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_invalid_scope_uppercase
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_coauthor_format
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_agent_session_requires_coauthor
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_agent_session_tokens_mega_suffix
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_agent_session_tokens_lowercase_suffix
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_agent_session_hook_appended_form
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_agent_session_malformed_tokens_fails
- context/scripts/tests/test_validators.py::TestAgentSessionCorroboration::test_model_corroborated_for_cline
- context/scripts/tests/test_validators.py::TestAgentSessionCorroboration::test_model_contradicting_runtime_fails
- context/scripts/tests/test_validators.py::TestAgentSessionCorroboration::test_unconfirmable_model_fails
- context/scripts/tests/test_validators.py::TestAgentSessionCorroboration::test_third_party_tool_not_adjudicated
- context/scripts/tests/test_validators.py::TestEARSNotation::test_valid_requirements
- context/scripts/tests/test_validators.py::TestEARSNotation::test_invalid_requirements
- context/scripts/tests/test_validators.py::TestEARSNotation::test_ubiquitous_pattern
- context/scripts/tests/test_validators.py::TestEARSNotation::test_event_pattern
- context/scripts/tests/test_validators.py::TestEARSNotation::test_state_pattern
- context/scripts/tests/test_validators.py::TestEARSNotation::test_optional_pattern
- context/scripts/tests/test_validators.py::TestEARSNotation::test_forbidden_pattern
- context/scripts/tests/test_validators.py::TestEARSNotation::test_complex_pattern
- context/scripts/tests/test_validators.py::TestEARSNotation::test_non_ears_requirement
- context/scripts/tests/test_validators.py::TestEARSNotation::test_code_blocks_ignored
- context/scripts/tests/test_validators.py::TestBritishEnglish::test_valid_british_english
- context/scripts/tests/test_validators.py::TestBritishEnglish::test_invalid_american_english
- context/scripts/tests/test_validators.py::TestBritishEnglish::test_color_vs_colour
- context/scripts/tests/test_validators.py::TestBritishEnglish::test_behavior_vs_behaviour
- context/scripts/tests/test_validators.py::TestBritishEnglish::test_organize_vs_organise
- context/scripts/tests/test_validators.py::TestBritishEnglish::test_code_blocks_ignored
- context/scripts/tests/test_validators.py::TestBritishEnglish::test_inline_code_ignored
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_valid_metrics
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_invalid_metrics
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_metrics_log_location_under_build
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_metrics_log_requires_jsonl_suffix
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_metrics_log_rejects_repository_root
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_missing_required_field
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_invalid_timestamp
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_invalid_event
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_invalid_token_source
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_missing_tokens_fields
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_handoff_requires_to_field
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_empty_file_valid
- context/scripts/tests/test_validators.py::TestMetricsLogging::test_invalid_json
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_valid_interruptions
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_invalid_interruptions
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_missing_required_field
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_null_outcome_fields_allowed
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_invalid_type
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_invalid_timestamp
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_agent_at_prefix_rejected
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_invalid_decision
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_invalid_impact
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_options_must_be_array
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_mixed_tasks_rejected
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_legacy_filename_rejected
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_duplicate_ids_rejected
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_resolution_ref_must_resolve
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_resolution_record_resolves
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_empty_file_valid
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_invalid_json
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_interruptions_path_detection
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_interruption_log_requires_jsonl_suffix
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_main_auto_detects_interruptions_log
- context/scripts/tests/test_validators.py::TestInterruptionsLogging::test_main_auto_detects_metrics_log
- context/scripts/tests/test_validators.py::TestTypstFormatting::test_valid_formatting
- context/scripts/tests/test_validators.py::TestTypstFormatting::test_mermaid_insufficient_blank_lines
- context/scripts/tests/test_validators.py::TestTypstFormatting::test_section_heading_without_separator
- context/scripts/tests/test_validators.py::TestTypstFormatting::test_typst_skip_blocks_ignored
- context/scripts/tests/test_validators.py::TestTypstFormatting::test_headings_in_code_blocks_ignored
- context/scripts/tests/test_validators.py::TestWorkspaceOutputLocations::test_valid_output_paths
- context/scripts/tests/test_validators.py::TestWorkspaceOutputLocations::test_invalid_artefact_subdir
- context/scripts/tests/test_validators.py::TestWorkspaceOutputLocations::test_invalid_test_result_name
- context/scripts/tests/test_validators.py::TestUIDev::test_important_forbidden
- context/scripts/tests/test_validators.py::TestUIDev::test_raw_hex_forbidden
- context/scripts/tests/test_validators.py::TestUIDev::test_css_files_restriction
- context/scripts/tests/test_validators.py::TestSupabase::test_supabase_import_outside_database_service
- context/scripts/tests/test_validators.py::TestSupabase::test_supabase_import_inside_database_service_allowed
- context/scripts/tests/test_validators.py::TestSupabase::test_migration_audit_row_required
- context/scripts/tests/test_validators.py::TestTestingInvariants::test_forbidden_interaction_mock
- context/scripts/tests/test_validators.py::TestTestingInvariants::test_exempt_interaction_mock
- context/scripts/tests/test_validators.py::TestTypeScriptEnvironment::test_package_lock_flagged
- context/scripts/tests/test_validators.py::TestTypeScriptEnvironment::test_tsconfig_strictness
- context/scripts/tests/test_validators.py::TestTypeScriptEnvironment::test_workspaces_validation
- context/scripts/tests/test_validators.py::TestUITesting::test_banned_dependencies_flagged
- context/scripts/tests/test_validators.py::TestUITesting::test_puppeteer_core_allowed
- context/scripts/tests/test_validators.py::TestSecrets::test_private_key_flagged
- context/scripts/tests/test_validators.py::TestSecrets::test_env_file_with_secret_flagged
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_find_subrepos
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_query_upstream_head_success
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_query_upstream_head_failure
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_subrepo_fresh_when_commit_matches
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_subrepo_stale_with_changes_fails
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_subrepo_stale_without_changes_passes
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_subrepo_check_all_forces_stale_detection
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_subrepo_unreachable_network_handling
- context/scripts/tests/test_validators.py::TestSubrepoFreshness::test_main_cli_success
- context/scripts/tests/test_validators.py::TestLoggingTemplateDocs::test_template_documents_metrics_schema
- context/scripts/tests/test_validators.py::TestLoggingTemplateDocs::test_template_documents_interruption_schema
- context/scripts/tests/test_validators.py::TestLoggingTemplateDocs::test_agent_template_references_logging_template

---
Generated deterministically by `context/scripts/code-specs/spec_indexer.py scan` (zero LLM tokens). Consume via `repo-index.json`.

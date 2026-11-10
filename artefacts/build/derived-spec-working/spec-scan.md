# Spec Scan: start-here
Generated: 2026-11-10T21:02:13Z · mode: both · 63 files · languages: javascript, python

## Scan Warnings
- pytest: 292 collected (py3)

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
| `context/skills/derive-spec.md` | spec |
| `context/skills/requirements-elicitation.md` | requirements |
| `context/templates/derived-spec-template.md` | spec |
| `context/templates/requirements-template.md` | requirements |
| `context/workflows/README.md` | readme |
| `tests/context-unit-tests/README.md` | readme |

## Repository Map (symbols)
- `context/scripts/code-specs/spec_indexer.py` (2945 lines): const LANG_BY_SUFFIX(78), const FOREIGN_LANG_SUFFIXES(89), const FOREIGN_LANGS(104), const TS_LANGS(105), const DOC_GLOBS(108), const DOC_BASENAME_PATTERNS(120), const EXCLUDED_DIRS(131), const ROUTE_METHOD_ATTRS(154), const _JSX_TAG_RE(158), const _TS_IMPORT_NAMED(161), const _TS_IMPORT_DEFAULT(164), const _TS_FUNC(167), const _TS_ARROW(170), const _TS_CLASS(174), const _TS_IFACE(175), const _TS_TYPE(176), const _TS_REQUIRE(177), class CommentEntry(187), method CommentEntry.to_jsonb(205), class Symbol(216), method Symbol.to_jsonb(227), class FileRecord(247), method FileRecord.to_jsonb(255), class ApiEntry(267), method ApiEntry.to_jsonb(274), class ColumnDef(285), method ColumnDef.to_jsonb(290), class TableDef(295), method TableDef.to_jsonb(301), class UiComponent(311), method UiComponent.to_jsonb(319), class TestNode(331), method TestNode.to_jsonb(335), class DocRecord(340), method DocRecord.to_jsonb(344), class ConfigEntry(349), method ConfigEntry.to_jsonb(358), function rel(373), function language_of(378), function find_target_files(385), function _unparse(443), function _decorator_names(450), function _route_from_decorator(458), function _method_body(483), function analyze_python(495), function _destructured_props(574), function _is_component(587), function analyze_tsjs(591), const EXTRACTOR_CHOICES(679), const BACKEND_LANG_COVERAGE(689), const _EXTRACTOR_LABEL(697), function _cmd_ok(709), function probe_backends(717), function _likely_backend(738), function _stdlib_for(759), function resolve_plan(769), function _extractor_meta(818), function _ctags_kind(840), function analyze_ctags(859), const _TS_PACK_LANG(910), function analyze_tsjs_treesitter(919), const _ASTGREP_PATTERNS(1126), const _ASTGREP_KIND_RE(1134), const _ASTGREP_LANG_FLAG(1143), function analyze_tsjs_astgrep(1152), function analyze_tsjs_tsmorph(1231), const _SQL_CREATE(1276), const _SQL_SKIP_COLUMN(1280), function analyze_sql(1287), function _run(1329), function collect_tests(1337), function discover_docs(1395), function analyze_openapi(1427), const MAX_MAP_ROWS(1465), const MAX_API_ROWS(1466), const MAX_UI_ROWS(1467), const MAX_TEST_ROWS(1468), const MAX_SCHEMA_ROWS(1469), const MAX_CONFIG_ROWS(1470), const _CONFIG_ENV_NAMES(1477), const _CONFIG_PY_STEM_RE(1480), const _CONFIG_DATA_STEM_RE(1485), const _CONFIG_DATA_EXCLUDE_RE(1490), const _CONFIG_SECRET_RE(1494), const _CONFIG_FEATURE_RE(1498), const _CONFIG_BOOL_VALUES(1501), const _CONFIG_TEST_PARTS(1504), const _MAX_VALUE_HINT(1507), const _HISTORY_COMMIT_FMT(1510), const _HISTORY_HASH_RE(1511), const _MAX_HISTORY_RENAMES(1512), const MAX_HISTORY_ROWS(1513), function _skip_config_path(1516), function _config_value_hint(1524), function _config_is_feature(1536), function _config_env_call(1540), function _collect_config_env(1572), function _collect_config_py_module(1592), function _config_key_line(1634), function _collect_config_data_file(1647), function collect_config(1679), function collect_history(1778), const _MAX_COMMENT_TEXT(1858), const MAX_COMMENT_ROWS(1864), const _LEADING_GAP(1865), const _MAX_COMMENT_ENTRIES(1866), const _COMMENT_MARKER(1868), function _shorten_comment(1871), function _mask_code_strings(1877), function _clean_comment_text(1909), function _group_comment_lines(1929), function _python_comments(1950), function _ts_comments(1994), function _sql_comments(2028), function _symbol_ref(2052), function _attach_leading_blocks(2056), function _attach_inline_comments(2094), function _attach_sql_leading(2116), function collect_comments(2148), function _default_out_dir(2308), function render_spec_scan(2313), function run_scan(2468), const _CITATION_RE(2627), const _COVERAGE_TIERS(2636), const _COVERAGE_TIER_RE(2641), const _COVERAGE_PERCENT_RE(2644), const _COVERAGE_CONFIDENCE_RE(2645), const _COVERAGE_HEADING_RE(2648), const _COVERAGE_NON_CONTENT_RE(2651), function _confidence_line_errors(2657), function check_doc_coverage(2682), function _line_text(2734), function run_verify(2748), function main(2840)
- `context/scripts/code-specs/ts_extract.mjs` (122 lines): function push(35)
- `context/scripts/generators/adapters/claude/generator.py` (92 lines): function _extract_model_mappings(8), function generate_claude_md(34), function generate_subagent_prompts(60)
- `context/scripts/generators/adapters/cline/generator.py` (151 lines): function _extract_cline_model_mappings(10), function generate_cline_md(39), function generate_cline_rules(71), function generate_cline_skills(97)
- `context/scripts/generators/adapters/core/agents_md.py` (73 lines): function generate_agents_md(6)
- `context/scripts/generators/adapters/core/budget.py` (31 lines): class DeliveryStrategy(4), class TokenEstimator(10), method TokenEstimator.__init__(15), method TokenEstimator.estimate_tokens(18), method TokenEstimator.recommend_strategy(24)
- `context/scripts/generators/adapters/core/loader.py` (125 lines): function extract_frontmatter(14), function normalise_tools(22), function load_canonical_context(49)
- `context/scripts/generators/adapters/core/models.py` (58 lines): class CanonicalRule(5), class CanonicalStandard(11), class CanonicalSkill(17), class CanonicalAgent(25), class CanonicalPersona(39), class Phase(46), class WorkflowDAG(54)
- `context/scripts/generators/adapters/core/tools.py` (22 lines): class CapabilityRegistry(1), method CapabilityRegistry.__init__(6), method CapabilityRegistry.register_capability(9), method CapabilityRegistry.get_mapping(17)
- `context/scripts/generators/adapters/gemini/generator.py` (135 lines): function generate_skills(9), function _extract_model_mappings(85), function generate_gemini_md(111)
- `context/scripts/generators/adapters/github/generator.py` (180 lines): function generate_prompts(8), function generate_copilot_instructions(44), function generate_scoped_instructions(66), function generate_workflows(143)
- `context/scripts/generators/adapters/openai/generator.py` (133 lines): function generate_system_prompts(8), function generate_tool_schemas(46), function generate_runner_harness(75)
- `context/scripts/generators/generate_adapters.py` (508 lines): const _REPO_ROOT(24), const SUPPORTED_TARGETS(55), const TARGET_ALIASES(57), const IGNORED_BLOCK(74), function ensure_root_gitignore(91), function normalize_target(128), function load_configured_targets(137), function get_adapter_projections(163), function run_generation(266), function build_parser(348), function main(468)
- `context/scripts/prepare-commit-msg.py` (848 lines): class ExtractionResult(40), function format_tokens(51), function short_model(60), function get_git_repo_root(68), function get_watermark_path(79), function read_watermark(84), function write_watermark(95), function _decode_varint(109), function parse_protobuf_fields(125), class BaseExtractor(163), method BaseExtractor.is_available(167), method BaseExtractor.find_active_session(171), method BaseExtractor.extract_delta(175), class AntigravityExtractor(180), method AntigravityExtractor.__init__(184), method AntigravityExtractor.is_available(191), method AntigravityExtractor.find_active_session(194), method AntigravityExtractor.extract_delta(219), class CopilotExtractor(298), method CopilotExtractor.__init__(302), method CopilotExtractor.is_available(311), method CopilotExtractor.find_active_session(314), method CopilotExtractor.extract_delta(349), class ClaudeExtractor(421), method ClaudeExtractor.is_available(425), method ClaudeExtractor.find_active_session(428), method ClaudeExtractor.extract_delta(443), class CodexExtractor(514), method CodexExtractor.is_available(518), method CodexExtractor.find_active_session(521), method CodexExtractor.extract_delta(524), class ClineExtractor(528), method ClineExtractor.__init__(546), method ClineExtractor.is_available(560), method ClineExtractor._load_session_meta(564), method ClineExtractor.find_active_session(572), method ClineExtractor.extract_delta(597), const EXTRACTORS(681), function select_extractor(694), function _set_trailer_field(724), function update_commit_message(731), function main(779)
- `context/scripts/tests/conftest.py` (131 lines): function fixtures_dir(8), function valid_commit(14), function invalid_commit_no_scope(20), function invalid_commit_too_long(26), function invalid_commit_past_tense(32), function valid_commit_with_agent_session(38), function merge_commit(44), function invalid_commit_no_body(50), function valid_requirements(56), function invalid_requirements(62), function valid_british_english(68), function invalid_british_english(74), function valid_metrics(80), function invalid_metrics(86), function valid_interruptions(92), function invalid_interruptions(98), function test_workflow(104), function valid_agent(110), function invalid_agent_no_frontmatter(116), function invalid_agent_hardcoded_paths(122), function invalid_agent_missing_sections(128)
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
- `context/scripts/tests/test_spec_indexer.py` (554 lines): const INDEXER_PATH(21), const REPO_ROOT(22), const CONTEXT_DIR(23), const SKILLS_DIR(24), const AGENTS_DIR(25), const WORKFLOWS_DIR(26), const KNOWN_AGENTS(35), const SKILL_FILES(38), const TSX_FIXTURE(40), function _parse_frontmatter(61), function _validate_skill(74), function _validate_workflow(88), function _valid_workflow(144), function _scan(161), class TestSkillFrontmatterSchema(174), method TestSkillFrontmatterSchema.test_derive_skills_have_valid_frontmatter(175), method TestSkillFrontmatterSchema.test_skill_name_matches_filename_stem(180), method TestSkillFrontmatterSchema.test_skill_globs_is_list_of_glob_strings(185), class TestWorkflowPhaseSchema(197), method TestWorkflowPhaseSchema.test_all_real_workflows_pass_schema(198), method TestWorkflowPhaseSchema.test_rejects_duplicate_phase_ids(204), method TestWorkflowPhaseSchema.test_rejects_unresolvable_depends_on(210), method TestWorkflowPhaseSchema.test_rejects_unknown_agent(216), method TestWorkflowPhaseSchema.test_accepts_at_prefix_and_inline_comment_agents(222), method TestWorkflowPhaseSchema.test_rejects_non_boolean_phase_gate(227), method TestWorkflowPhaseSchema.test_gate_phase_without_quality_gates_entry_is_allowed(233), method TestWorkflowPhaseSchema.test_rejects_quality_gate_unknown_phase(239), method TestWorkflowPhaseSchema.test_accepts_evidence_style_quality_gate_without_gate_key(245), class TestPythonExtraction(257), method TestPythonExtraction.test_symbols_and_constants(283), method TestPythonExtraction.test_imports_recorded(297), method TestPythonExtraction.test_route_decorators_produce_api_entries(304), class TestTsJsExtraction(321), method TestTsJsExtraction.test_components_props_and_usage(322), method TestTsJsExtraction.test_scan_aggregates_ui_components(337), class TestSqlParsing(356), method TestSqlParsing.test_create_table_columns(370), class TestVerifyOnSyntheticRepo(390), method TestVerifyOnSyntheticRepo.test_verify_passes_index_then_fails_when_source_removed(391), method TestVerifyOnSyntheticRepo.test_verify_doc_checks_cited_file_lines(402), class TestExtractorSmoke(420), method TestExtractorSmoke.test_invalid_extractor_exits_nonzero(421), method TestExtractorSmoke.test_meta_extractors_provenance_populated(426), function _write_source(444), const GOOD_DOC(451), class TestDocCoverage(479), method TestDocCoverage.test_coverage_passes_when_every_content_subsection_confident(480), method TestDocCoverage.test_coverage_can_be_disabled_by_default(486), method TestDocCoverage.test_coverage_fails_on_missing_confidence_line(493), method TestDocCoverage.test_coverage_reports_missing_tier(498), method TestDocCoverage.test_coverage_reports_missing_percentage(504), method TestDocCoverage.test_coverage_reports_missing_file_line_citation(510), method TestDocCoverage.test_coverage_reports_band_mismatch(516), method TestDocCoverage.test_coverage_accepts_markdown_file_line_citations(521), method TestDocCoverage.test_coverage_boundary_85_allows_verified_or_needs_confirmation(526), method TestDocCoverage.test_coverage_skips_placeholder_and_structural_headings(532), method TestDocCoverage.test_coverage_fails_via_run_verify_and_lists_subsection(542), method TestDocCoverage.test_cli_require_coverage_requires_doc(551)
- `context/scripts/tests/test_spec_indexer_comments.py` (358 lines): const INDEXER_PATH(19), const REPO_ROOT(20), function _write(30), function _scan(38), function _entries(46), function _symbol(50), const PY_FIXTURE(55), class TestPythonCommentsTokenize(72), method TestPythonCommentsTokenize.test_comment_markers_inside_strings_are_never_captured(73), method TestPythonCommentsTokenize.test_doc_block_above_definition_attaches_leading_and_fills_docstring(82), method TestPythonCommentsTokenize.test_trailing_comment_does_not_join_the_doc_block(90), method TestPythonCommentsTokenize.test_body_comments_attach_inline_within_symbol_span(102), method TestPythonCommentsTokenize.test_orphan_comments_stay_in_the_stream_unattached(110), class TestPythonDocstrings(121), method TestPythonDocstrings.test_module_docstring_is_an_orphan_docstring_entry(122), method TestPythonDocstrings.test_function_docstring_attaches_to_symbol(130), method TestPythonDocstrings.test_class_and_method_docstrings_attach(145), const TS_FIXTURE(156), class TestTsJsComments(174), method TestTsJsComments.test_jsdoc_attaches_as_docstring_and_sets_symbol_docstring(175), method TestTsJsComments.test_line_comment_inside_string_is_masked(182), method TestTsJsComments.test_line_doc_block_above_function_attaches_leading(188), method TestTsJsComments.test_block_comment_is_orphan_until_attached(195), const SQL_FIXTURE(203), class TestSqlComments(216), method TestSqlComments.test_double_dash_comment_attaches_to_nearest_table(217), method TestSqlComments.test_column_comment_attaches_to_nearest_column(227), method TestSqlComments.test_block_comment_attaches_to_nearest_table(236), class TestIndexIntegration(247), method TestIndexIntegration.test_comments_key_sorted_and_deterministic(248), method TestIndexIntegration.test_verify_index_checks_comment_citations(259), method TestIndexIntegration.test_render_spec_scan_shows_comment_map(267), method TestIndexIntegration.test_render_spec_scan_says_none_when_no_comments(307), method TestIndexIntegration.test_cli_scan_emits_comments_key(327), class TestRealRepo(339), method TestRealRepo.test_real_repo_module_docstring_is_indexed(340), method TestRealRepo.test_real_repo_comment_stream_uses_exact_file_lines(349)
- `context/scripts/tests/test_spec_indexer_config.py` (183 lines): const INDEXER_PATH(12), const REPO_ROOT(13), const ENV_TEMPLATE(21), const SETTINGS_PY(29), function _write_tree(40), function _scan(48), function _config_map(56), class TestConfigSources(60), method TestConfigSources.test_config_should_extract_env_template_keys_when_env_file_present(61), method TestConfigSources.test_config_should_extract_module_constants_and_env_defaults_when_settings_module_present(76), method TestConfigSources.test_config_should_extract_scalar_keys_when_yaml_config_present(91), method TestConfigSources.test_config_should_extract_scalar_keys_when_json_config_present(112), method TestConfigSources.test_config_should_ignore_non_config_files_when_names_do_not_match(124), method TestConfigSources.test_config_should_keep_first_source_value_when_key_defined_in_multiple_sources(139), method TestConfigSources.test_config_should_be_deterministic_when_scan_repeated(151), class TestConfigVerify(165), method TestConfigVerify.test_verify_should_fail_when_config_source_removed_after_indexing(166), class TestRealRepo(176), method TestRealRepo.test_config_should_redact_secrets_when_scanning_real_repo_env_template(177)
- `context/scripts/tests/test_spec_indexer_extractors.py` (249 lines): const INDEXER_PATH(14), const REPO_ROOT(15), const TSX_FIXTURE(24), function _scan(54), function _all_symbols(62), function _python_symbols(70), class TestProbeAndPlan(74), method TestProbeAndPlan.test_probe_backends_never_raises(75), method TestProbeAndPlan.test_auto_plan_python_uses_stdlib_ast(80), method TestProbeAndPlan.test_auto_plan_ts_prefers_treesitter_when_available(87), method TestProbeAndPlan.test_auto_plan_ts_degrades_to_astgrep_then_regex(93), method TestProbeAndPlan.test_explicit_unavailable_backend_is_an_error(104), method TestProbeAndPlan.test_explicit_ts_morph_unavailable_degrades_quietly(111), method TestProbeAndPlan.test_cli_rejects_unknown_extractor(118), class TestParity(124), method TestParity.test_auto_and_stdlib_python_symbols_identical(125), method TestParity.test_auto_is_superset_of_stdlib(134), method TestParity.test_meta_provenance_fields_present(143), class TestCtagsBackend(162), method TestCtagsBackend.test_python_file_yields_symbols(163), method TestCtagsBackend.test_ts_file_method_scoped_names(175), class TestTreeSitterBackend(186), method TestTreeSitterBackend.test_fixture_richer_than_regex(187), method TestTreeSitterBackend.test_fixture_symbols_kinds(217), class TestAstGrepBackend(232), method TestAstGrepBackend.test_fixture_interfaces_types_and_consts(233)
- `context/scripts/tests/test_spec_indexer_history.py` (264 lines): const INDEXER_PATH(21), const REPO_ROOT(22), function _git(31), function _init_repo(41), function _commit(48), function _scan(58), class TestHistoryPresence(66), method TestHistoryPresence.test_history_should_list_commit_subjects_newest_first(67), method TestHistoryPresence.test_history_should_record_rename_clues_when_files_moved(84), method TestHistoryPresence.test_history_should_respect_history_cap_with_capped_flag(115), method TestHistoryPresence.test_history_should_be_deterministic_across_scans(128), class TestHistoryAbsent(138), method TestHistoryAbsent.test_history_should_be_absent_when_repo_has_no_git_metadata(139), method TestHistoryAbsent.test_history_should_be_absent_when_git_repo_has_no_commits(146), method TestHistoryAbsent.test_history_cap_zero_should_disable_the_git_pull(153), class TestHistoryCli(161), method TestHistoryCli.test_cli_history_flag_should_wire_into_run_scan(162), method TestHistoryCli.test_cli_default_history_cap_should_be_200(175), class TestRenderHistory(186), method TestRenderHistory.test_render_spec_scan_should_list_subjects_and_renames(187), method TestRenderHistory.test_render_spec_scan_should_say_absent_when_no_history(224), class TestRealRepo(246), method TestRealRepo.test_history_for_real_repo_should_match_latest_commit_subject(247), method TestRealRepo.test_history_for_real_repo_should_include_rename_clues(258)
- `context/scripts/tests/test_validators.py` (1268 lines): class TestConventionalCommits(65), method TestConventionalCommits.test_valid_commit(68), method TestConventionalCommits.test_invalid_no_scope(75), method TestConventionalCommits.test_invalid_too_long(82), method TestConventionalCommits.test_invalid_no_body(89), method TestConventionalCommits.test_invalid_past_tense(96), method TestConventionalCommits.test_valid_with_agent_session(103), method TestConventionalCommits.test_merge_commit_allowed(109), method TestConventionalCommits.test_empty_commit_fails(115), method TestConventionalCommits.test_invalid_type(122), method TestConventionalCommits.test_invalid_scope_uppercase(129), method TestConventionalCommits.test_coauthor_format(136), method TestConventionalCommits.test_agent_session_requires_coauthor(145), method TestConventionalCommits.test_agent_session_tokens_mega_suffix(154), method TestConventionalCommits.test_agent_session_tokens_lowercase_suffix(165), method TestConventionalCommits.test_agent_session_hook_appended_form(176), method TestConventionalCommits.test_agent_session_malformed_tokens_fails(187), class TestAgentSessionCorroboration(198), method TestAgentSessionCorroboration._cline_session_for_repo(206), method TestAgentSessionCorroboration._agent_commit(225), method TestAgentSessionCorroboration.test_model_corroborated_for_cline(233), method TestAgentSessionCorroboration.test_model_contradicting_runtime_fails(242), method TestAgentSessionCorroboration.test_unconfirmable_model_fails(252), method TestAgentSessionCorroboration.test_third_party_tool_not_adjudicated(261), class TestEARSNotation(267), method TestEARSNotation.test_valid_requirements(270), method TestEARSNotation.test_invalid_requirements(275), method TestEARSNotation.test_ubiquitous_pattern(281), method TestEARSNotation.test_event_pattern(286), method TestEARSNotation.test_state_pattern(290), method TestEARSNotation.test_optional_pattern(294), method TestEARSNotation.test_forbidden_pattern(298), method TestEARSNotation.test_complex_pattern(302), method TestEARSNotation.test_non_ears_requirement(308), method TestEARSNotation.test_code_blocks_ignored(313), class TestBritishEnglish(329), method TestBritishEnglish.test_valid_british_english(332), method TestBritishEnglish.test_invalid_american_english(337), method TestBritishEnglish.test_color_vs_colour(344), method TestBritishEnglish.test_behavior_vs_behaviour(356), method TestBritishEnglish.test_organize_vs_organise(367), method TestBritishEnglish.test_code_blocks_ignored(378), method TestBritishEnglish.test_inline_code_ignored(393), class TestMetricsLogging(403), method TestMetricsLogging.test_valid_metrics(406), method TestMetricsLogging.test_invalid_metrics(411), method TestMetricsLogging.test_metrics_log_location_under_build(416), method TestMetricsLogging.test_metrics_log_requires_jsonl_suffix(420), method TestMetricsLogging.test_metrics_log_rejects_repository_root(425), method TestMetricsLogging.test_missing_required_field(430), method TestMetricsLogging.test_invalid_timestamp(443), method TestMetricsLogging.test_invalid_event(456), method TestMetricsLogging.test_invalid_token_source(469), method TestMetricsLogging.test_missing_tokens_fields(482), method TestMetricsLogging.test_handoff_requires_to_field(495), method TestMetricsLogging.test_empty_file_valid(509), method TestMetricsLogging.test_invalid_json(517), class TestInterruptionsLogging(527), method TestInterruptionsLogging._question(531), method TestInterruptionsLogging.test_valid_interruptions(546), method TestInterruptionsLogging.test_invalid_interruptions(551), method TestInterruptionsLogging.test_missing_required_field(556), method TestInterruptionsLogging.test_null_outcome_fields_allowed(563), method TestInterruptionsLogging.test_invalid_type(568), method TestInterruptionsLogging.test_invalid_timestamp(574), method TestInterruptionsLogging.test_agent_at_prefix_rejected(580), method TestInterruptionsLogging.test_invalid_decision(586), method TestInterruptionsLogging.test_invalid_impact(602), method TestInterruptionsLogging.test_options_must_be_array(619), method TestInterruptionsLogging.test_mixed_tasks_rejected(637), method TestInterruptionsLogging.test_legacy_filename_rejected(647), method TestInterruptionsLogging.test_duplicate_ids_rejected(654), method TestInterruptionsLogging.test_resolution_ref_must_resolve(661), method TestInterruptionsLogging.test_resolution_record_resolves(683), method TestInterruptionsLogging.test_empty_file_valid(704), method TestInterruptionsLogging.test_invalid_json(710), method TestInterruptionsLogging.test_interruptions_path_detection(717), method TestInterruptionsLogging.test_interruption_log_requires_jsonl_suffix(723), method TestInterruptionsLogging.test_main_auto_detects_interruptions_log(729), method TestInterruptionsLogging.test_main_auto_detects_metrics_log(742), class TestTypstFormatting(767), method TestTypstFormatting.test_valid_formatting(770), method TestTypstFormatting.test_mermaid_insufficient_blank_lines(786), method TestTypstFormatting.test_section_heading_without_separator(807), method TestTypstFormatting.test_typst_skip_blocks_ignored(826), method TestTypstFormatting.test_headings_in_code_blocks_ignored(838), class TestWorkspaceOutputLocations(856), method TestWorkspaceOutputLocations.test_valid_output_paths(859), method TestWorkspaceOutputLocations.test_invalid_artefact_subdir(870), method TestWorkspaceOutputLocations.test_invalid_test_result_name(877), class TestUIDev(885), method TestUIDev.test_important_forbidden(888), method TestUIDev.test_raw_hex_forbidden(896), method TestUIDev.test_css_files_restriction(904), class TestSupabase(915), method TestSupabase.test_supabase_import_outside_database_service(918), method TestSupabase.test_supabase_import_inside_database_service_allowed(927), method TestSupabase.test_migration_audit_row_required(935), class TestTestingInvariants(953), method TestTestingInvariants.test_forbidden_interaction_mock(956), method TestTestingInvariants.test_exempt_interaction_mock(964), class TestTypeScriptEnvironment(972), method TestTypeScriptEnvironment.test_package_lock_flagged(975), method TestTypeScriptEnvironment.test_tsconfig_strictness(983), method TestTypeScriptEnvironment.test_workspaces_validation(996), class TestUITesting(1010), method TestUITesting.test_banned_dependencies_flagged(1013), method TestUITesting.test_puppeteer_core_allowed(1027), class TestSecrets(1039), method TestSecrets.test_private_key_flagged(1042), method TestSecrets.test_env_file_with_secret_flagged(1050), class TestSubrepoFreshness(1059), method TestSubrepoFreshness.test_find_subrepos(1062), method TestSubrepoFreshness.test_query_upstream_head_success(1084), method TestSubrepoFreshness.test_query_upstream_head_failure(1095), method TestSubrepoFreshness.test_subrepo_fresh_when_commit_matches(1106), method TestSubrepoFreshness.test_subrepo_stale_with_changes_fails(1126), method TestSubrepoFreshness.test_subrepo_stale_without_changes_passes(1148), method TestSubrepoFreshness.test_subrepo_check_all_forces_stale_detection(1168), method TestSubrepoFreshness.test_subrepo_unreachable_network_handling(1188), method TestSubrepoFreshness.test_main_cli_success(1211), class TestLoggingTemplateDocs(1233), method TestLoggingTemplateDocs.test_template_documents_metrics_schema(1243), method TestLoggingTemplateDocs.test_template_documents_interruption_schema(1249), method TestLoggingTemplateDocs.test_agent_template_references_logging_template(1263)
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
- `context/scripts/validators/workspace_conventions.py` (703 lines): const VALID_OUTPUT_TOP_DIRS(24), const VALID_ARTEFACT_SUBDIRS(25), const TEST_RESULT_PATTERN(27), const REVIEW_PATTERN(28), const IMPL_DOC_PATTERN(29), function validate_output_path(32), function validate_output_paths(88), const VALID_COMMIT_TYPES(98), const COMMIT_SUBJECT_PATTERN(99), const COAUTHOR_PATTERN(100), const AGENT_SESSION_PATTERN(103), const TOOL_FIELD_PATTERN(125), const MODEL_FIELD_PATTERN(126), const _RUNTIME_TELEMETRY_MODULE(133), function _load_runtime_telemetry(136), function corroborate_agent_session(150), const BODY_EXCLUDED_PREFIXES(197), function _has_explanatory_body(207), function validate_commit_message(219), const REQUIRED_METRICS_FIELDS(300), const VALID_METRICS_EVENTS(301), const VALID_TOKEN_SOURCES(302), function validate_metrics_entry(305), function validate_metrics_file(353), const INTERRUPTIONS_DIRNAME(383), const INTERRUPTION_BASE_FIELDS(385), const VALID_INTERRUPTION_TYPES(386), const VALID_INTERRUPTION_IMPACTS(387), const VALID_INTERRUPTION_DECISIONS(388), const INTERRUPTION_TYPE_FIELDS(390), const INTERRUPTION_NULLABLE_FIELDS(399), const INTERRUPTION_TS_PATTERN(401), function is_interruptions_log(404), function validate_interruptions_entry(410), function validate_interruptions_file(490), function _auto_detect(567), function main(614)
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
- context/scripts/tests/test_spec_indexer.py::TestSkillFrontmatterSchema::test_derive_skills_have_valid_frontmatter
- context/scripts/tests/test_spec_indexer.py::TestSkillFrontmatterSchema::test_skill_name_matches_filename_stem
- context/scripts/tests/test_spec_indexer.py::TestSkillFrontmatterSchema::test_skill_globs_is_list_of_glob_strings
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_all_real_workflows_pass_schema
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_rejects_duplicate_phase_ids
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_rejects_unresolvable_depends_on
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_rejects_unknown_agent
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_accepts_at_prefix_and_inline_comment_agents
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_rejects_non_boolean_phase_gate
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_gate_phase_without_quality_gates_entry_is_allowed
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_rejects_quality_gate_unknown_phase
- context/scripts/tests/test_spec_indexer.py::TestWorkflowPhaseSchema::test_accepts_evidence_style_quality_gate_without_gate_key
- context/scripts/tests/test_spec_indexer.py::TestPythonExtraction::test_symbols_and_constants
- context/scripts/tests/test_spec_indexer.py::TestPythonExtraction::test_imports_recorded
- context/scripts/tests/test_spec_indexer.py::TestPythonExtraction::test_route_decorators_produce_api_entries
- context/scripts/tests/test_spec_indexer.py::TestTsJsExtraction::test_components_props_and_usage
- context/scripts/tests/test_spec_indexer.py::TestTsJsExtraction::test_scan_aggregates_ui_components
- context/scripts/tests/test_spec_indexer.py::TestSqlParsing::test_create_table_columns
- context/scripts/tests/test_spec_indexer.py::TestVerifyOnSyntheticRepo::test_verify_passes_index_then_fails_when_source_removed
- context/scripts/tests/test_spec_indexer.py::TestVerifyOnSyntheticRepo::test_verify_doc_checks_cited_file_lines
- context/scripts/tests/test_spec_indexer.py::TestExtractorSmoke::test_invalid_extractor_exits_nonzero
- context/scripts/tests/test_spec_indexer.py::TestExtractorSmoke::test_meta_extractors_provenance_populated
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_passes_when_every_content_subsection_confident
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_can_be_disabled_by_default
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_fails_on_missing_confidence_line
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_reports_missing_tier
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_reports_missing_percentage
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_reports_missing_file_line_citation
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_reports_band_mismatch
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_accepts_markdown_file_line_citations
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_boundary_85_allows_verified_or_needs_confirmation
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_skips_placeholder_and_structural_headings
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_coverage_fails_via_run_verify_and_lists_subsection
- context/scripts/tests/test_spec_indexer.py::TestDocCoverage::test_cli_require_coverage_requires_doc
- context/scripts/tests/test_spec_indexer_comments.py::TestPythonCommentsTokenize::test_comment_markers_inside_strings_are_never_captured
- context/scripts/tests/test_spec_indexer_comments.py::TestPythonCommentsTokenize::test_doc_block_above_definition_attaches_leading_and_fills_docstring
- context/scripts/tests/test_spec_indexer_comments.py::TestPythonCommentsTokenize::test_trailing_comment_does_not_join_the_doc_block
- context/scripts/tests/test_spec_indexer_comments.py::TestPythonCommentsTokenize::test_body_comments_attach_inline_within_symbol_span
- context/scripts/tests/test_spec_indexer_comments.py::TestPythonCommentsTokenize::test_orphan_comments_stay_in_the_stream_unattached
- context/scripts/tests/test_spec_indexer_comments.py::TestPythonDocstrings::test_module_docstring_is_an_orphan_docstring_entry
- context/scripts/tests/test_spec_indexer_comments.py::TestPythonDocstrings::test_function_docstring_attaches_to_symbol
- context/scripts/tests/test_spec_indexer_comments.py::TestPythonDocstrings::test_class_and_method_docstrings_attach
- context/scripts/tests/test_spec_indexer_comments.py::TestTsJsComments::test_jsdoc_attaches_as_docstring_and_sets_symbol_docstring
- context/scripts/tests/test_spec_indexer_comments.py::TestTsJsComments::test_line_comment_inside_string_is_masked
- context/scripts/tests/test_spec_indexer_comments.py::TestTsJsComments::test_line_doc_block_above_function_attaches_leading
- context/scripts/tests/test_spec_indexer_comments.py::TestTsJsComments::test_block_comment_is_orphan_until_attached
- context/scripts/tests/test_spec_indexer_comments.py::TestSqlComments::test_double_dash_comment_attaches_to_nearest_table
- context/scripts/tests/test_spec_indexer_comments.py::TestSqlComments::test_column_comment_attaches_to_nearest_column
- context/scripts/tests/test_spec_indexer_comments.py::TestSqlComments::test_block_comment_attaches_to_nearest_table
- context/scripts/tests/test_spec_indexer_comments.py::TestIndexIntegration::test_comments_key_sorted_and_deterministic
- context/scripts/tests/test_spec_indexer_comments.py::TestIndexIntegration::test_verify_index_checks_comment_citations
- context/scripts/tests/test_spec_indexer_comments.py::TestIndexIntegration::test_render_spec_scan_shows_comment_map
- context/scripts/tests/test_spec_indexer_comments.py::TestIndexIntegration::test_render_spec_scan_says_none_when_no_comments
- context/scripts/tests/test_spec_indexer_comments.py::TestIndexIntegration::test_cli_scan_emits_comments_key
- context/scripts/tests/test_spec_indexer_comments.py::TestRealRepo::test_real_repo_module_docstring_is_indexed
- context/scripts/tests/test_spec_indexer_comments.py::TestRealRepo::test_real_repo_comment_stream_uses_exact_file_lines
- context/scripts/tests/test_spec_indexer_config.py::TestConfigSources::test_config_should_extract_env_template_keys_when_env_file_present
- context/scripts/tests/test_spec_indexer_config.py::TestConfigSources::test_config_should_extract_module_constants_and_env_defaults_when_settings_module_present
- context/scripts/tests/test_spec_indexer_config.py::TestConfigSources::test_config_should_extract_scalar_keys_when_yaml_config_present
- context/scripts/tests/test_spec_indexer_config.py::TestConfigSources::test_config_should_extract_scalar_keys_when_json_config_present
- context/scripts/tests/test_spec_indexer_config.py::TestConfigSources::test_config_should_ignore_non_config_files_when_names_do_not_match
- context/scripts/tests/test_spec_indexer_config.py::TestConfigSources::test_config_should_keep_first_source_value_when_key_defined_in_multiple_sources
- context/scripts/tests/test_spec_indexer_config.py::TestConfigSources::test_config_should_be_deterministic_when_scan_repeated
- context/scripts/tests/test_spec_indexer_config.py::TestConfigVerify::test_verify_should_fail_when_config_source_removed_after_indexing
- context/scripts/tests/test_spec_indexer_config.py::TestRealRepo::test_config_should_redact_secrets_when_scanning_real_repo_env_template
- context/scripts/tests/test_spec_indexer_extractors.py::TestProbeAndPlan::test_probe_backends_never_raises
- context/scripts/tests/test_spec_indexer_extractors.py::TestProbeAndPlan::test_auto_plan_python_uses_stdlib_ast
- context/scripts/tests/test_spec_indexer_extractors.py::TestProbeAndPlan::test_auto_plan_ts_prefers_treesitter_when_available
- context/scripts/tests/test_spec_indexer_extractors.py::TestProbeAndPlan::test_auto_plan_ts_degrades_to_astgrep_then_regex
- context/scripts/tests/test_spec_indexer_extractors.py::TestProbeAndPlan::test_explicit_unavailable_backend_is_an_error
- context/scripts/tests/test_spec_indexer_extractors.py::TestProbeAndPlan::test_explicit_ts_morph_unavailable_degrades_quietly
- context/scripts/tests/test_spec_indexer_extractors.py::TestProbeAndPlan::test_cli_rejects_unknown_extractor
- context/scripts/tests/test_spec_indexer_extractors.py::TestParity::test_auto_and_stdlib_python_symbols_identical
- context/scripts/tests/test_spec_indexer_extractors.py::TestParity::test_auto_is_superset_of_stdlib
- context/scripts/tests/test_spec_indexer_extractors.py::TestParity::test_meta_provenance_fields_present
- context/scripts/tests/test_spec_indexer_extractors.py::TestCtagsBackend::test_python_file_yields_symbols
- context/scripts/tests/test_spec_indexer_extractors.py::TestCtagsBackend::test_ts_file_method_scoped_names
- context/scripts/tests/test_spec_indexer_extractors.py::TestTreeSitterBackend::test_fixture_richer_than_regex
- context/scripts/tests/test_spec_indexer_extractors.py::TestTreeSitterBackend::test_fixture_symbols_kinds
- context/scripts/tests/test_spec_indexer_extractors.py::TestAstGrepBackend::test_fixture_interfaces_types_and_consts
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryPresence::test_history_should_list_commit_subjects_newest_first
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryPresence::test_history_should_record_rename_clues_when_files_moved
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryPresence::test_history_should_respect_history_cap_with_capped_flag
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryPresence::test_history_should_be_deterministic_across_scans
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryAbsent::test_history_should_be_absent_when_repo_has_no_git_metadata
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryAbsent::test_history_should_be_absent_when_git_repo_has_no_commits
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryAbsent::test_history_cap_zero_should_disable_the_git_pull
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryCli::test_cli_history_flag_should_wire_into_run_scan
- context/scripts/tests/test_spec_indexer_history.py::TestHistoryCli::test_cli_default_history_cap_should_be_200
- context/scripts/tests/test_spec_indexer_history.py::TestRenderHistory::test_render_spec_scan_should_list_subjects_and_renames
- context/scripts/tests/test_spec_indexer_history.py::TestRenderHistory::test_render_spec_scan_should_say_absent_when_no_history
- context/scripts/tests/test_spec_indexer_history.py::TestRealRepo::test_history_for_real_repo_should_match_latest_commit_subject
- context/scripts/tests/test_spec_indexer_history.py::TestRealRepo::test_history_for_real_repo_should_include_rename_clues
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_valid_commit
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_invalid_no_scope
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_invalid_too_long
- context/scripts/tests/test_validators.py::TestConventionalCommits::test_invalid_no_body
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
… 92 more test node-ids

## Config Settings & Feature Flags
- `ANTHROPIC_API_KEY` = <redacted> @.env.template:18
- `GEMINI_API_KEY` = <redacted> @.env.template:20
- `OPENAI_API_KEY` = <redacted> @.env.template:19
- `SUPABASE_ANON_KEY` = <redacted> @.env.template:13
- `SUPABASE_DB_PASSWORD` = <redacted> @.env.template:15
- `SUPABASE_SERVICE_ROLE_KEY` = <redacted> @.env.template:14
- `SUPABASE_URL` = <redacted> @.env.template:12
- `UPSTREAM_PUSH_TOKEN` = <redacted> @.env.template:9

## Recent Git History (evidence)
- 200 commits (newest first) · capped — repo has more · renames=17
- Merge pull request #25 from Schmoiger/feat/new-agentmd
- chore(repo): rerun init script
- feat(harness): deterministic runtime-context bullets for AGENTS.md
- feat(harness): streamline AGENTS.md source
- feat(docs): add new model tiers
- feat(docs): trim to reduce token cost
- feat(docs): update PR template
- docs(context): move AGENTS.md detail into workflows README
- docs(context): document agents-md.yaml as AGENTS.md source
- feat(context): move agents-md.yaml to workflows directory
- feat(context): generate AGENTS.md from agents-md.yaml YAML source file
- docs(spec): mark T-020 handoff complete
- feat(spec): verify --require-coverage deterministic Phase 6 gate (T-020)
- docs(spec): mark T-018 handoff complete
- docs(spec): harden confidence bands + promotion DoD template (T-018)
- docs(spec): mark T-017 handoff complete
- chore(spec): append T-017 session metrics
- feat(spec): indexer meta.history git-history evidence (T-017)
- test(bugs): bugs  after task 008
- fix(docs): move output location
- refactor(spec): move working artefacts to derived-spec-working
- docs(spec): complete Pilot A — derive-spec mode=both on this repo
- chore(spec-agent): mark T-010 completed in task tracker
- test(spec-indexer): add T-010 unit-test suite
- fix(harness): correct workspace-conventions.md with telemetry location
- feat(skill): add confirmation mode to requirements-elicitation
- feat(harness): require explanatory body in commit messages
- bugfix(harness): update source of telemetry
- bugfix(rules): udpate source of commit message telemetry
- chore(todo): add new todo for harness improvements
- feat(harness): completed task 4 extend solution-architect.md with derive mode
- feat(harness): completed task 3 extend product-owner.md with new mode
- bugfix(harness): explictly load agent-sandbox skill in AGENTS.md
- chore(metrics): log T-006 session
- feat(spec): add derived-spec draft template with confidence schema
- chore(harness): back up project-specific AGENTS.md
- feat(template): update to template to have common section at top
- docs(spec): add Cline tool-hygiene bugs B-006/B-007
- docs(spec): record process bugs + backfill session metrics (B-001..B-005)
- test(spec): rename config tests to should convention
… 160 more subjects omitted

Rename / refactor clues (cheap feature-intent signals):
- `context/artifacts/agents-md.yaml` → `context/workflows/agents-md.yaml` (feat(context): move agents-md.yaml to workflows directory)
- `artefacts/build/spec-drafts/api-catalogue.md` → `artefacts/build/derived-spec-working/api-catalogue-draft.md` (fix(docs): move output location)
- `artefacts/build/spec-drafts/architecture.md` → `artefacts/build/derived-spec-working/architecture-draft.md` (fix(docs): move output location)
- `artefacts/build/spec-drafts/data-model.md` → `artefacts/build/derived-spec-working/data-model-draft.md` (fix(docs): move output location)
- `artefacts/build/spec-drafts/product-spec.md` → `artefacts/build/derived-spec-working/product-spec-draft.md` (fix(docs): move output location)
- `artefacts/build/repo-index.json` → `artefacts/build/derived-spec-working/repo-index.json` (refactor(spec): move working artefacts to derived-spec-working)
- `artefacts/build/repo-profile.md` → `artefacts/build/derived-spec-working/repo-profile.md` (refactor(spec): move working artefacts to derived-spec-working)
- `artefacts/build/spec-scan.md` → `artefacts/build/derived-spec-working/spec-scan.md` (refactor(spec): move working artefacts to derived-spec-working)
- `context/scripts/spec_indexer.py` → `scripts/code-specs/spec_indexer.py` (refactor(spec): relocate spec indexer to scripts/code-specs)
- `artefacts/build/CLINE-STALL-PATTERNS.md` → `artefacts/build/archive/CLINE-STALL-PATTERNS.md` (docs(chore): all tasks complete, archiving task-related docs)
- `artefacts/build/tasks-cline-projection.md` → `artefacts/build/archive/tasks-cline-projection.md` (docs(chore): all tasks complete, archiving task-related docs)
- `artefacts/build/orchestrator-old.md` → `artefacts/build/archive/orchestrator-old.md` (docs(chore): move completed tasks and backed up orchestrator agent file into new build/archive folder.)
- `artefacts/build/tasks-agent-context-drift.md` → `artefacts/build/archive/tasks-agent-context-drift.md` (docs(chore): move completed tasks and backed up orchestrator agent file into new build/archive folder.)
- `context/agents/tokenomics-analyst.md` → `context/skills/tokenomics-audit.md` (refactor(agents): merge both analysts into harness-analyst)
- `context/agents/workflow-analyst.md` → `context/skills/workflow-analysis.md` (refactor(agents): merge both analysts into harness-analyst)
- `metrics/session-log.jsonl` → `artefacts/build/metrics/session-log.jsonl` (refactor(metrics): relocate session log under artefacts/build)
- `context/templates/tasks-template.md` → `context/templates/tasks-doc-template.md` (renamed to tasks-doc-template for clarity (differentiates from task-prompt-template))

## Comments & Docstrings (intent evidence)
- 866 comment blocks across 59 files; first rows:
  - `context/__init__.py:1` [docstring] Canonical context package for Agentic Orchestration Harness.
  - `context/scripts/__init__.py:1` [docstring] Scripts package for Agentic Orchestration Harness.
  - `context/scripts/code-specs/spec_indexer.py:1` [docstring] Deterministic codebase indexer for the derive-spec workflow.

Zero-LLM extraction of a structural map of a repository so that agents spawned
by the derive-spec workflow spend their token budget on synthesis and judgement
instead of file ...
  - `context/scripts/code-specs/spec_indexer.py:1` [leading] /// script | dependencies = [ | "pyyaml>=6.0", | ] | ///
  - `context/scripts/code-specs/spec_indexer.py:70` [inline] type: ignore
  - `context/scripts/code-specs/spec_indexer.py:71` [inline] pragma: no cover - declared in PEP 723 metadata
  - `context/scripts/code-specs/spec_indexer.py:74` [leading] --------------------------------------------------------------------------- | Constants | --------------------------------------------------------------------------- → const `LANG_BY_SUFFIX`
  - `context/scripts/code-specs/spec_indexer.py:88` [leading] Foreign languages handled by the universal-ctags backend (T-015) when available. → const `FOREIGN_LANG_SUFFIXES`
  - `context/scripts/code-specs/spec_indexer.py:107` [leading] (relative glob, kind) pairs for the Phase-1 existing-document discovery. → const `DOC_GLOBS`
  - `context/scripts/code-specs/spec_indexer.py:160` [leading] --- TS/JS heuristics -------------------------------------------------------- → const `_TS_IMPORT_NAMED`
  - `context/scripts/code-specs/spec_indexer.py:181` [leading] --------------------------------------------------------------------------- | Data model | ---------------------------------------------------------------------------
  - `context/scripts/code-specs/spec_indexer.py:187` [docstring] One comment/docstring block (T-021): ``{file, line, kind, text, attached}``.

``kind`` is ``docstring`` (Python docstring / TS JSDoc), ``leading``
(contiguous comment block immediately above a definition), ``inline``
(comment on a line i... → class `CommentEntry`
  - `context/scripts/code-specs/spec_indexer.py:217` [inline] class | function | method | component | interface | type | const → class `Symbol`
  - `context/scripts/code-specs/spec_indexer.py:223` [inline] T-021: last body line (0 when the backend provides none) → class `Symbol`
  - `context/scripts/code-specs/spec_indexer.py:224` [inline] T-021: doc-comment / ast docstring text (truncated) → class `Symbol`
  - `context/scripts/code-specs/spec_indexer.py:225` [inline] T-021: attached entries → class `Symbol`
  - `context/scripts/code-specs/spec_indexer.py:253` [inline] T-015: backend that produced this record (e.g. "tree-sitter") → class `FileRecord`
  - `context/scripts/code-specs/spec_indexer.py:288` [inline] T-021: source line of the column definition (0 = unknown) → class `ColumnDef`
  - `context/scripts/code-specs/spec_indexer.py:349` [docstring] One env/config/feature-flag key (T-016): ``{key, source, line, value_hint, feature}``. → class `ConfigEntry`
  - `context/scripts/code-specs/spec_indexer.py:355` [inline] <redacted> for secret-looking keys; '' when only the key matters → class `ConfigEntry`
  - `context/scripts/code-specs/spec_indexer.py:356` [inline] ENABLE_*/FEATURE_* naming or boolean-like value → class `ConfigEntry`
  - `context/scripts/code-specs/spec_indexer.py:368` [leading] --------------------------------------------------------------------------- | Repository walking | --------------------------------------------------------------------------- → function `rel`
  - `context/scripts/code-specs/spec_indexer.py:373` [docstring] Return path relative to the repo root, using forward slashes. → function `rel`
  - `context/scripts/code-specs/spec_indexer.py:385` [docstring] Return (relative paths, warnings, too_large) for files to index.

Prefers git-tracked files (respects .gitignore, skips untracked junk).
Falls back to a bounded os.walk when the repo has no git metadata. → function `find_target_files`
  - `context/scripts/code-specs/spec_indexer.py:438` [leading] --------------------------------------------------------------------------- | Python extraction (stdlib ast) | --------------------------------------------------------------------------- → function `_unparse`
  - `context/scripts/code-specs/spec_indexer.py:446` [inline] pragma: no cover - defensive against odd nodes → function `_unparse`
  - `context/scripts/code-specs/spec_indexer.py:458` [docstring] Extract (METHOD, path) from FastAPI/Flask route decorators. → function `_route_from_decorator`
  - `context/scripts/code-specs/spec_indexer.py:495` [docstring] Parse a Python module with stdlib ast; return record plus API routes. → function `analyze_python`
  - `context/scripts/code-specs/spec_indexer.py:569` [leading] --------------------------------------------------------------------------- | TypeScript / JavaScript extraction (v1 line heuristics; tree-sitter later) | --------------------------------------------------------------------------- → function `_destructured_props`
  - `context/scripts/code-specs/spec_indexer.py:574` [docstring] Extract prop names from a destructured parameter list, e.g. `({a, b}: Props)`. → function `_destructured_props`
  - `context/scripts/code-specs/spec_indexer.py:591` [docstring] Return record plus jsx-tag usage list for UI aggregation. → function `analyze_tsjs`
  - `context/scripts/code-specs/spec_indexer.py:666` [inline] props for component consts/functions (from earlier pass) → function `analyze_tsjs`
  - `context/scripts/code-specs/spec_indexer.py:674` [leading] --------------------------------------------------------------------------- | Backend selection (T-015): --extractors flag, probing, provenance | --------------------------------------------------------------------------- → const `EXTRACTOR_CHOICES`
  - `context/scripts/code-specs/spec_indexer.py:688` [leading] Which backends can cover which languages. → const `BACKEND_LANG_COVERAGE`
  - `context/scripts/code-specs/spec_indexer.py:717` [docstring] Report which external extractors are available. Every probe is wrapped; never raises.

tree-sitter is provided on demand via
``uv run --with tree-sitter --with tree-sitter-language-pack``. → function `probe_backends`
  - `context/scripts/code-specs/spec_indexer.py:730` [inline] type: ignore  # noqa: F401 → function `probe_backends`
  - `context/scripts/code-specs/spec_indexer.py:738` [docstring] Auto-mode per-language choice: (backend, reason). → function `_likely_backend`
  - `context/scripts/code-specs/spec_indexer.py:769` [docstring] Map each present language to an extractor.

Returns (plan, reasons, errors, warnings). A non-auto selection of an
unavailable backend is an error (the CLI exits non-zero), except ts-morph
which degrades quietly by design. → function `resolve_plan`
  - `context/scripts/code-specs/spec_indexer.py:859` [docstring] universal-ctags JSON backend (primary for languages without a dedicated parser). → function `analyze_ctags`
  - `context/scripts/code-specs/spec_indexer.py:887` [inline] interface-member noise; skip → function `analyze_ctags`
  - `context/scripts/code-specs/spec_indexer.py:919` [docstring] Real-AST pass for TS/TSX via tree-sitter. Richer than the regex backend:
multiline destructured props, JSX usage counts, decorators, named imports.

Requires tree-sitter, provided on demand via
``uv run --with tree-sitter --with tree-sit... → function `analyze_tsjs_treesitter`
  - `context/scripts/code-specs/spec_indexer.py:928` [inline] type: ignore → function `analyze_tsjs_treesitter`
  - `context/scripts/code-specs/spec_indexer.py:949` [inline] pragma: no cover → function `analyze_tsjs_treesitter`
  - `context/scripts/code-specs/spec_indexer.py:983` [docstring] Return (signature, destructured props) from a formal_parameters node.
  - `context/scripts/code-specs/spec_indexer.py:1037` [inline] fall through: walk the body so JSX inside functions is captured → function `analyze_tsjs_treesitter`
  - `context/scripts/code-specs/spec_indexer.py:1067` [inline] fall through to walk the method body (JSX) → function `analyze_tsjs_treesitter`
  - `context/scripts/code-specs/spec_indexer.py:1110` [inline] fall through to walk the initializers (arrow bodies contain JSX) → function `analyze_tsjs_treesitter`
  - `context/scripts/code-specs/spec_indexer.py:1118` [inline] keep walking: opening elements can nest further JSX → function `analyze_tsjs_treesitter`
  - `context/scripts/code-specs/spec_indexer.py:1125` [leading] ast-grep rule patterns for TS/JS (degraded-mode backend; tree-sitter preferred). → const `_ASTGREP_PATTERNS`
  - `context/scripts/code-specs/spec_indexer.py:1152` [docstring] Rule-driven TS/JS pass via ast-grep, used when tree-sitter is unavailable. → function `analyze_tsjs_astgrep`
  - `context/scripts/code-specs/spec_indexer.py:1224` [inline] JSX usage via the cheap line scan (ast-grep has no reliable JSX pattern set). → function `analyze_tsjs_astgrep`
  - `context/scripts/code-specs/spec_indexer.py:1231` [docstring] Optional Node/ts-morph backend; skipped quietly when node or ts-morph is absent. → function `analyze_tsjs_tsmorph`
  - `context/scripts/code-specs/spec_indexer.py:1272` [leading] --------------------------------------------------------------------------- | SQL extraction (migrations) | --------------------------------------------------------------------------- → const `_SQL_CREATE`
  - `context/scripts/code-specs/spec_indexer.py:1324` [leading] --------------------------------------------------------------------------- | Test inventory (candidate features at ~0 tokens) | --------------------------------------------------------------------------- → function `_run`
  - `context/scripts/code-specs/spec_indexer.py:1337` [docstring] Return (test node-ids, warnings). Best effort; never fails the scan. → function `collect_tests`
  - `context/scripts/code-specs/spec_indexer.py:1390` [leading] --------------------------------------------------------------------------- | Existing document discovery (Phase 1 input) | --------------------------------------------------------------------------- → function `discover_docs`
  - `context/scripts/code-specs/spec_indexer.py:1422` [leading] --------------------------------------------------------------------------- | OpenAPI extraction | --------------------------------------------------------------------------- → function `analyze_openapi`
  - `context/scripts/code-specs/spec_indexer.py:1427` [docstring] Parse openapi*.yaml/json documents into API entries + schema names. → function `analyze_openapi`
  - `context/scripts/code-specs/spec_indexer.py:1442` [inline] io / yaml / json errors — skip non-conforming docs → function `analyze_openapi`
  - `context/scripts/code-specs/spec_indexer.py:1461` [leading] --------------------------------------------------------------------------- | scan: orchestrate extraction + write index artefacts | --------------------------------------------------------------------------- → const `MAX_MAP_ROWS`
  … 806 more comment blocks

---
Generated deterministically by `context/scripts/code-specs/spec_indexer.py scan` (zero LLM tokens). Consume via `repo-index.json`.

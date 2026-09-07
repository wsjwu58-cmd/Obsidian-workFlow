"""Regression tests: run with python -m unittest discover -s scripts -p 'test_*.py'."""
import contextlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import check_consistency as gate
import collect
import curate
import gc_report
import kb_common
import lint
import research


def candidate(verdict="translate", title="Example"):
    return dict(title=title, url="https://example.com/" + title,
                verdict=verdict, reason="Technical evidence", source="author", date="2026-09-01")


class PipelineTests(unittest.TestCase):
    def test_echoed_search_json_cannot_override_final_triage(self):
        final = {"candidates": [candidate()]}
        search = {"candidates": [{"title": "Example", "url": "https://example.com/Example"}]}
        output = "```json\n" + json.dumps(final) + "\n```\nuser\ncodex\n```json\n" + json.dumps(search) + "\n```"
        self.assertEqual(research.extract_json_obj(output, True), final)
        self.assertEqual(research.extract_json_obj(json.dumps(search), True), {})

    def test_tool_json_before_valid_triage_is_ignored(self):
        final = {"candidates": [candidate("index")]}
        self.assertEqual(research.extract_json_obj('{"tool":"search"}\n' + json.dumps(final), True), final)

    def test_missing_verdict_rejected_before_disk_access(self):
        invalid = candidate()
        del invalid["verdict"]
        with self.assertRaises(ValueError):
            research.apply_triage([candidate(), invalid])

    def test_legitimate_empty_or_observe_result(self):
        for candidates in ([], [candidate("observe")]):
            data = {"candidates": candidates}
            self.assertEqual(research.extract_json_obj(json.dumps(data), True), data)

    def test_replay_promotes_observed_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d, contextlib.ExitStack() as stack:
            root = pathlib.Path(d)
            (root / "references").mkdir()
            art = root / "references/articles.md"
            art.write_text('## 已收录（编号正文）\n\n## 待处理\n<!-- pending:start -->\n<!-- pending:end -->\n## 观察项\n'
                           '| 标题 | 链接 | 来源 | 日期 | 备注 |\n| --- | --- | --- | --- | --- |\n'
                           '| Example | https://example.com/Example | old | 2026-01-01 | old |\n## 统计\n', encoding="utf-8")
            for module in (research, collect):
                stack.enter_context(patch.object(module, "ROOT", root))
            stack.enter_context(patch.object(collect, "ARTICLES", art))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            data = [candidate(), candidate("index", "Indexed")]
            self.assertEqual(research.apply_triage(data, True), (1, 1, 0))
            first = art.read_text(encoding="utf-8")
            self.assertEqual(research.apply_triage(data, True), (0, 0, 0))
            self.assertEqual(art.read_text(encoding="utf-8"), first)
            self.assertEqual(curate.parse_queue(first)[0]["date"], "2026-09-01")

    def test_queue_ignores_header_separator_and_review_rows(self):
        text = '''<!-- pending:start -->
| 标题 | 链接 | 来源 | 日期 |
| --- | --- | --- | --- |
| Example | https://example.com | author | 2026-09-01 |
| Busy | https://example.com/busy | author | 2026-09-01 | 评审中 |
<!-- pending:end -->'''
        self.assertEqual(len(curate.parse_queue(text)), 1)
        self.assertEqual(curate.parse_queue(text)[0]["title"], "Example")

    def test_final_answer_file_is_only_codex_input(self):
        with tempfile.TemporaryDirectory() as d:
            prompt = pathlib.Path(d) / "prompt.md"
            def fake_run(*args, **kwargs):
                prompt.with_suffix(".result.md").write_text("FINAL", encoding="utf-8")
                return subprocess.CompletedProcess([], 0, stdout="echo", stderr="user\ncodex\nWRONG")
            with patch.object(research.subprocess, "run", side_effect=fake_run):
                self.assertEqual(research.run_codex("prompt", str(prompt)), ("FINAL", 0))
            # A previous successful result must not be reused when output is missing.
            with patch.object(research.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
                self.assertEqual(research.run_codex("prompt", str(prompt)), ("", 1))

    def test_landing_missing_artifacts_retains_pending_and_unmatched_files(self):
        with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(io.StringIO()):
            root = pathlib.Path(d)
            (root / "references").mkdir()
            art = root / "references/articles.md"
            rows = [candidate(title="One"), candidate(title="Two")]
            art.write_text('<!-- pending:start -->\n' + ''.join(
                f"| {r['title']} | {r['url']} | author | 2026-09-01 |\n" for r in rows
            ) + '<!-- pending:end -->\n', encoding="utf-8")
            batch = root / "candidates/batch"
            wr = batch / "works-ready"
            wr.mkdir(parents=True)
            (wr / "One-translation.md").write_text("# A real translation", encoding="utf-8")
            (wr / "Unknown-translation.md").write_text("# Unmatched", encoding="utf-8")
            with patch.object(kb_common, "ROOT", root):
                moved = kb_common.land_translations(batch, rows)
            self.assertEqual(moved, ["One-translation.md"])
            text = art.read_text(encoding="utf-8")
            self.assertIn("Two", curate.parse_queue(text)[0]["title"])
            self.assertNotIn("已淘汰", text)
            self.assertTrue((wr / "Unknown-translation.md").exists())
            self.assertFalse((root / "working/Unknown-translation.md").exists())

    def test_lint_gc_include_working_and_do_not_reingest_reports(self):
        with tempfile.TemporaryDirectory() as d, contextlib.ExitStack() as stack:
            root = pathlib.Path(d)
            for directory in ("wiki", "expand", "working"):
                (root / directory).mkdir()
            (root / "working/translation.md").write_text("# Translation", encoding="utf-8")
            (root / "working/AGENTS.md").write_text("Rules", encoding="utf-8")
            (root / "expand/gc-report.md").write_text("[[old-missing]]", encoding="utf-8")
            for module in (gate, lint, gc_report):
                for name, value in (("ROOT", root), ("WIKI", root / "wiki"), ("EXPAND", root / "expand")):
                    stack.enter_context(patch.object(module, name, value))
            self.assertEqual(lint.wiki_md_files(), [root / "working/translation.md"])
            self.assertEqual(gc_report.collect_files(), lint.wiki_md_files())
            stack.enter_context(patch.object(sys, "argv", ["gc_report", "--report", str(root / "report.json"),
                "--markdown", str(root / "report.md"), "--issue", str(root / "issue.md")]))
            with contextlib.redirect_stdout(io.StringIO()):
                gc_report.main()
            self.assertEqual((root / "issue.md").stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()

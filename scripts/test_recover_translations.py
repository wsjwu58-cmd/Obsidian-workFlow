import contextlib
import io
import json
import pathlib
import subprocess
import tarfile
import tempfile
import unittest

import recover_translations as recovery


class RecoveryTests(unittest.TestCase):
    def test_recovers_staged_translation_after_reset_without_changing_checkout(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            root = pathlib.Path(directory)

            def git(*args):
                return subprocess.run(["git", *args], cwd=root, check=True,
                                      capture_output=True).stdout

            git("init")
            (root / "references").mkdir()
            (root / "references/articles.md").write_text(
                '<!-- pending:start -->\n| Example | https://example.com/article | Author | 2026-10-03 |\n'
                '<!-- pending:end -->', encoding="utf-8")
            git("add", ".")
            git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "queue")
            git("update-ref", "refs/remotes/origin/pipeline/queue", "HEAD")
            (root / "working").mkdir()
            data = ("---\ncreated: 2026-10-03\nupdated: 2026-10-03\nsources: [https://example.com/article]\n"
                    "tags: [type/翻译]\n---\n\n# 示例译文\n\n" + "中文正文，保留完整译文。" * 30).encode()
            (root / "working/Example-translation.md").write_bytes(data)
            git("add", "working")
            git("reset", "--hard", "HEAD")
            status_before = git("status", "--porcelain")
            # The output lives outside the scanned repository.
            with tempfile.TemporaryDirectory() as out:
                bundle = pathlib.Path(out) / "recovered.tar.gz"
                self.assertEqual(recovery.recover(root, bundle, 1), 0)
                with tarfile.open(bundle) as archive:
                    self.assertEqual(archive.extractfile("working/Example-translation.md").read(), data)
                    manifest = json.load(archive.extractfile("manifest.json"))
                    self.assertTrue(manifest['recovered'][0]['origin'].startswith('git-blob:'))
                self.assertEqual(git("status", "--porcelain"), status_before)

    def test_source_capture_cannot_be_used_as_translation(self):
        source = b'---\ncreated: 2026-10-03\nupdated: 2026-10-03\nsources: []\ntags: [source]\n---\nhttps://example.com/article\n'
        self.assertEqual(recovery.translation_urls(source), set())


if __name__ == "__main__":
    unittest.main()

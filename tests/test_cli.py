import json
import tempfile
import unittest
from pathlib import Path

from task_state_capsule.cli import init_capsule, verify_capsule


class CliTests(unittest.TestCase):
    def test_init_then_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"
            self.assertEqual(init_capsule(target), 0)
            self.assertEqual(verify_capsule(target), 0)
            manifest = json.loads((target / "STATE_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["project_name"], "demo")
            self.assertEqual(manifest["capsule_type"], "ai_task_state_capsule")

    def test_verify_fails_when_required_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"
            self.assertEqual(init_capsule(target), 0)
            (target / "DECISION_LOG.md").unlink()
            self.assertEqual(verify_capsule(target), 1)

    def test_verify_fails_on_invalid_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"
            self.assertEqual(init_capsule(target), 0)
            path = target / "STATE_MANIFEST.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["version_hash"] = "not-a-version"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(verify_capsule(target), 1)

    def test_init_refuses_non_empty_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            (target / "keep.txt").write_text("do not overwrite", encoding="utf-8")
            self.assertEqual(init_capsule(target), 2)
            self.assertEqual((target / "keep.txt").read_text(encoding="utf-8"), "do not overwrite")


if __name__ == "__main__":
    unittest.main()

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_capsule_zip import build
from pack_common import capsule_content_sha256_from_zip, read_capsule_manifest_from_zip


class ValidationHardeningTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> None:
        version = "v20260714-1200-test"
        files = [
            "TASK_STATUS_REPORT.md",
            "DECISION_LOG.md",
            "BRANCH_INFO.md",
            "RESUME_INSTRUCTIONS.md",
            "RECOVERY_CHECK.md",
            "STATE_MANIFEST.json",
        ]
        (root / "TASK_STATUS_REPORT.md").write_text(
            f"Version Hash: {version}\n## 4. Next Actions\n### Priority Action 1\nRun test.\n",
            encoding="utf-8",
        )
        (root / "RESUME_INSTRUCTIONS.md").write_text(
            f"Resume this task from version {version}.\n",
            encoding="utf-8",
        )
        for name in files[1:5]:
            (root / name).write_text(name, encoding="utf-8")
        manifest = {
            "schema_version": "0.1.5",
            "project_name": "fixture",
            "capsule_type": "ai_task_state_capsule",
            "version_hash": version,
            "previous_version_hash": None,
            "branch": "main",
            "created_at": "2026-07-14T12:00:00Z",
            "created_by": "human",
            "status": "active",
            "capsule_content_sha256": None,
            "files": files,
        }
        (root / "STATE_MANIFEST.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_sealed_zip_binds_state_and_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source"
            source.mkdir()
            self.make_fixture(source)
            result = build(source, Path(temp) / "dist", "ai-task-state-capsule")
            with zipfile.ZipFile(result["zip_path"]) as archive:
                manifest = read_capsule_manifest_from_zip(archive)
                self.assertEqual(manifest["version_hash"], "v20260714-1200-test")
                self.assertEqual(
                    manifest["capsule_content_sha256"],
                    capsule_content_sha256_from_zip(archive),
                )
            self.assertTrue(Path(str(result["zip_path"]) + ".sha256").exists())
            self.assertTrue(Path(result["seal"]["sealed_path"]).exists())

    def test_blank_template_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source"
            source.mkdir()
            (source / "STATE_MANIFEST.json").write_text(
                '{"version_hash": ""}\n', encoding="utf-8"
            )
            with self.assertRaises(ValueError):
                build(source, Path(temp) / "dist", "capsule")


if __name__ == "__main__":
    unittest.main()

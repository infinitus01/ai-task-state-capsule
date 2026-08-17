import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_capsule_zip import build
from pack_common import (
    capsule_content_sha256_from_zip,
    external_seal_paths,
    read_capsule_manifest_from_zip,
    write_capsule_external_seal,
)
from verify_zips import verify_zip


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

    def build_fixture(self, temp: str) -> dict:
        source = Path(temp) / "source"
        source.mkdir()
        self.make_fixture(source)
        return build(source, Path(temp) / "dist", "ai-task-state-capsule")

    def replace_zip_entry(self, archive_path: Path, entry_name: str, replacement: bytes) -> None:
        with zipfile.ZipFile(archive_path, "r") as archive:
            entries = [
                (info.filename, archive.read(info.filename))
                for info in archive.infolist()
                if not info.is_dir()
            ]
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in entries:
                archive.writestr(name, replacement if name == entry_name else content)

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

    def test_verifier_rejects_manifest_content_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = self.build_fixture(temp)
            archive_path = Path(result["zip_path"])
            with zipfile.ZipFile(archive_path) as archive:
                manifest = read_capsule_manifest_from_zip(archive)
            manifest["notes"] = "tampered after sealing"
            self.replace_zip_entry(
                archive_path,
                "STATE_MANIFEST.json",
                (json.dumps(manifest, indent=2) + "\n").encode("utf-8"),
            )
            write_capsule_external_seal(
                archive_path,
                state_version_hash=manifest["version_hash"],
                capsule_content_sha256=manifest["capsule_content_sha256"],
            )

            verification = verify_zip(archive_path)
            self.assertEqual(verification["overall"], "FAIL")
            self.assertEqual(verification["capsule_manifest"]["integrity"], "FAIL")
            self.assertIn("recomputed capsule content SHA-256", verification["capsule_manifest"]["detail"])
            self.assertEqual(verification["capsule_external_seal"]["integrity"], "PASS")

    def test_verifier_rejects_filename_version_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = self.build_fixture(temp)
            archive_path = Path(result["zip_path"])
            renamed_path = archive_path.with_name("ai-task-state-capsule-v20260714-1200-other.zip")
            archive_path.rename(renamed_path)
            write_capsule_external_seal(
                renamed_path,
                state_version_hash=result["version_hash"],
                capsule_content_sha256=result["capsule_content_sha256"],
            )

            verification = verify_zip(renamed_path)
            self.assertEqual(verification["overall"], "FAIL")
            self.assertEqual(verification["capsule_manifest"]["integrity"], "FAIL")
            self.assertIn("filename state version", verification["capsule_manifest"]["detail"])
            self.assertEqual(verification["capsule_external_seal"]["integrity"], "FAIL")

    def test_verifier_rejects_external_seal_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = self.build_fixture(temp)
            archive_path = Path(result["zip_path"])
            sha_path, sealed_path = external_seal_paths(archive_path)

            sha_path.write_text(f"{'0' * 64}  {archive_path.name}\n", encoding="utf-8")
            verification = verify_zip(archive_path)
            self.assertEqual(verification["overall"], "FAIL")
            self.assertEqual(verification["capsule_external_seal"]["integrity"], "FAIL")
            self.assertIn(".sha256 does not match", verification["capsule_external_seal"]["detail"])

            write_capsule_external_seal(
                archive_path,
                state_version_hash=result["version_hash"],
                capsule_content_sha256=result["capsule_content_sha256"],
            )
            sealed = json.loads(sealed_path.read_text(encoding="utf-8"))
            sealed["archive"] = "different-capsule.zip"
            sealed_path.write_text(json.dumps(sealed, indent=2) + "\n", encoding="utf-8")
            verification = verify_zip(archive_path)
            self.assertEqual(verification["overall"], "FAIL")
            self.assertEqual(verification["capsule_external_seal"]["integrity"], "FAIL")
            self.assertIn("archive name mismatch", verification["capsule_external_seal"]["detail"])


if __name__ == "__main__":
    unittest.main()

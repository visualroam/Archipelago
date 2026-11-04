"""The generator input hash is a property of gen_inputs.db, not its extraction context."""
import os
import shutil
import hashlib
import sqlite3
from pathlib import Path
from unittest.mock import patch
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    from ._util import find_repo_root, REPO_ONLY_REASON
except ImportError:  # run as a script
    sys.path.insert(0, HERE)
    from _util import find_repo_root, REPO_ONLY_REASON

_FOUND = find_repo_root(HERE)
REPO = _FOUND
if _FOUND is not None:
    sys.path.insert(0, os.path.join(REPO, "tools"))
    import gen_manifest


@unittest.skipUnless(_FOUND is not None, REPO_ONLY_REASON)
class GenManifestBundleIdentity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        (self.root / "greenfield").mkdir()
        (self.root / "greenfield/gen_data.py").write_text("# synthetic generator\n")
        # Test bundle identity with invented bytes, never the private game corpus.
        self.bundle = self.root / "gen_inputs.db"
        with sqlite3.connect(self.bundle) as db:
            db.execute("CREATE TABLE files(path TEXT, sha256 TEXT)")
            db.execute("INSERT INTO files VALUES (?, ?)",
                       ("event/synthetic.emevd.dcx.js",
                        hashlib.sha256(b"synthetic input").hexdigest()))
        db.close()
        env = patch.dict(os.environ, {"ER_GEN_INPUTS_DB": str(self.bundle)})
        env.start()
        self.addCleanup(env.stop)
        for name, value in (
            ("FILE_INPUTS", ["greenfield/gen_data.py"]),
            ("GLOB_INPUTS", ["elden_ring_artifacts/event/**/*"]),
        ):
            replacement = patch.object(gen_manifest, name, value)
            replacement.start()
            self.addCleanup(replacement.stop)

    def test_artifact_leftovers_do_not_change_bundle_identity(self):
        baseline = gen_manifest.compute_inputs_hash(str(self.root))
        leftover = self.root / "elden_ring_artifacts/event/stale-leftover.emevd.dcx.js"
        leftover.parent.mkdir(parents=True)
        leftover.write_text("not in synthetic bundle\n")
        self.assertEqual(baseline, gen_manifest.compute_inputs_hash(str(self.root)))

    def test_same_bundle_hashes_identically_without_an_extracted_tree(self):
        extracted = self.root / "elden_ring_artifacts/event/synthetic.emevd.dcx.js"
        extracted.parent.mkdir(parents=True)
        extracted.write_bytes(b"synthetic input")
        baseline = gen_manifest.compute_inputs_hash(str(self.root))
        other = Path(self.temp.name) / "other"
        (other / "greenfield").mkdir(parents=True)
        shutil.copyfile(self.root / "greenfield/gen_data.py", other / "greenfield/gen_data.py")
        shutil.copyfile(self.bundle, other / "gen_inputs.db")
        with patch.dict(os.environ, {"ER_GEN_INPUTS_DB": str(other / "gen_inputs.db")}):
            self.assertEqual(baseline, gen_manifest.compute_inputs_hash(str(other)))

    def test_bundle_manifest_is_read_only(self):
        before = (self.bundle.stat().st_mtime_ns, self.bundle.read_bytes())
        gen_manifest.compute_inputs_hash(str(self.root))
        after = (self.bundle.stat().st_mtime_ns, self.bundle.read_bytes())
        self.assertEqual(before, after)

    def test_external_bundle_has_same_content_identity(self):
        baseline = gen_manifest.compute_inputs_hash(str(self.root))
        private = Path(self.temp.name) / "private" / "inputs.db"
        private.parent.mkdir()
        self.bundle.replace(private)
        with patch.dict(os.environ, {"ER_GEN_INPUTS_DB": str(private)}):
            self.assertEqual(baseline, gen_manifest.compute_inputs_hash(str(self.root)))
        self.assertFalse(self.bundle.exists())

    def test_missing_configured_bundle_fails_without_creating_it(self):
        missing = Path(self.temp.name) / "private" / "missing.db"
        with patch.dict(os.environ, {"ER_GEN_INPUTS_DB": str(missing)}):
            with self.assertRaisesRegex(RuntimeError, "private generator inputs are unavailable"):
                gen_manifest.compute_inputs_hash(str(self.root))
        self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)

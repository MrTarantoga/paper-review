"""Tests for skills/paper-review/scripts/check_citations.py."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "paper-review" / "scripts" / "check_citations.py"
FIXTURE = ROOT / "tests" / "fixtures" / "basic"


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)],
        capture_output=True, text=True, check=False,
    )


def section(output, heading):
    """Return the bullet lines under a '## heading' block."""
    lines, inside = [], False
    for line in output.splitlines():
        if line.startswith("## "):
            inside = line[3:].startswith(heading)
        elif inside and line.startswith("- "):
            lines.append(line[2:])
    return lines


class CheckCitationsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run(FIXTURE / "main.tex")
        cls.out = cls.result.stdout

    def test_runs_successfully(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)

    def test_follows_input(self):
        self.assertIn("intro.tex", self.out)

    def test_missing_key_reported_with_location(self):
        missing = section(self.out, "Cited but missing")
        self.assertEqual(len(missing), 1)
        self.assertTrue(missing[0].startswith("missingkey"))
        self.assertIn("intro.tex:1", missing[0])

    def test_commented_cite_ignored(self):
        self.assertNotIn("commented", self.out)

    def test_unused_entry(self):
        self.assertEqual(section(self.out, "In bibliography but never cited"), ["unusedentry"])

    def test_duplicate_key(self):
        self.assertEqual(section(self.out, "Duplicate bib keys"), ["unusedentry"])

    def test_missing_fields(self):
        fields = section(self.out, "Entries missing common fields")
        self.assertEqual(len(fields), 1)
        self.assertIn("gamma", fields[0])
        self.assertIn("missing journal", fields[0])

    def test_date_counts_as_year(self):
        self.assertNotIn("beta", "\n".join(section(self.out, "Entries missing")))

    def test_explicit_bib_argument(self):
        result = run(FIXTURE / "main.tex", "--bib", FIXTURE / "refs.bib")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("refs.bib", result.stdout)

    def test_no_tex_files(self):
        result = run(FIXTURE / "does-not-exist.tex")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()

import os
import csv
from pathlib import Path
import unittest

class TestScaffolding(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent

    def test_directory_structure(self):
        expected_dirs = [
            "app",
            "app/agent",
            "app/audit",
            "app/database",
            "app/telephony",
            "app/voice",
            "app/workflows",
            "data",
            "tests",
            "docs",
            "scripts"
        ]
        for rel_dir in expected_dirs:
            dir_path = self.base_dir / rel_dir
            self.assertTrue(dir_path.is_dir(), f"Expected directory {rel_dir} does not exist")

    def test_env_example_exists(self):
        env_example = self.base_dir / ".env.example"
        self.assertTrue(env_example.is_file(), ".env.example must exist")
        content = env_example.read_text(encoding="utf-8")
        self.assertIn("GEMMA_API_KEY", content)
        self.assertIn("TABPFN_API_KEY", content)
        self.assertIn("TEMPORAL_HOST_URL", content)

    def test_pyproject_exists(self):
        pyproject = self.base_dir / "pyproject.toml"
        self.assertTrue(pyproject.is_file(), "pyproject.toml must exist")
        content = pyproject.read_text(encoding="utf-8")
        self.assertIn('name = "hisaabdost"', content)

    def test_sample_history_csv_readable(self):
        csv_path = self.base_dir / "data" / "sample_history.csv"
        self.assertTrue(csv_path.is_file(), "sample_history.csv must exist")
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            expected_cols = {"date", "item_id", "item", "supplier_name", "unit_price", "quantity", "unit", "total_amount"}
            self.assertTrue(expected_cols.issubset(set(reader.fieldnames or [])), "CSV missing required columns")
            self.assertGreaterEqual(len(rows), 30, "sample_history.csv should have at least 30 records")

if __name__ == "__main__":
    unittest.main()

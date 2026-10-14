"""Portuguese onboarding migration keeps existing site customizations."""

import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / "patches" / "v16_0"


class FakeDatabase:
	def __init__(self, values):
		self.values = values.copy()
		self.writes = []

	def get_value(self, doctype, name, field):
		return self.values.get((doctype, name, field))

	def set_value(self, doctype, name, field, value):
		self.values[(doctype, name, field)] = value
		self.writes.append((doctype, name, field, value))


def run_migration(db):
	frappe = types.ModuleType("frappe")
	frappe.db = db
	with patch.dict(sys.modules, {"frappe": frappe}):
		spec = importlib.util.spec_from_file_location(
			"kubera_onboarding_ptbr_test", PATCH_DIR / "kubera_onboarding_ptbr.py"
		)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		module.execute()


class TestPortugueseOnboarding(unittest.TestCase):
	def test_migrates_original_copy_and_preserves_custom_copy(self):
		values = {
			("Onboarding Step", "Create Supplier", "title"): "Add a supplier",
			("Onboarding Step", "Create Supplier", "description"): "Texto customizado",
			("Onboarding Step", "Create Supplier", "action_label"): "Add Supplier",
		}
		db = FakeDatabase(values)
		run_migration(db)
		self.assertEqual(db.values[("Onboarding Step", "Create Supplier", "title")], "Cadastre um fornecedor")
		self.assertEqual(db.values[("Onboarding Step", "Create Supplier", "description")], "Texto customizado")
		self.assertEqual(db.values[("Onboarding Step", "Create Supplier", "action_label")], "Adicionar fornecedor")
		self.assertEqual(len(db.writes), 2)

	def test_idempotent_and_matches_source_json(self):
		manifest = json.loads((PATCH_DIR / "kubera_onboarding_ptbr.json").read_text(encoding="utf-8"))
		values = {}
		for item in manifest:
			for field, pair in item["fields"].items():
				values[(item["doctype"], item["name"], field)] = pair["old"]
		db = FakeDatabase(values)
		run_migration(db)
		first_writes = len(db.writes)
		run_migration(db)
		self.assertEqual(len(db.writes), first_writes)
		self.assertEqual(first_writes, len(values))
		for item in manifest:
			source = json.loads((ROOT / item["path"]).read_text(encoding="utf-8"))
			self.assertEqual(source["name"], item["name"])
			self.assertEqual(source["doctype"], item["doctype"])
			for field, pair in item["fields"].items():
				self.assertEqual(source[field], pair["new"])


if __name__ == "__main__":
	unittest.main()

"""Keep the installed onboarding title branded without replacing custom text."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class FakeDatabase:
	def __init__(self, title):
		self.title = title
		self.writes = []

	def get_value(self, doctype, name, fieldname):
		assert (doctype, name, fieldname) == (
			"Module Onboarding", "Organization Onboarding", "title"
		)
		return self.title

	def set_value(self, doctype, name, fieldname, value):
		self.writes.append((doctype, name, fieldname, value))
		self.title = value


class TestKuberaOnboarding(unittest.TestCase):
	def run_patch(self, title):
		db = FakeDatabase(title)
		frappe = types.ModuleType("frappe")
		frappe.db = db
		path = ROOT / "patches" / "v16_0" / "kubera_onboarding_title.py"
		with patch.dict(sys.modules, {"frappe": frappe}):
			spec = importlib.util.spec_from_file_location("kubera_onboarding_title_test", path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			module.execute()
		return db

	def test_replaces_upstream_title(self):
		db = self.run_patch("Get to know ERPNext")
		self.assertEqual(db.title, "Get to know Kubera ERP")
		self.assertEqual(len(db.writes), 1)

	def test_preserves_custom_title(self):
		self.assertEqual(self.run_patch("Boas-vindas da Empresa").writes, [])

	def test_idempotent(self):
		self.assertEqual(self.run_patch("Get to know Kubera ERP").writes, [])


if __name__ == "__main__":
	unittest.main()

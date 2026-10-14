"""Dependency-free checks for Kubera's install and migration name defaults."""

import ast
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ERPNEXT_ROOT = Path(__file__).resolve().parents[1]


class FakeDatabase:
	def __init__(self, values):
		self.values = values.copy()
		self.writes = []

	def get_single_value(self, doctype, fieldname):
		return self.values.get((doctype, fieldname))

	def set_single_value(self, doctype, fieldname, value):
		self.writes.append((doctype, fieldname, value))
		self.values[(doctype, fieldname)] = value


class TestKuberaAppName(unittest.TestCase):
	def _run_patch(self, values):
		db = FakeDatabase(values)
		frappe = types.ModuleType("frappe")
		frappe.db = db
		path = ERPNEXT_ROOT / "patches" / "v16_0" / "kubera_app_name.py"
		with patch.dict(sys.modules, {"frappe": frappe}):
			spec = importlib.util.spec_from_file_location("kubera_app_name_under_test", path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			module.execute()
		return db

	def test_patch_replaces_only_upstream_defaults(self):
		initial = {
			("System Settings", "app_name"): "ERPNext",
			("Website Settings", "app_name"): "Frappe",
			("Website Settings", "app_logo"): None,
		}
		db = self._run_patch(initial)
		self.assertEqual(
			db.writes,
			[
				("System Settings", "app_name", "Kubera ERP"),
				("Website Settings", "app_name", "Kubera ERP"),
				("Website Settings", "app_logo", "/assets/erpnext/images/kubera-wordmark.svg"),
			],
		)

	def test_patch_preserves_custom_names(self):
		initial = {
			("System Settings", "app_name"): "Minha Empresa",
			("Website Settings", "app_name"): "Portal Próprio",
			("Website Settings", "app_logo"): "/files/custom-logo.svg",
		}
		self.assertEqual(self._run_patch(initial).writes, [])

	def test_patch_handles_empty_defaults(self):
		initial = {
			("System Settings", "app_name"): None,
			("Website Settings", "app_name"): "",
		}
		self.assertEqual(len(self._run_patch(initial).writes), 3)

	def test_install_sets_both_app_names(self):
		source = (ERPNEXT_ROOT / "setup" / "install.py").read_text(encoding="utf-8")
		functions = [
			node
			for node in ast.parse(source).body
			if isinstance(node, ast.FunctionDef) and node.name == "add_app_name"
		]
		self.assertEqual(len(functions), 1)
		db = FakeDatabase({})
		function_only = ast.Module(body=functions, type_ignores=[])
		namespace = {"frappe": types.SimpleNamespace(db=db)}
		exec(compile(function_only, str(ERPNEXT_ROOT / "setup" / "install.py"), "exec"), namespace)
		namespace["add_app_name"]()
		self.assertEqual(
			db.writes,
			[
				("System Settings", "app_name", "Kubera ERP"),
				("Website Settings", "app_name", "Kubera ERP"),
				("Website Settings", "app_logo", "/assets/erpnext/images/kubera-wordmark.svg"),
			],
		)


if __name__ == "__main__":
	unittest.main()

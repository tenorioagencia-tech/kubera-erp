"""Checks for Kubera's Brazilian Portuguese default without overriding choices."""

import ast
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ERPNEXT_ROOT = Path(__file__).resolve().parents[1]


class FakeSystemSettings:
	def __init__(self, language):
		self.language = language
		self.saves = 0

	def save(self):
		self.saves += 1


class TestKuberaLanguage(unittest.TestCase):
	def _run_install_function(self, language, runs=1):
		source = (ERPNEXT_ROOT / "setup" / "install.py").read_text(encoding="utf-8")
		functions = [
			node
			for node in ast.parse(source).body
			if isinstance(node, ast.FunctionDef) and node.name == "set_default_site_language"
		]
		self.assertEqual(len(functions), 1)
		doc = FakeSystemSettings(language)
		frappe = types.SimpleNamespace(
			db=types.SimpleNamespace(get_single_value=lambda doctype, field: doc.language),
			get_doc=lambda doctype: doc,
		)
		namespace = {"frappe": frappe}
		exec(compile(ast.Module(body=functions, type_ignores=[]), "install.py", "exec"), namespace)
		for _ in range(runs):
			namespace["set_default_site_language"]()
		return doc

	def test_english_default_becomes_brazilian_portuguese(self):
		doc = self._run_install_function("en")
		self.assertEqual((doc.language, doc.saves), ("pt-BR", 1))

	def test_custom_language_is_preserved(self):
		doc = self._run_install_function("es")
		self.assertEqual((doc.language, doc.saves), ("es", 0))

	def test_empty_default_is_set_once(self):
		doc = self._run_install_function(None, runs=2)
		self.assertEqual((doc.language, doc.saves), ("pt-BR", 1))

	def test_install_calls_language_default(self):
		source = (ERPNEXT_ROOT / "setup" / "install.py").read_text(encoding="utf-8")
		after_install = next(
			node for node in ast.parse(source).body
			if isinstance(node, ast.FunctionDef) and node.name == "after_install"
		)
		self.assertTrue(
			any(
				isinstance(node, ast.Call)
				and isinstance(node.func, ast.Name)
				and node.func.id == "set_default_site_language"
				for node in ast.walk(after_install)
			)
		)

	def test_patch_uses_same_safe_default(self):
		path = ERPNEXT_ROOT / "patches" / "v16_0" / "kubera_portuguese_default.py"
		frappe = types.ModuleType("frappe")
		install = types.ModuleType("erpnext.setup.install")
		calls = []
		install.set_default_site_language = lambda: calls.append(True)
		with patch.dict(sys.modules, {"frappe": frappe, "erpnext.setup.install": install}):
			spec = importlib.util.spec_from_file_location("kubera_portuguese_default_under_test", path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			module.execute()
		self.assertEqual(calls, [True])


if __name__ == "__main__":
	unittest.main()

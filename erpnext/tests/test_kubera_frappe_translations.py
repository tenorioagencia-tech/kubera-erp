"""Regression checks for Brazilian Portuguese strings supplied by Kubera ERP."""

import csv
import re
import unittest
from pathlib import Path


TRANSLATIONS = Path(__file__).resolve().parents[1] / "translations" / "pt-BR.csv"
PLACEHOLDER = re.compile(r"(?<!\{)\{\d+\}(?!\})")


class TestKuberaFrappeTranslations(unittest.TestCase):
	def test_core_interface_has_portuguese_labels(self):
		with TRANSLATIONS.open(encoding="utf-8-sig", newline="") as stream:
			rows = list(csv.reader(stream))
		translations = {source: target for source, target, *context in rows if not context or not context[0]}
		for source in (
			"Sign In",
			"Forgot password?",
			"All apps",
			"Sidebar Menu",
			"Collapse sidebar",
			"Expand sidebar",
			"Good morning",
			"Good afternoon",
			"Good evening",
			"{0} of {1} steps done",
		):
			with self.subTest(source=source):
				self.assertIn(source, translations)
				self.assertTrue(translations[source].strip())

	def test_csv_has_unique_keys_and_preserves_placeholders(self):
		with TRANSLATIONS.open(encoding="utf-8-sig", newline="") as stream:
			rows = list(csv.reader(stream))
		keys = set()
		for row in rows:
			self.assertIn(len(row), (2, 3), row)
			source, target = row[:2]
			key = (source, row[2] if len(row) == 3 else "")
			self.assertNotIn(key, keys)
			keys.add(key)
			self.assertEqual(sorted(PLACEHOLDER.findall(source)), sorted(PLACEHOLDER.findall(target)), source)

	def test_common_frappe_workflows_have_portuguese_text(self):
		with TRANSLATIONS.open(encoding="utf-8-sig", newline="") as stream:
			rows = list(csv.reader(stream))
		translations = {(source, context[0] if context else ""): target for source, target, *context in rows}
		for source, context in (
			("Back to sign in", ""),
			("Invalid credentials, try again.", ""),
			("Please check your email.", ""),
			("Use strong passwords.", ""),
			("Clear all filters", ""),
			("Deleted all documents successfully", ""),
			("Save the document to attach files.", ""),
			("Please fill the following mandatory fields before saving:", ""),
			("Permission Manager", ""),
			("You do not have permission to restore this document.", ""),
			("You need write permissions to add attachments to this record.", ""),
			("Create a new document", "Description of a list view shortcut"),
			("Enter Value", "Title of prompt dialog"),
		):
			with self.subTest(source=source, context=context):
				self.assertIn((source, context), translations)
				self.assertTrue(translations[source, context].strip())
				self.assertNotEqual(source, translations[source, context])


if __name__ == "__main__":
	unittest.main()

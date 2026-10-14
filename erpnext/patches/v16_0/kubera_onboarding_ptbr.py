"""Localize standard onboarding copy already stored on installed sites.

Only exact upstream values are replaced. Site-specific edits and stable record
names, routes, actions, roles, and completion state remain untouched.
"""

import json
from pathlib import Path

import frappe


def execute():
	manifest = Path(__file__).with_suffix(".json")
	for item in json.loads(manifest.read_text(encoding="utf-8")):
		for field, translation in item["fields"].items():
			current = frappe.db.get_value(item["doctype"], item["name"], field)
			if current == translation["old"]:
				frappe.db.set_value(item["doctype"], item["name"], field, translation["new"])

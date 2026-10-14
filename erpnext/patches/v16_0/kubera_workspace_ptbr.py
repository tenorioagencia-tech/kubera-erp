"""Translate standard Desk presentation text on already installed Kubera sites.

Only exact upstream English labels are changed. Record names, link targets,
routes, roles, filters and chart identifiers remain untouched.
"""

import json
from pathlib import Path

import frappe


ERPNEXT = Path(__file__).resolve().parents[2]
LABELS = json.loads(Path(__file__).with_name("kubera_workspace_labels.json").read_text(encoding="utf-8"))
DOCTYPES = {"Workspace", "Workspace Sidebar", "Sidebar", "Number Card", "Dashboard Chart"}
CHILD_TABLES = ("links", "shortcuts", "charts", "number_cards", "items", "sidebar_items")


def localize_doc(doc, db):
	for field in ("label", "title", "empty_state_message"):
		value = getattr(doc, field, None)
		if value in LABELS and LABELS[value] != value:
			db.set_value(doc.doctype, doc.name, field, LABELS[value], update_modified=False)

	for table in CHILD_TABLES:
		for row in getattr(doc, table, None) or []:
			value = getattr(row, "label", None)
			if value in LABELS and LABELS[value] != value:
				db.set_value(row.doctype, row.name, "label", LABELS[value], update_modified=False)

	content = getattr(doc, "content", None)
	if isinstance(content, str):
		blocks = json.loads(content or "[]")
		changed = False
		for block in blocks:
			if block.get("type") != "card":
				continue
			data = block.get("data") or {}
			value = data.get("card_name")
			if value in LABELS and LABELS[value] != value:
				data["card_name"] = LABELS[value]
				changed = True
		if changed:
			db.set_value(
				doc.doctype, doc.name, "content", json.dumps(blocks, ensure_ascii=False),
				update_modified=False,
			)


def execute():
	for path in ERPNEXT.rglob("*.json"):
		if not any(part in path.parts for part in (
			"workspace", "workspace_sidebar", "sidebar", "number_card", "dashboard_chart"
		)):
			continue
		try:
			source = json.loads(path.read_text(encoding="utf-8"))
		except (ValueError, UnicodeDecodeError):
			continue
		doctype = source.get("doctype")
		name = source.get("name")
		if doctype in DOCTYPES and name and frappe.db.exists(doctype, name):
			localize_doc(frappe.get_doc(doctype, name), frappe.db)

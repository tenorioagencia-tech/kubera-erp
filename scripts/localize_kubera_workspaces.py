"""Apply Kubera's pt-BR presentation labels to standard Desk JSON.

The map intentionally never changes record names, links, routes or permission rows.
Run this script when adding standard Workspace, Sidebar, Number Card or Dashboard
Chart fixtures to the fork.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERPNEXT = ROOT / "erpnext"
LABELS_FILE = ERPNEXT / "patches" / "v16_0" / "kubera_workspace_labels.json"


def localize_document(document, labels):
	for key in ("label", "title", "empty_state_message"):
		if document.get(key) in labels:
			document[key] = labels[document[key]]

	for collection in ("links", "shortcuts", "charts", "number_cards", "items", "sidebar_items"):
		for row in document.get(collection) or []:
			if isinstance(row, dict) and row.get("label") in labels:
				row["label"] = labels[row["label"]]

	if isinstance(document.get("content"), str):
		content = json.loads(document["content"] or "[]")
		for row in content:
			if row.get("type") == "card" and row.get("data", {}).get("card_name") in labels:
				row["data"]["card_name"] = labels[row["data"]["card_name"]]
		document["content"] = json.dumps(content, ensure_ascii=False)

	return document


def main():
	labels = json.loads(LABELS_FILE.read_text(encoding="utf-8"))
	for path in ERPNEXT.rglob("*.json"):
		if not any(part in path.parts for part in (
			"workspace", "workspace_sidebar", "sidebar", "number_card", "dashboard_chart"
		)):
			continue
		raw = path.read_bytes()
		try:
			document = json.loads(raw)
		except (ValueError, UnicodeDecodeError):
			continue
		if document.get("doctype") not in {
			"Workspace", "Workspace Sidebar", "Sidebar", "Number Card", "Dashboard Chart"
		}:
			continue
		before = json.dumps(document, ensure_ascii=False, sort_keys=True)
		localize_document(document, labels)
		if json.dumps(document, ensure_ascii=False, sort_keys=True) == before:
			continue
		newline = b"\r\n" if b"\r\n" in raw else b"\n"
		text = json.dumps(document, ensure_ascii=False, indent=1) + "\n"
		path.write_bytes(text.replace("\n", newline.decode()).encode("utf-8"))
		print(path.relative_to(ROOT))


if __name__ == "__main__":
	main()

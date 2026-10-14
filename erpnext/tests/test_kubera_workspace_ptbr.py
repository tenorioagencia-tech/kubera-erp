"""Verify Portuguese Desk labels without changing workspace identifiers."""

import json
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def source(*parts):
	return json.loads(ROOT.joinpath(*parts).read_text(encoding="utf-8"))


class TestKuberaWorkspacePortuguese(unittest.TestCase):
	def test_every_workspace_card_references_its_link_section(self):
		for path in ROOT.rglob("*.json"):
			if "workspace" not in path.parts:
				continue
			workspace = json.loads(path.read_text(encoding="utf-8"))
			if workspace.get("doctype") != "Workspace":
				continue
			with self.subTest(workspace=workspace["name"]):
				cards = {
					row["data"]["card_name"] for row in json.loads(workspace["content"])
					if row["type"] == "card"
				}
				sections = {
					row["label"] for row in workspace["links"] if row["type"] == "Card Break"
				}
				self.assertEqual(cards, sections)

	def test_accounting_cards_keep_internal_references(self):
		workspace = source("accounts", "workspace", "accounting", "accounting.json")
		self.assertEqual(workspace["name"], "Accounting")
		self.assertEqual(workspace["label"], "Contabilidade")
		cards = [row["data"]["card_name"] for row in json.loads(workspace["content"]) if row["type"] == "card"]
		self.assertIn("Impostos e conformidade", cards)
		self.assertIn("Faturamento e pagamentos", cards)
		self.assertIn("Conciliação", cards)
		self.assertIn("Abertura e encerramento", cards)
		self.assertIn("Ferramentas do razão", cards)
		self.assertEqual(
			{row["label"] for row in workspace["links"] if row["type"] == "Card Break"},
			set(cards),
		)
		self.assertTrue(any(row.get("link_to") == "Balance Sheet" for row in workspace["links"]))
		self.assertTrue(any(
			row.get("link_to") == "Accounts Receivable Summary"
			and row.get("label") == "Resumo de contas a receber"
			for row in workspace["links"]
		))

	def test_home_cards_and_chart_copy(self):
		home = source("setup", "workspace", "home", "home.json")
		self.assertEqual(home["name"], "Home")
		self.assertEqual(home["label"], "Início")
		self.assertIn("Vendas anuais", [row["label"] for row in home["number_cards"]])
		self.assertIn("Valor total do estoque", [row["label"] for row in home["number_cards"]])
		chart = source("accounts", "dashboard_chart", "profit_and_loss", "profit_and_loss.json")
		self.assertEqual(chart["name"], "Profit and Loss")
		self.assertEqual(
			chart["empty_state_message"],
			"Suas receitas e despesas ao longo do ano e o lucro resultante.",
		)

	def test_sidebar_preserves_links(self):
		sidebar = source("accounts", "sidebar", "accounts", "accounts.json")
		self.assertEqual(sidebar["name"], "Accounts")
		self.assertEqual(sidebar["title"], "Contabilidade")
		self.assertIn("Orçamento", [row["label"] for row in sidebar["items"]])
		self.assertTrue(any(row.get("link_to") == "Budget" for row in sidebar["items"]))

	def test_patch_updates_only_original_labels_and_is_idempotent(self):
		class Row:
			def __init__(self, name, label):
				self.doctype = "Workspace Link"
				self.name = name
				self.label = label

		class Database:
			def __init__(self):
				self.writes = []

			def set_value(self, doctype, name, field, value, **kwargs):
				self.writes.append((doctype, name, field, value))

		db = Database()
		frappe = types.ModuleType("frappe")
		frappe.db = db
		module_path = ROOT / "patches" / "v16_0" / "kubera_workspace_ptbr.py"
		with patch.dict(sys.modules, {"frappe": frappe}):
			spec = importlib.util.spec_from_file_location("kubera_workspace_ptbr_test", module_path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			doc = types.SimpleNamespace(
				doctype="Workspace", name="Accounting", label="Accounting",
				content=json.dumps([
					{"id": "card-1", "type": "card", "data": {"card_name": "Tax & Compliance"}},
				]),
				links=[Row("upstream", "Budgeting"), Row("custom", "Minha seção personalizada")],
				shortcuts=[], charts=[], number_cards=[], items=[], sidebar_items=[],
			)
			module.localize_doc(doc, db)
			self.assertIn(("Workspace", "Accounting", "label", "Contabilidade"), db.writes)
			self.assertIn(("Workspace Link", "upstream", "label", "Orçamento"), db.writes)
			self.assertFalse(any(write[1] == "custom" for write in db.writes))
			content_write = next(write[3] for write in db.writes if write[2] == "content")
			self.assertEqual(json.loads(content_write)[0]["data"]["card_name"], "Impostos e conformidade")
			doc.label = "Contabilidade"
			doc.content = content_write
			doc.links[0].label = "Orçamento"
			db.writes.clear()
			module.localize_doc(doc, db)
			self.assertEqual(db.writes, [])


if __name__ == "__main__":
	unittest.main()

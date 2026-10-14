"""Guard the Kubera presentation labels against upstream navigation changes."""

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = "7474d9e786277383de1242ab882f16856d17a9c9"
DOCK = "erpnext/dock/erpnext/erpnext.json"
APP_ICON = "erpnext/desktop_icon/erpnext.json"
SETTINGS_ICON = "erpnext/desktop_icon/erpnext_settings.json"


def current_json(path):
	return json.loads((ROOT / path).read_text(encoding="utf-8"))


def base_json(path):
	contents = subprocess.check_output(
		["git", "-C", str(ROOT), "show", f"{BASE}:{path}"], text=True, encoding="utf-8"
	)
	return json.loads(contents)


class TestKuberaNavigation(unittest.TestCase):
	def test_dock_only_changes_display_titles(self):
		current = current_json(DOCK)
		base = base_json(DOCK)
		expected_titles = [
			"Configurações",
			"Contabilidade",
			"Vendas",
			"Compras",
			"Estoque",
			"Produção",
			"Projetos",
			"Patrimônio",
			"Qualidade",
			"CRM",
			"Suporte",
			"Portal",
		]
		self.assertEqual([item["title"] for item in current["items"]], expected_titles)
		self.assertEqual(len(current["items"]), len(base["items"]))
		for updated, original in zip(current["items"], base["items"], strict=True):
			self.assertEqual(
				{k: v for k, v in updated.items() if k != "title"},
				{k: v for k, v in original.items() if k != "title"},
			)
		self.assertEqual(
			{k: v for k, v in current.items() if k != "items"},
			{k: v for k, v in base.items() if k != "items"},
		)

	def test_desktop_icons_only_change_presentation(self):
		for path, expected_label, expected_logo in (
			(APP_ICON, "Kubera ERP", "/assets/erpnext/images/kubera-icon.svg"),
			(SETTINGS_ICON, "Configurações Kubera ERP", ""),
		):
			with self.subTest(path=path):
				current = current_json(path)
				base = base_json(path)
				self.assertEqual(current["label"], expected_label)
				self.assertEqual(current["logo_url"], expected_logo)
				self.assertEqual(
					{k: v for k, v in current.items() if k not in {"label", "logo_url"}},
					{k: v for k, v in base.items() if k not in {"label", "logo_url"}},
				)
				if path == SETTINGS_ICON:
					self.assertEqual(current["logo_url"], base["logo_url"])


if __name__ == "__main__":
	unittest.main()

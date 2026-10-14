"""Guard the Kubera presentation labels against upstream navigation changes."""

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
# SHA-256 values of upstream 7474d9e after removing presentation-only fields.
# These constants let the guard run from a shallow clone or a built Docker image.
UPSTREAM_PROTECTED_HASHES = {
	"erpnext/dock/erpnext/erpnext.json": "049cdabf3aa4f07bb4d5e5ae7b6b6e91c3bcb77b37db8274c3a2655713c61340",
	"erpnext/desktop_icon/erpnext.json": "1e7a617f2ffe5cc0b326aa073927cda489608b7f815fa6837acd23442e7de992",
	"erpnext/desktop_icon/erpnext_settings.json": "914b716e76e74b35c0b2bdb67f07a0f906b87cd7ec332f8af311d45d45082398",
}
DOCK = "erpnext/dock/erpnext/erpnext.json"
APP_ICON = "erpnext/desktop_icon/erpnext.json"
SETTINGS_ICON = "erpnext/desktop_icon/erpnext_settings.json"


def current_json(path):
	return json.loads((ROOT / path).read_text(encoding="utf-8"))


def protected_digest(data):
	serialized = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
	return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class TestKuberaNavigation(unittest.TestCase):
	def test_dock_only_changes_display_titles(self):
		current = current_json(DOCK)
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
		for item in current["items"]:
			item.pop("title")
		self.assertEqual(protected_digest(current), UPSTREAM_PROTECTED_HASHES[DOCK])

	def test_desktop_icons_only_change_presentation(self):
		for path, expected_label, expected_logo in (
			(APP_ICON, "Kubera ERP", "/assets/erpnext/images/kubera-icon.svg"),
			(SETTINGS_ICON, "Configurações Kubera ERP", ""),
		):
			with self.subTest(path=path):
				current = current_json(path)
				self.assertEqual(current["label"], expected_label)
				self.assertEqual(current["logo_url"], expected_logo)
				current.pop("label")
				current.pop("logo_url")
				self.assertEqual(protected_digest(current), UPSTREAM_PROTECTED_HASHES[path])


if __name__ == "__main__":
	unittest.main()

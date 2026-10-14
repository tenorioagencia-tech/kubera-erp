"""Verify the public identity without requiring a running Frappe site."""

import runpy
import unittest
from pathlib import Path


ERPNEXT_ROOT = Path(__file__).resolve().parents[1]
ASSET_PREFIX = "/assets/erpnext/images/"


class TestKuberaBranding(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.hooks = runpy.run_path(str(ERPNEXT_ROOT / "hooks.py"))

	def assert_brand_asset(self, url, suffix):
		self.assertTrue(url.startswith(ASSET_PREFIX), url)
		self.assertTrue(url.endswith(suffix), url)
		asset = ERPNEXT_ROOT / "public" / "images" / url.removeprefix(ASSET_PREFIX)
		self.assertTrue(asset.is_file(), f"Missing brand asset: {asset}")
		self.assertGreater(asset.stat().st_size, 100, f"Empty brand asset: {asset}")

	def test_app_identity_and_upstream_attribution(self):
		hooks = self.hooks
		self.assertEqual(hooks["app_title"], "Kubera ERP")
		self.assertEqual(hooks["app_name"], "erpnext")
		self.assertEqual(hooks["app_publisher"], "Frappe Technologies Pvt. Ltd.")
		self.assertEqual(hooks["app_license"], "GNU General Public License (v3)")
		self.assertEqual(hooks["source_link"], "https://github.com/frappe/erpnext")

	def test_logo_and_apps_screen(self):
		hooks = self.hooks
		self.assert_brand_asset(hooks["app_logo_url"], ".svg")
		self.assertNotIn("erpnext-logo", hooks["app_logo_url"])
		self.assertEqual(len(hooks["add_to_apps_screen"]), 1)
		app = hooks["add_to_apps_screen"][0]
		self.assertEqual(app["name"], "erpnext")
		self.assertEqual(app["title"], "Kubera ERP")
		self.assertEqual(app["route"], "/desk/home")
		self.assertEqual(app["has_permission"], "erpnext.check_app_permission")
		self.assert_brand_asset(app["logo"], ".svg")
		self.assertNotIn("erpnext-logo", app["logo"])

	def test_website_and_email_assets(self):
		hooks = self.hooks
		self.assertTrue((ERPNEXT_ROOT / "public" / "images" / "kubera-wordmark.svg").is_file())
		self.assert_brand_asset(hooks["website_context"]["favicon"], ".svg")
		self.assert_brand_asset(hooks["website_context"]["splash_image"], ".svg")
		self.assert_brand_asset("/" + hooks["email_brand_image"].lstrip("/"), ".png")
		for url in [*hooks["website_context"].values(), hooks["email_brand_image"]]:
			self.assertNotIn("erpnext-logo", url)
			self.assertNotIn("erpnext-favicon", url)


if __name__ == "__main__":
	unittest.main()

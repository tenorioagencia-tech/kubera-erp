"""Keep new user profiles aligned with the site's selected language."""

import frappe


def set_user_language_if_blank(doc, method=None):
	if not doc.language:
		doc.language = frappe.db.get_single_value("System Settings", "language") or "pt-BR"


def fill_empty_user_languages():
	"""Set only empty user languages; explicit user choices remain intact."""
	default = frappe.db.get_single_value("System Settings", "language") or "pt-BR"
	for user in frappe.get_all("User", fields=["name", "language"], limit_page_length=0):
		if not user.language:
			frappe.db.set_value("User", user.name, "language", default, update_modified=False)

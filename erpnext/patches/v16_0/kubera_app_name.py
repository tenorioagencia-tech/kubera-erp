"""Set Kubera's visible name without overwriting a site's custom branding."""

import frappe


def execute():
	for doctype in ("System Settings", "Website Settings"):
		current_name = frappe.db.get_single_value(doctype, "app_name")
		if current_name in (None, "", "ERPNext", "Frappe"):
			frappe.db.set_single_value(doctype, "app_name", "Kubera ERP")

	current_logo = frappe.db.get_single_value("Website Settings", "app_logo")
	if current_logo in (
		None,
		"",
		"/assets/erpnext/images/erpnext-logo.svg",
		"/assets/frappe/images/frappe-logo.svg",
	):
		frappe.db.set_single_value(
			"Website Settings", "app_logo", "/assets/erpnext/images/kubera-wordmark.svg"
		)

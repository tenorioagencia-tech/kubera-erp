"""Rebrand the standard organization onboarding title on existing sites."""

import frappe


def execute():
	current_title = frappe.db.get_value(
		"Module Onboarding", "Organization Onboarding", "title"
	)
	if current_title == "Get to know ERPNext":
		frappe.db.set_value(
			"Module Onboarding", "Organization Onboarding", "title", "Get to know Kubera ERP"
		)

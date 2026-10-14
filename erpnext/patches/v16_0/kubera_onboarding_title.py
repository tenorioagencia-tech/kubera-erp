"""Rebrand the standard organization onboarding title on existing sites."""

import frappe


def execute():
	current_title = frappe.db.get_value(
		"Module Onboarding", "Organization Onboarding", "title"
	)
	if current_title in {"Get to know ERPNext", "Get to know Kubera ERP"}:
		frappe.db.set_value(
			"Module Onboarding", "Organization Onboarding", "title", "Conheça o Kubera ERP"
		)

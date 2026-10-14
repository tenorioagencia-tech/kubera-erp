"""Set the site language to Brazilian Portuguese without changing user choices."""

from erpnext.setup.install import set_default_site_language


def execute():
	set_default_site_language()

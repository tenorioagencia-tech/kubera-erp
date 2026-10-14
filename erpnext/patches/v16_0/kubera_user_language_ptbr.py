"""Fill empty language preferences on previously installed users."""

from erpnext.setup.user_language import fill_empty_user_languages


def execute():
	fill_empty_user_languages()

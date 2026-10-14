"""Apply the expanded Portuguese display-label map on installed sites."""

from erpnext.patches.v16_0.kubera_workspace_ptbr import execute as localize_workspaces


def execute():
	localize_workspaces()

import frappe
from frappe import _

class Project(frappe.model.document.Document):
    def validate(self):
        if not self.project_name:
            frappe.throw(_("Project Name is required"))
        if not self.start_date:
            frappe.throw(_("Start Date is required"))
        if not self.status:
            frappe.throw(_("Status is required"))

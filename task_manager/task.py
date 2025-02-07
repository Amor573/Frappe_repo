import frappe
from frappe import _

class Task(frappe.model.document.Document):
    def validate(self):
        if not self.task_name:
            frappe.throw(_("Task Name is required"))
        if not self.project:
            frappe.throw(_("Project is required"))
        if not self.assigned_to:
            frappe.throw(_("Assigned To is required"))
        if not self.status:
            frappe.throw(_("Status is required"))
        if not self.priority:
            frappe.throw(_("Priority is required"))
        if not self.due_date:
            frappe.throw(_("Due Date is required"))

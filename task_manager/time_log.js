frappe.ui.form.on("Time Log", {
    validate: function (frm) {
        if (frm.doc.hours <= 0) {
            frappe.throw("Logged hours must be greater than zero.");
        }
    }
});

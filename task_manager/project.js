frappe.ui.form.on("Project", {
    validate: function (frm) {
        if (frm.doc.end_date < frm.doc.start_date) {
            frappe.throw("End date must be later than the start date.");
        }
    }
});

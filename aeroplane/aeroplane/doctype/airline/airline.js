// Copyright (c) 2024, nil and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
  refresh(frm) {
    frm.add_web_link(frm.doc.route, "Visit Website");
  },
});

// Copyright (c) 2024, nil and contributors
// For license information, please see license.txt

// Custom Script for Payment Schedular
frappe.ui.form.on("Payment Schedular", {
  refresh: function (frm) {
    frm.add_custom_button(__("Make Payment"), function () {
      // Call the record_payment function
      frappe.call({
        method:
          "aeroplane.airport_shop_management.doctype.payment_schedular.payment_schedular.record_payment",
        args: {
          payment_schedule_name: frm.doc.name, // Use the current document name
        },
        callback: function (response) {
          if (response.exc) {
            frappe.msgprint(
              "Error recording payment. Check the console for details."
            );
            console.log(response.exc);
          } else {
            frappe.msgprint("Payment recorded and receipt sent.");
          }
        },
      });
    });
  },
});

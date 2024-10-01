// Copyright (c) 2024, nil and contributors
// For license information, please see license.txt
frappe.ui.form.on("Airplane Ticket", {
  refresh(frm) {
    frm.add_custom_button(
      "Assign Seats",
      () => {
        d.show();
        console.log("Called");
      },
      "Actions"
    );
  },
});

let d = new frappe.ui.Dialog({
  title: "Select Seat",
  fields: [
    {
      label: "Seat Number",
      fieldname: "seat_number",
      fieldtype: "Data",
    },
  ],
  size: "small",
  primary_action_label: "Submit",
  primary_action(values) {
    if (values.seat_number) {
      cur_frm.set_value("seat", values.seat_number);
    }
    d.hide();
  },
});

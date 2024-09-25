// Copyright (c) 2024, nil and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
  onload: function (frm) {
    // Set the initial color based on the default status
    set_status_color(frm);
  },
  status: function (frm) {
    // Change color when status is changed
    set_status_color(frm);
  },
});

function set_status_color(frm) {
  const status = frm.doc.status;
  let color;

  if (status === "Booked") {
    color = "gray";
  } else if (status === "Checked-In") {
    color = "purple";
  } else if (status === "Boarded") {
    color = "green";
  }

  // Apply the color to the form header or another element
  if (color) {
    frm.$wrapper.find(".form-header").css("background-color", color);
  }
}

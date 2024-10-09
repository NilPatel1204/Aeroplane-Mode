// assets/aeroplane/js/report.js

frappe.query_reports["Shop Script Report"] = {
  filters: [
    {
      fieldname: "airport_name",
      label: __("Airport Name"), // Ensure you are using __() for translations
      fieldtype: "Link",
      options: "Airport", // Ensure this matches your actual doctype
    },
    // {
    //   fieldname: "shop_status",
    //   label: __("Shop Status"),
    //   fieldtype: "Select",
    //   options: ["Open", "Closed"], // Use array for options
    //   reqd: 0,
    // },
  ],
};

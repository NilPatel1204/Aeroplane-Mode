# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.document import Document

class AirplaneFlight(WebsiteGenerator,Document):
    def validate(self):
        frappe.msgprint(self.name)

    def on_submit(self):
        self.submit_boarded_tickets()

    def submit_boarded_tickets(self):
        boarded_tickets = frappe.get_all(
            "Airplane Ticket",
            filters={
                "flight": self.name,
                "status": "Boarded"
            },
            fields=["name"]
        )

        for ticket in boarded_tickets:
            ticket_doc = frappe.get_doc("Airplane Ticket", ticket.name)
            if ticket_doc.docstatus == 0:
                ticket_doc.submit()
                frappe.msgprint(f"Ticket {ticket_doc.name} has been submitted successfully.")
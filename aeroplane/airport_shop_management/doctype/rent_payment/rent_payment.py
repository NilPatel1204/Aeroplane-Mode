# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
	def before_insert(self):
        # Get the current year
		current_year = frappe.utils.nowdate().split("-")[0]

        # Get the last receipt number generated for the current year
		last_receipt = frappe.db.sql("""SELECT receipt_number FROM `tabRent Payment`
                                        WHERE receipt_number LIKE %s
                                        ORDER BY creation DESC LIMIT 1""", (f"RENT-{current_year}-%",))

        # Extract the numeric part of the last receipt number
		if last_receipt:
			last_num = int(last_receipt[0][0].split("-")[-1])
		else:
			last_num = 0
        
        # Generate new receipt number
		new_num = last_num + 1
		self.receipt_number = f"RENT-{current_year}-{str(new_num).zfill(4)}"

        # Check for uniqueness
		if frappe.db.exists("Rent Payment", {"receipt_number": self.receipt_number}):
			frappe.throw(f"Receipt Number {self.receipt_number} already exists, try again!")

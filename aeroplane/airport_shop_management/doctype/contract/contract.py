# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate, add_months

class Contract(Document):
	def before_save(self):
# Check if the selected shop is already occupied
		send_rent_reminders()
		shop = frappe.get_doc("Shop", self.shop)
        
		if shop.is_occupied:
			frappe.throw(f"Shop {shop.shop_number} is already occupied by another tenant.")

	def after_insert(self):
		if not self.rent_amount:
			settings = frappe.get_single("Shop Settings")
			self.rent_amount = settings.default_rent_amount

        # Update the shop to set it as occupied
		shop = frappe.get_doc("Shop", self.shop)
		shop.is_occupied = 1  # Set the shop as occupied
		shop.save()

	def before_cancel(self):
        # Set the shop as vacant when the contract is canceled
		shop = frappe.get_doc("Shop", self.shop)
		shop.is_occupied = 0  # Set the shop as vacant
		shop.save()


def send_rent_reminders():
	settings = frappe.get_single("Shop Settings")
	if not settings.enable_rent_reminders:
		return

	contracts = frappe.get_all("Contract", filters={
		"contract_end_date": (">=", today())
	}, fields=["name", "tenant", "rent_amount"])

	for contract in contracts:
		tenant = frappe.get_doc("Tenant", contract.tenant)
		if tenant.email:
			message = f"""
			Dear {tenant.tenant_name},

			This is a reminder that your rent of {contract.rent_amount} is due for this month.

			Please make the payment by the due date to avoid any late fees.

			Thank you,
			Airport Management
			"""
			frappe.sendmail(
				recipients=tenant.email,
				subject="Monthly Rent Due Reminder",
				message=message
			)
	# print("Done")
#xjss ebme wwyk gjmz
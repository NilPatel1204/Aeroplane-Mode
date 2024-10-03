# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CrewMemberData(Document):
	def before_save(self):
		self.name1 = f"{self.first_name} {self.last_name}"

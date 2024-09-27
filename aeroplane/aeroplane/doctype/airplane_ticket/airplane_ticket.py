# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		self.calculate_amount()

	def before_submit(self):
		pass
		# self.checkStatus() 

	def before_insert(self):
		self.create_randomSeat()

	def on_submit(self):
		self.changeFlightStatus()


	def calculate_amount(self):
		extra_amount = 0
		
		for item in self.add_ons:
			extra_amount += item.amount

		amount = self.flight_price + extra_amount

		self.total_amount = amount

	def checkStatus(self):
		if self.status == "Boarded":
			frappe.throw("Flight ticket is boarded")

	def create_randomSeat(self):
		if not self.seat: 	
			random_int = random.randint(1,99)
			random_char = random.choice(['A', 'B', 'C', 'D', 'E'])
			self.seat = f"{random_int}{random_char}"

	def changeFlightStatus(self):
		flight = frappe.get_doc("Airplane Flight",self.flight)
		flight.status = "Completed"
		flight.save()
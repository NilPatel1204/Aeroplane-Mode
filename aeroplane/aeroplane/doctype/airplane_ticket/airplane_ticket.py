# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		self.calculate_amount()
		self.check_seat_availability()

	def before_submit(self):
		if not self.gate_number[0].isalpha() or not self.gate_number[1:].isdigit():
			frappe.throw("Invalid Gate Number format. Example: A1, B2")
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


	def check_seat_availability(self):
		airplane_flight = frappe.get_doc("Airplane Flight", self.flight)
		airplane = frappe.get_doc("Airplane", airplane_flight.airplane)

		airplane_capacity = airplane.capacity

		existing_tickets = frappe.db.count("Airplane Ticket", filters={"flight": self.flight})
		# print(f"Existing tickets: {existing_tickets}")

		if existing_tickets >= airplane_capacity:
			frappe.throw(f"The airplane has reached its seat capacity of {airplane_capacity}. No more tickets can be issued.")
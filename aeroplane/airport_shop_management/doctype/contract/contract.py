# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate, add_months, nowdate

class Contract(Document):
    def before_save(self):
        # Check if the selected shop is already occupied
        shop = frappe.get_doc("Shop", self.shop)
        
        if shop.is_occupied:
            frappe.throw(f"Shop {shop.shop_number} is already occupied by another tenant.")
        
        # Call rent reminders, if needed
        send_rent_reminders()

    def before_cancel(self):
        # Set the shop as vacant when the contract is canceled
        shop = frappe.get_doc("Shop", self.shop)
        shop.is_occupied = 0  # Set the shop as vacant
        shop.save()

    def on_submit(self):
        if not self.rent_amount:
            # Fetch default rent amount if rent is not specified
            settings = frappe.get_single("Shop Settings")
            self.rent_amount = settings.default_rent_amount

        # Update the shop to mark it as occupied
        shop = frappe.get_doc("Shop", self.shop)
        shop.is_occupied = 1
        shop.tenant = self.tenant
        shop.save()

        # Generate the payment schedule for the contract
        generate_payment_schedule(self.name)

def send_rent_reminders():
    # Check if rent reminders are enabled in settings
    settings = frappe.get_single("Shop Settings")
    if not settings.enable_rent_reminders:
        return

    # Fetch contracts that need reminders
    contracts = frappe.get_all("Contract", filters={
        "contract_end_date": (">=", today())
    }, fields=["name", "tenant", "rent_amount"])

    # Send reminders
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

def generate_receipt_number():
    # Generate a unique receipt number based on the current date
    current_date = nowdate().replace("-", "")  # Format: YYYYMMDD

    # Fetch the last receipt number for today
    last_receipt = frappe.get_all(
        "Payment Schedular", 
        filters={"receipt_number": ["like", f"{current_date}%"]},
        order_by="receipt_number desc",
        limit=1,
        fields=["receipt_number"]
    )
    
    if last_receipt and last_receipt[0].receipt_number:
        # Extract the numeric part and increment it
        last_number = last_receipt[0].receipt_number
        numeric_part = int(last_number[-4:]) + 1  # Assuming the last 4 digits are numeric
    else:
        numeric_part = 1  # Start from 1 if no receipts exist for today

    # Format the new receipt number
    new_receipt_number = f"{current_date}-{numeric_part:04d}"  # e.g., 20231004-0001
    return new_receipt_number

def generate_payment_schedule(contract_name):
    contract = frappe.get_doc("Contract", contract_name)
    start_date = getdate(contract.contract_start_date)
    end_date = getdate(contract.contract_end_date)
    rent_amount = contract.rent_amount

    while start_date <= end_date:
        new_schedule = frappe.new_doc("Payment Schedular")
        new_schedule.contract = contract_name
        new_schedule.due_date = start_date
        new_schedule.amount = rent_amount
        new_schedule.payment_date = start_date
        new_schedule.status = "Pending"
        new_schedule.receipt_number = generate_receipt_number()
        new_schedule.insert()
        
        # Increment the start_date by one month for the next schedule
        start_date = add_months(start_date, 1)
        

def send_payment_reminders():
    # Get payment entries with status "Pending" and due within the next 3 days
    upcoming_payments = frappe.get_all("Payment Schedular", 
										filters={
											"status": "Pending",
											"due_date": ["<=", add_days(today(), 3)]
										},
										fields=["name", "tenant_email", "due_date", "amount"])

    # Send reminders for each upcoming payment
    for payment in upcoming_payments:
        frappe.sendmail(
            recipients=payment.tenant_email,
            subject="Rent Payment Due Reminder",
            message=f"Dear Tenant, your rent payment of {payment.amount} is due on {payment.due_date}. Please make the payment promptly."
        )
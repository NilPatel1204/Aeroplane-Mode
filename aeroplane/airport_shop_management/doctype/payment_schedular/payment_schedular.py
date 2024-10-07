import frappe
from frappe.model.document import Document
from frappe.utils import today, nowdate

class PaymentSchedular(Document):
    pass


def generate_receipt_number():
    current_date = nowdate().replace("-", "")
    last_receipt = frappe.get_all(
        "Payment Schedular",
        filters={"receipt_number": ["like", f"{current_date}%"]},
        order_by="receipt_number desc",
        limit=1,
        fields=["receipt_number"]
    )
    
    if last_receipt:
        last_number = int(last_receipt[0].receipt_number[-4:])
        new_number = last_number + 1
    else:
        new_number = 1

    receipt_number = f"{current_date}-{new_number:04d}"
    return receipt_number

# @frappe.whitelist()
# def record_payment(payment_schedule_name):
#     payment_schedule = frappe.get_doc("Payment Schedular", payment_schedule_name)
    
#     if payment_schedule.status != "Paid":
#         payment_schedule.status = "Paid"
#         payment_schedule.payment_date = today()
#         payment_schedule.receipt_number = generate_receipt_number()
#         payment_schedule.save()
        
#         send_receipt_to_tenant(payment_schedule)

def send_receipt_to_tenant(payment_schedule):
    tenant_email = payment_schedule.tenant_email  # Update based on your actual tenant email field
    if tenant_email:
        message = f"""
        Dear Tenant,

        We have received your payment of {payment_schedule.amount} on {payment_schedule.payment_date}.
        Your receipt number is {payment_schedule.receipt_number}.

        Thank you for your payment!

        Regards,
        Airport Management
        """
        
        frappe.sendmail(
            recipients=tenant_email,
            subject="Payment Receipt",
            message=message
        )

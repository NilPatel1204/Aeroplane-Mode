
import frappe

def get_context(context):
    context.shops = frappe.get_all("Shop", filters={"is_occupied": 0}, fields=["shop_number", "shop_name", "area", "airport"])
    context.title = "Available Shops"
    return context


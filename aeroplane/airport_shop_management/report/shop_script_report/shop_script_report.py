import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": _("Airport Name"), "fieldname": "airport_name", "fieldtype": "Link","options": "Airport", "width": 200},
        {"label": _("Total Shops"), "fieldname": "total_shops", "fieldtype": "Int", "width": 150},
    ]

    # Base query
    query = """
        SELECT 
            airport.name as airport_name, 
            COUNT(shop.name) as total_shops 
        FROM 
            `tabAirport` airport
        LEFT JOIN 
            `tabShop` shop ON shop.airport = airport.name 
    """

    # Add conditions based on filters
    conditions = []
    if filters.get("airport_name"):
        conditions.append("airport.name = %(airport_name)s")

    if filters.get("shop_status"):
        conditions.append("shop.status = %(shop_status)s")  # Assuming 'status' is a field in the 'Shop' doctype

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY airport.name"

    # Fetch data using the query
    data = frappe.db.sql(query, filters, as_dict=True)

    return columns, data

# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

import frappe
from frappe import _  


# Copyright (c) 2024, nil and contributors
# For license information, please see license.txt

import frappe
from frappe import _  


def execute(filters=None):
    columns = [
        {"label": _("Airline"), "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 150},
        {"label": _("Revenue"), "fieldname": "revenue", "fieldtype": "Currency", "width": 150}
    ]
    
    data = frappe.db.sql("""
        SELECT 
            airline.airline_name AS airline, 
            SUM(ticket.flight_price) AS revenue
        FROM `tabAirline` airline
        LEFT JOIN `tabAirplane` airplane ON airplane.airline = airline.name
        LEFT JOIN `tabAirplane Flight` flight ON flight.airplane = airplane.name
        LEFT JOIN `tabAirplane Ticket` ticket ON ticket.flight = flight.name
        GROUP BY airline.name
    """, as_dict=True)

    chart = get_chart(data)

    total_revenue = sum([d.get("revenue", 0) for d in data])
    
    data.append({
        "airline": _("Total"),
        "revenue": total_revenue,
    })

    # Create the card data
    report_summary = get_chart_data(total_revenue)

    return columns, data, None, chart, report_summary  # Return the card as part of the response

def get_chart(data):
    return {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [{"name": "Revenue By Airline","values":[d["revenue"] for d in data]}]
        },
        "type": "donut",
    }
    
def get_chart_data(total_revenue):
    return[{
		'value': total_revenue,
		'indicator': 'Green',
		'label': 'Total Revenue',
		'datatype': 'Currency',
	}]
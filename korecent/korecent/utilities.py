import frappe
from datetime import datetime
from erpnext.setup.utils import get_exchange_rate

def init_response():
    RESPONSE = frappe._dict(
        {"status": "success", "data": {}, "error": {"message": "", "traceback": ""}}
    )
    return RESPONSE

def create_order(customer, items):
    order = frappe.new_doc("Sales Order")
    order.customer = customer
    customer_currency = frappe.get_value("Customer", customer, "default_currency")
    conversion_rate = 1
    if customer_currency and customer_currency != "INR":
        conversion_rate = get_exchange_rate(customer_currency, "INR")
    order.conversion_rate = conversion_rate
    customer_shipping_address = frappe.get_all("Dynamic Link", {"link_doctype": "Customer", "link_name": customer, "parenttype": "Address"}, ["parent"], pluck="parent")
    for address in customer_shipping_address:
        if frappe.get_value("Address", address, "is_shipping_address"):
            order.shipping_address = address
            break
    
    for item in items:
        order.append(
            "items",
            {
                "doctype": "Order Item",
                "item_code": item.get("item_code"),
                "item_name": frappe.get_value("Item", item.get("item_code"), "item_name"),
                "qty": item.get("qty"),
                "size": item.get("size"),
                "rate": item.get("rate") * conversion_rate,
                "delivery_date": datetime.strptime(
                    item.get("delivery_date"), "%d-%m-%Y"
                ).date(),
                "base_rate": item.get("rate"),
                "base_amount": item.get("rate") * item.get("qty"),
                "amount": item.get("rate") * item.get("qty") * conversion_rate,
            },
        )
    order.insert(ignore_permissions=True)
    return order.name

def create_customer(customer, customer_billing_currency):
    curr = "INR"
    if customer_billing_currency and frappe.db.exists("Currency", customer_billing_currency):
        curr = customer_billing_currency
    customer_doc = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": customer,
        "default_currency": curr
    })
    customer_doc.insert(ignore_permissions=True)

def create_item(item_name, item_group=None, stock_uom=None):
    ig = "All Item Groups"
    if item_group and frappe.db.exists("Item Group", item_group):
        ig = item_group
    uom = "Nos"
    if stock_uom and frappe.db.exists("Stock UOM", stock_uom):
        uom = stock_uom
    
    item = frappe.get_doc({
        "doctype": "Item",
        "item_code": item_name,
        "item_group": ig,
        "stock_uom": uom
    })
    item.insert(ignore_permissions=True)

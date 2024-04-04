import frappe
from korecent.korecent.utilities import init_response, create_customer, create_order, create_item

@frappe.whitelist()
def create_sales_order(customer, items, customer_billing_currency=None, item_group=None, stock_uom=None):
    """
    Create a new Sales Order.

    Payload-JSON:
        dict: {
                "customer": "CUST-001",
                "items": [
                    {
                        "item_name": "Item A",
                        "qty": 10,
                        "rate": 100,
                        "delivery_date": "2024-04-30",
                        "item_group": "Product",
                        "stock_uom": "Nos"
                    },
                    {
                        "item_name": "Item B",
                        "qty": 5,
                        "rate": 200,
                        "delivery_date": "2024-04-30",
                        "item_group": "Product",
                        "stock_uom": "Nos"
                    }
                ],
                "customer_billing_currency": "INR"
            }

    Response:
        dict: {"status": "success", "data": {"sales_order": "sal-ord-01"}, "error": {"message": "", "traceback": ""}}

    Note: Add Authorization in headers with given api-key and api-secret. (e.g. "Token api-key:api-secret")
    """
    RESPONSE = init_response()
    try:
        frappe.db.savepoint("create_sales_order")
        if not frappe.db.exists("Customer", customer):
            # Create customer
            create_customer(customer, customer_billing_currency)

        for item in items:
            if not item.get("item_name") or not item.get("qty") or not item.get("rate") or not item.get("delivery_date"):
                RESPONSE["status"] = "error"
                RESPONSE["error"]["message"] = "'item_name', 'qty', 'rate' and 'delivery_date' all fields are mandatory"
                frappe.local.response.http_status_code = 400
                frappe.local.response.update(RESPONSE)
                return

            if not frappe.db.exists("Item", {"item_name": item.get("item_name")}):
                 # Create item
                 create_item(item.get("item_name"), item.get("item_group"), item.get("stock_uom"))

        # Create Order
        order = create_order(customer, items)
        RESPONSE["status"] = "success"
        RESPONSE["data"] = frappe._dict(sales_order = order)

    except Exception as e:
        frappe.db.rollback(save_point="create_sales_order")
        status_code = 500
        exception_type = type(e).__name__
        traceback = exception_type + ":" + str(e) + "\n" + frappe.get_traceback()
        error_message = f"Error in creating sales order"
        frappe.log_error(
            title=error_message,
            message=traceback,
        )
        RESPONSE["status"] = "error"
        RESPONSE["error"]["message"] = error_message
        RESPONSE["error"]["traceback"] = traceback
        frappe.local.response.http_status_code = status_code
    frappe.local.response.update(RESPONSE)
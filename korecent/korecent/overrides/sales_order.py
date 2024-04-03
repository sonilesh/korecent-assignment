import frappe
from erpnext.selling.doctype.sales_order.sales_order import make_purchase_order

def on_submit(self, func_name):
    """
    New hook method that will trigger on on_submit action on any SO and results in creating PO for each item against supplier mentioned in every item row
    """
    if self.docstatus == 1:
        supplier_items = {}
        for item in self.items:
            if item.supplier:
                if item.supplier in supplier_items:
                    supplier_items[item.supplier].append(item)
                else:
                    supplier_items[item.supplier] = [item]

        for supplier, items in supplier_items.items():
            po = make_purchase_order(self.name, items)
            po.supplier = supplier
            po.supplier_address = frappe.get_value("Supplier", supplier, "supplier_primary_address")
            po.save(ignore_permissions=True)
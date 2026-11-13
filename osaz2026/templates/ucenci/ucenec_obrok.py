import frappe
@frappe.whitelist()
def get_context(context):
    context.ucenci = frappe.get_list("Ucenci", fields=["uid", "priimek", "qr_code"])

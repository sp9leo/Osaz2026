# Copyright (c) 2024,   and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.jinja import render_template

class Ucenci(Document):
	def before_save(self):
		self.full_name = f"{self.ime} {self.priimek}"

	def validate(self):
		a=str(self.zajtrk).replace("1","Z")
		b=str(self.malica).replace("1","M")
		c=str(self.kosilo).replace("1","K")
		d=str(self.vozac).replace("1","V")
		e=str(self.dieta).replace("1","D")
		n=str(self.name)
		o = str(getattr(self, 'oddelek', ''))

		#name = random_string(12)+"000"+ a + b + c + d +e
		name = n+"-"+ a + b + c + d +e+o
		name = str(name)
		#qrcode = str(n+"0"+o)
		self.ucenec_id = name
		#self.ucenec_id = qrcode
		#self.qr_code = get_qr_code(qrcode)
		
	# pass


# ucenci.py

# import frappe
# from frappe.utils.jinja import render_template

# @frappe.whitelist()
# def get_related_prehrana_html(docname):
#     related_records = frappe.get_all('Obroki', filters={'ucenec': docname}, fields=['datum','storitev','status'])
#     context = {
#         'related_records': related_records
#     }
#     html = render_template('osazapp2024/templates/related_prehrana_list.html', context)
#     return html
import frappe
@frappe.whitelist()
def get_prehrana_data(docname):
    data = frappe.get_all('Obroki', filters={'ucenec': docname}, fields=['name', 'storitev', 'datum','status','modified'])
    return data
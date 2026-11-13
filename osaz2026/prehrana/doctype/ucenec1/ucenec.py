# Copyright (c) 2024,   and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


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
		o=str(self.oddelek)
		#name = random_string(12)+"000"+ a + b + c + d +e
		name = n+"000"+ a + b + c + d +e+o
		name = str(name)
		#qrcode = str(n+"0"+o)
		self.ucenec_id = name
		#self.ucenec_id = qrcode
		#self.qr_code = get_qr_code(qrcode)
		
	# pass


# Copyright (c) 2024,   and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Obroki(Document):
	def validate(self):
		# frappe.throw(msg=f"Odjava z datumom {self.datum} za obrok {self.storitev} in za učenca {self.ucenec} že obstaja")
		is_odjava=frappe.get_list("Odjava obroka", fields=["name"], filters={"ucenec": self.ucenec, "obrok": self.storitev,"datum":self.datum} )

		if frappe.db.exists(
			"Odjava obroka",
			{"ucenec": self.ucenec, "obrok": self.storitev, "datum": self.datum},
		):

			self.odjava = 1
			self.link_odjava = is_odjava[0].name
			print(is_odjava[0].name)
		else:
			#frappe.throw(f"ne obstaja  {self.ucenec}")
			self.odjava = 0
			self.link_odjava = ""
		
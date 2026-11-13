# Copyright (c) 2023, osaz and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.website_generator import WebsiteGenerator

class Jedilnik(WebsiteGenerator):
	# pass

    # def get_context(context):
    #     context.jedilnik = frappe.get_all("Jedilnik",fields=['*']) # type: ignore

    def validate(self):
            
            self.route = self.doctype +"/"+ self.name
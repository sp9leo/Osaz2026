# Copyright (c) 2024, osaz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import today, now, add_days, getdate, nowdate



# class Dogodek(WebsiteGenerator):
#  		print("Hello")
# 		pass


class Dogodek(Document):
    
    def validate(self):
        
        self.route = self.doctype +"/"+ self.name
        if self.event_category == "Dogodek":
            self.color = "#4463F0"
        elif self.event_category == "Dnevi dejavnosti":
            self.color = "#ECAD4B"
        
    # def validate(self):
      
    #     dogodeks = frappe.get_list("Dogodek", filters={"status": "Open"}, fields=["name", "ends_on", "repeat_till"])
    #     print (dogodeks)
    #     for dogodek in dogodeks:
    #         print (getdate(dogodek.ends_on))
    #         if (dogodek.ends_on and getdate(dogodek.ends_on) < getdate(nowdate())) or (
    #             dogodek.repeat_till and getdate(dogodek.repeat_till) < getdate(nowdate())
    #         ):
    #             self.status ="Completed"
    #             print (dogodek.name)
    #             #frappe.throw("dogodek status called")  sdfsf
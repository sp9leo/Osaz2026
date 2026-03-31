import frappe

def get_context(context):
    ## load some data and put it in context
    context.message = "Hello Portal!"

def get_context(context):
	
	context.acal= frappe.db.get_list('Sportna Dvorana',
						fields=['name', 'title'],
						
						start=10,
						page_length=20,
						as_list=True)
      

@frappe.whitelist()
def get_events():
    events = frappe.get_all('Sportna Dvorana', fields=['title', 'start', 'end', 'all_day', 'color', 'description'])
    events_list = [{
        'title': event.title,
        'start': event.start.isoformat(),
        'end': event.end.isoformat(),
        'allDay': event.all_day,
        'color': event.color,
        'description': event.description
    } for event in events]
    return events_list

def get_context(context):
    context.events = get_events()
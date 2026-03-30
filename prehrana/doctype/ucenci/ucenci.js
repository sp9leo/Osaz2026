// Copyright (c) 2024,   and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ucenci", {
  izberi_rfid(frm) {
    const ucenec = frm.doc.name;
    console.log(ucenec);

    frappe.prompt(
      {
        label: "Select RFID",
        fieldname: "rfid",
        fieldtype: "Link",
        options: "RFID", // Ensure this is the correct doctype name
        reqd: 1,
        primary_action_label: "Potrdi",
        get_query: function() {
          return {
            filters: {
              status: "Pripravljen",
              link_ucenec: ""
            }
          };
        }
      },
      values => {
        const selectedRfid = values.rfid;
        console.log(`Selected RFID: ${selectedRfid}`);

        frappe.db
          .get_doc("RFID", selectedRfid)
          .then(doc => {
            console.log(doc);
            console.log(ucenec);
            doc.status = "Aktiven";
            doc.link_ucenec = ucenec;
            frm.save();

            // Use frappe.call to update the document
            frappe.call({
              method: "frappe.client.save",
              args: {
                doc: doc
              },
              callback: function(response) {
                if (!response.exc) {
                  frappe.show_alert(
                    `Učencu ${frm.doc.full_name} dodan RFID ${selectedRfid}`
                  );
                  frm.set_value("rfid", selectedRfid);                  
                  frm.save();
                } else {
                  frappe.warn(
                    "Prišlo je do napake pri posodabljanju dokumenta."
                  );
                }
              }
            });
          })
          .catch(error => {
            console.error("Error fetching RFID document:", error);
            frappe.warn("Prišlo je do napake pri pridobivanju dokumenta RFID.");
          });
      }
    );
  }
});

frappe.ui.form.on('Ucenci', {
  refresh: function(frm) {
    // Call the server-side method to fetch data
    frappe.call({
      method: 'osazapp2024.prehrana.doctype.ucenci.ucenci.get_prehrana_data',
      args: {
        docname: frm.doc.name
      },
      callback: function(r) {
        if (r.message) {
          // Initialize the datatable
          let datatable = new DataTable(frm.fields_dict['related_prehrana_list'].wrapper, {
            columns: [
              { 
                name: 'Name', 
                id: 'name', 
                format: value => `<a class="text-primary" href="/app/prehrana/${value}" target="_blank">${value}</a>`,
                width: 1, // Adjust width ratio if needed
                editable: false
              },
              { 
                name: 'Storitev', 
                id: 'storitev',
                width: 1, // Adjust width ratio if needed
                editable: false
              },
              { 
                name: 'Status', 
                id: 'status',
                width: 1, // Adjust width ratio if needed
                editable: false
              },
              { 
                name: 'Datum', 
                id: 'datum',
                width: 1, // Adjust width ratio if needed
                editable: false
              }
            ],
            data: r.message,
            layout: 'ratio', // Adjusts column width based on ratio
            inlineFilters: true, // Enables inline filters
            serialNoColumn: true, // Adds a serial number column
            dynamicRowHeight: true, // Adjusts row height based on content
            noDataMessage: "No related records found", // Custom message when no data is available
            checkboxColumn: false, // Adds a checkbox column for row selection
            // headerDropdown: [
            //   {
            //     label: 'Export',
            //     action: function() {
            //       datatable.exportCSV();
            //     }
            //   }
            // ] // Adds a custom dropdown action in the header
          });
        }
      }
    });
  }
});


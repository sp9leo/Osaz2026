// Copyright (c) 2024,   and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Ucenec", {
// 	refresh(frm) {

// 	},
// });

// frappe.ui.form.on("Ucenci", "onload", function(frm){
//     frm.set_query("starsi", function(){
//         return {
//             filters: {
//                 "ignore_user_type": 1
//             }
//         }
//     });
// });

// TO_DO

// frappe.ui.form.on("Ucenec",{
//     izberi_rfid(frm){
//         const ucenec = frm.doc.name
//         console.log(ucenec)
//         frappe.prompt(
                
//           {
//             label: "Select RFID",
//             fieldname: "rfid",
//             fieldtype: "Link",
//             options: "RFID", // Replace with the actual doctype name
//             reqd:1,
//             primary_action_label: 'Potrdi', // Make it required (optional)
//             get_query: function() {
//               return {
//                   filters: {
//                       // Add your filter conditions here
//                       status: "Pripravljen"
//                   }
//               };
//           },
//           },
//           values => {
//             const selectedRfid = values.rfid;
//             console.log(`Selected RFID: ${selectedRfid}`);
//               //frappe.db.set_value("Ucenec", doc.name, "rfid", "");
//               frappe.db.get_doc("RFID", selectedRfid).then(doc => {
//                 console.log(doc);
//                 console.log(ucenec)
//                 doc.status = "Aktiven";
//                 doc.link_ucenec = ucenec;
//                 doc.save();
//                 frappe.msgprint("učencu"+frm.doc.full_name+"dodan rfid" + selectedRfid);
//                 frm.save();
//                 // frappe.db.set_value("RFID", selectedRfid, "ucenec", frm.doc.name);
//                 //frappe.db.set_value("RFID", selectedRfid, "status", "Aktiven");
//                 //frm.set_value("rfid", selectedRfid);
                
//                 });
//             });                 
        
        
//       }
   

        
    
// });

// // In your custom script file
// frappe.ui.form.on('Ucenec', {
//   rfid: function(frm) {
//       // Get the related document
//       frappe.db.get_doc('RFID', frm.doc.name).then(doc => {
//           // Update the field value
//           doc.status = "Aktiven";
//           doc.link_ucenec = frm.doc.full_name;
//           // Save the changes
//           frappe.db.update_doc(doc);
//       });
//   }
// });


frm.add_custom_button("Izberi RFID", () => {
           
});

frappe.ui.form.on("Ucenci", {
    izberi_rfid(frm) {
        const ucenec = frm.doc.name;
        console.log(ucenec);
        
        frappe.prompt(
            {
                label: "Select RFID",
                fieldname: "rfid",
                fieldtype: "Link",
                options: "RFID", // Replace with the actual doctype name
                reqd: 1,
                primary_action_label: 'Potrdi', // Make it required (optional)
                get_query: function() {
                    return {
                        filters: {
                            status: "Pripravljen"
                        }
                    };
                },
            },
            values => {
                const selectedRfid = values.rfid;
                console.log(`Selected RFID: ${selectedRfid}`);
                
                frappe.db.get_doc("RFID", selectedRfid).then(doc => {
                    console.log(doc);
                    console.log(ucenec);
                    doc.status = "Aktiven";
                    doc.link_ucenec = ucenec;

                    // Use frappe.call to update the document
                    frappe.call({
                        method: "frappe.client.save",
                        args: {
                            doc: doc
                        },
                        callback: function(response) {
                            if (!response.exc) {
                                frappe.msgprint("Učencu " + frm.doc.full_name + " dodan RFID " + selectedRfid);
                                frm.set_value("rfid", selectedRfid);
                                frm.save();
                            } else {
                                frappe.msgprint("Prišlo je do napake pri posodabljanju dokumenta.");
                            }
                        }
                    });
                });
            }
        );
    }
});

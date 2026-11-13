// Copyright (c) 2024,   and contributors
// For license information, please see license.txt

frappe.ui.form.on("RFID", {
  refresh: function(frm) {
    // Check if the link field is empty
    if (!frm.doc.link_ucenec) {
      // Fetch the document from Ucenci where rfid matches
      frappe.db.get_value("Ucenci", { rfid: frm.doc.name }, "name", r => {
        if (r && r.name) {
          // Set the fetched name to the link_ucenec field
          frm.set_value("link_ucenec", r.name);
          frm.set_value("status", "Aktiven");
          // frm.set_df_property("status", "read_only", 1);
          frm.save();
          frappe.show_alert("Ucenec field updated successfully");
        } else {
          frappe.show_alert("No Ucenci document found with the matching RFID");
          // frm.set_value("status", "Pripravljen");
        }
      });
    }
  },

  refresh: function(frm) {
    // Check if link_ucenec exists and status is "Aktiven"
    if (frm.doc.link_ucenec && frm.doc.status === "Aktiven") {
      // Set the status field to read-only
      frm.set_df_property("status", "read_only", 1);
    }
    else if(!frm.doc.link_ucenec && frm.doc.status === "Aktiven"){
      frappe.throw("Status ne more biti Aktiven če nima dodanega učenca", { title: "Napaka" });
    }
  }
});

frappe.ui.form.on("RFID", {
  izbrisi_rfid(frm) {
    const ucenec = frm.doc.link_ucenec;
    var rfid = frm.doc.name;
    console.log(ucenec);
    frappe.db.get_value("Ucenci", { name: ucenec }, ["ime", "priimek"])
      .then(r => {
        let values = r.message;
        console.log(values.ime, values.priimek);
        var ucenecname = values.ime + " " + values.priimek;
        // });

        frappe.warn(
          `Are you sure you want to proceed?`,
          `Osebi ${ucenecname} bo odstranjen RFID z UUID ${rfid}`,
          () => {
            // action to perform if Yes is selected

            frappe.call({
              method: "frappe.client.set_value",
              args: {
                doctype: "Ucenci",
                name: ucenec,
                fieldname: "rfid",
                value: null
              },
              callback: function(response) {
                if (!response.exc) {
                  frappe.show_alert(`${ucenec} updated successfully`);
                  frm.set_value("status", "Pripravljen");
                  frm.set_value("link_ucenec", null);
                  frm.set_df_property("status", "read_only", 0);
                  frappe.show_alert("Status field unlocked");
                  frm.save();
                  // doc.reload();
                }
              }
            });
          },
          "Nadaljuj"
          // () => {
          //     action to perform if No is selected
          // }
        );
      });
  }
});

frappe.ui.form.on('RFID', {
  refresh: function(frm) {
    // Ensure the button is rendered before applying styles
    frm.fields_dict['izbrisi_rfid'].$wrapper.find('button').html('<i class="fa fa-trash"></i> Odstrani RFID ucencu');

    // Optionally, you can also style the button
    frm.fields_dict['izbrisi_rfid'].$wrapper.find('button').css({
      'background-color': 'var(--danger)', // Red color
      'color': '#ffffff' // White text
    });
  }
});

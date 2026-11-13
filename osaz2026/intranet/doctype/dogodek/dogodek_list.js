frappe.listview_settings['Dogodek'] = {

    onload: function (listview) {

        // Add a button for doing something useful.
        listview.page.add_inner_button(__("Poišči QR"), function () {

            
            



            // change to your function's name
        })
            .addClass("btn-warning").css({ 'background': 'red', 'font-weight': 'normal', 'font-color': 'white' });
        //.addClass("btn-warning").css({'background':'darkred','font-weight': 'normal'});
        // The .addClass above is optional.  It just adds styles to the button.
    }
};
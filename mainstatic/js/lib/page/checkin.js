/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 12/14/11
 * Time: 4:24 PM
 *
 * Utils for checkin page, not big enough for app structure
 */

$(function() {
    //manually move id form field
    $('#checkin-form #id_quantity').parent("p")
        .addClass('id_quantity');

    //other text field show hide
    $('#id_freggie').change(function() {
        var option = $('#id_freggie' + ' option:selected').val();
        var label = "label[for=id_freggie_other]";
        var fieldId = "#id_freggie_other";

        if ( (option == "other_fruit") || (option == "other_veg") ) {
            $(fieldId + ', ' + label).fadeIn('fast');
            $(label).css('display', 'block');
        } else {
            $(fieldId + ', ' + label).fadeOut('fast');
        }
    });
});
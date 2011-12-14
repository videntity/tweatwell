/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 12/14/11
 * Time: 9:32 AM
 *
 */

define(["lib/utils/pubsub"],function() {
    /** Save method
     *
     * @param points
     */
    var save = function(points) {
        $.ajax({
            type: "POST",
            url: "/roulette/spin-results/",
            data: "points=" + points,
            success: function(data) {
                if (!data.exception) {
                    //alert("success");

                } else {
                    alert("fail")
                }
            }
        });
    };

    /** public methods */
    return {
        save : save
    };

});

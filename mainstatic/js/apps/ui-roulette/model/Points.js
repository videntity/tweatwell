/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 12/14/11
 * Time: 9:32 AM
 *
 */

define(["lib/utils/pubsub"],function() {
    /** Save points
     *
     * @param points
     */
    var save = function(points) {
        $.ajax({
            type: "POST",
            url: "/roulette/spin-results/",
            data: "points=" + points,
            fixture: "/",
            success: function(data) {
                if (!data.exception) {
                    $.publish('/points/save');
                } else {
                    alert("Save Failure")
                }
            }
        });
    };

    /** Save if joker badge is won */
    var saveJoker = function() {
        $.ajax({
            type: "POST",
            url: " /roulette/joker-results/",
            data: "joker_badge=true",
            fixture: "/",
            success: function(data) {
                if (!data.exception) {
                    $.publish('/points/joker');
                } else {
                    alert("Save Failure")
                }
            }
        });
    };

    /** public methods */
    return {
        save        : save,
        saveJoker   : saveJoker
    };

});

/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 11/18/11
 * Time: 12:25 PM
 *
 * Model for roulette points, simple object no private methods.
 * TODO: add service for ajax
 *
 *
 */

define([
    'jquery'
], function($) {
    return {

        /** Gets users points
         *
         * @param id userID
         */
        getPoints : function(id) {
            return true
        },

        /** Updates user points
         *
         * @param id
         * @param points
         */
        updatePoints : function(id, points) {
            return true;
        }

    };
});


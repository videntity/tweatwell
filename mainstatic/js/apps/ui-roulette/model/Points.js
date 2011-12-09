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
    var Points = {};

    /** Gets users points
     *
     * @param id    userid
     */
    Points.getPoints = function(id) {
        return true
    };

    /** Updates users points
     *
     * @param id        userid
     * @param points    points
     */
    Points.updatePoints = function(id, points) {
        return true;
    };

    return Points;

});


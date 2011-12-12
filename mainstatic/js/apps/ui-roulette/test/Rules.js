/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 12/9/11
 * Time: 3:09 PM
 *
 */

define([
    "../model/Rules"
], function (Rules) {

    module("Rules Test");
    test("Results From Rules", function() {

        expect(8);

        var points = 20;

        var result = Rules.applyRule(0, points);
        equals( 40, result.points, "Pocket 0, timesTwo" );

        result = Rules.applyRule(1, points);
        equals( 10, result.points, "Pocket 1, loseHalf" );

        result = Rules.applyRule(2, points);
        equals( 0, result.points, "Pocket 2, loseTurn" );

        result = Rules.applyRule(3, points);
        equals( 30, result.points, "Pocket 3, plusTen" );

        result = Rules.applyRule(4, points);
        equals( 'joker', result.points, "Pocket 4, joker" );

        result = Rules.applyRule(5, points);
        equals( 100, result.points, "Pocket 5, timesFive" );

        result = Rules.applyRule(6, points);
        equals( 10, result.points, "Pocket 6, minusTen" );

        result = Rules.applyRule(7, points);
        equals( 0, result.points, "Pocket 7, bankrupt" );

    });
});






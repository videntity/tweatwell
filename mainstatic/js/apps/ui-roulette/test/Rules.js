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

        equals( 40, Rules.applyRule(0, points), "Pocket 0, timesTwo" );
        equals( 10, Rules.applyRule(1, points), "Pocket 1, loseHalf" );
        equals( 20, Rules.applyRule(2, points), "Pocket 2, loseTurn" );
        equals( 30, Rules.applyRule(3, points), "Pocket 3, plusTen" );
        equals( 'joker', Rules.applyRule(4, points), "Pocket 4, joker" );
        equals( 100, Rules.applyRule(5, points), "Pocket 5, timesFive" );
        equals( 10, Rules.applyRule(6, points), "Pocket 6, minusTen" );
        equals( 0, Rules.applyRule(7, points), "Pocket 7, bankrupt" );

    });
});






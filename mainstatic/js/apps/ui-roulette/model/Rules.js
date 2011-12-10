/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 12/9/11
 * Time: 2:01 PM
 *
 * Handles the rules for each roulete pocket
 *
 */


define(function() {
    //stores the internal function name, mapped to pocket position
    var ruleTXT = [
        'timesTwo',
        'loseHalf',
        'loseTurn',
        'plusTen',
        'joker',
        'timesFive',
        'minusTen',
        'bankrupt'
    ];

    var rules = {};

    rules.timesTwo = function(points) {
        return (points * 2);
    };

    rules.loseHalf = function(points) {
        return (Math.round(points - (points/2)));
    };

    rules.loseTurn = function(points) {
        return points;
    };

    rules.plusTen = function(points) {
        return (points + 10);
    };

    rules.joker = function(points) {
        return "joker";
    };

    rules.timesFive = function(points) {
        return (points * 5);
    };

    rules.minusTen = function(points) {
        return (points - 10);
    };

    rules.bankrupt = function(points) {
        return 0;
    };


    /** Takex rule and points, returns points with rules applied
     *
     * @param ruleIndex     the index of the pocket position
     * @param points        current points pre-rules
     */
    var applyRule = function(ruleIndex, points) {
        var rule = ruleTXT[ruleIndex];

        if(typeof rules[rule] === 'function') {
            return rules[rule](points);
        } else {

            return false;
        }
    };

    /** one public method */
    return {
        applyRule : applyRule
    };

});



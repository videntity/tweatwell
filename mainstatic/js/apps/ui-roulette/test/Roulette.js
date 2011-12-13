/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 12/9/11
 * Time: 3:09 PM
 *
 */

define([
], function () {

    module("Roulette Test");

    test("Roulette UI", function() {
        expect(3);

        stop();

        var timer = setInterval(function(){test()}, 5000);

        $('#roulette-canvas').click();

        function test() {
            notEqual( $('.txt').html(), "", "txt value not empty" );
            notEqual( $('.winnings').html(),"", "winnings value not empty" );
            notEqual( $('.total').html(), "", "total value not empty" );
            clearInterval(timer);
            start();
        }

    });
});




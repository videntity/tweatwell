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
        expect(2);

        stop();
        var timer = "";


        $('#roulette-canvas').click(function(){
            timer = setInterval(function(){test()}, 5000);
        });

        function test() {
            notEqual( $('.txt').html(), "", "txt value not empty" );
            notEqual( $('.total').html(), "", "total value not empty" );
            clearInterval(timer);
            start();
        }

    });
});




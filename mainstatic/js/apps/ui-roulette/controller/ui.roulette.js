/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 *
 * Date: 12/9/11
 * Time: 8:30 AM
 *
 * Jquery UI roulette wheel, note this requires raphael which is not amd, so load as sep file.
 *
 */

define("ui.roulette", [
    "jquery",
    "apps/ui-roulette/model/Points",
    "lib/vendor/raphael/raphael-min",
    "lib/vendor/jquery-ui/jquery-ui-1.8.16.custom.min",
    "lib/utils/pubsub"
], function ($, Points) {

    $.widget("ui.roulette", {
        options: {
            arrowId     : "#roulette-arrow",
            canvas      : "roulette-canvas",
            numPockets  : 8,
            numRotations: 3
        },

        _create: function() {
            var self = this;
            self.img = null;

            self._createCanvas();

            //bind click
            $('#roulette-canvas').click(function(){
                self._spinWheel(self._getRandomPocket());
            });

        },

        /**
         * Creates raphael version of image
         */
        _createCanvas: function() {
            var self = this, o = this.options;
            var paper = Raphael(o.canvas, 350, 350);

            self.img = paper.image($(o.arrowId).attr("src"), 100, 95, 150, 150);
        },

        /**
         * Spin Animation
         */
        _spinWheel: function(pocket) {
            var self = this;
            
            //handle multiple clicks & reset
            self.img.stop();
            self.img.attr("rotation", "0");
            self.img.animate({rotation: self._calculateSpin(pocket)}, 4000, ">", function(){
                $.publish('/roulette/stop', [pocket]);
            });
        },

        /**
         * Calculate how much to spin, make sure image matches with offset
         */
        _calculateSpin: function(pocket) {
            var o = this.options;
            var pocketLocation = (360 / o.numPockets) * pocket;
            var minimumRotation = (360 * o.numRotations);
            var offset = Math.floor((360 / o.numPockets) / 2);

            //debug
            $("#roulette-result").html(pocket);
            return (pocketLocation + minimumRotation + offset);
        },

        /**
         * Calculate Random Arrow Location Based on number of elements
         */
        _getRandomPocket: function() {
            var o = this.options;
            
            return Math.floor(Math.random() * (o.numPockets - 1 + 1)) + 1;
        },

        _setOption: function(key, value) {
            switch( key ) {
                case "clear":
                    break;
            }
            $.Widget.prototype._setOption.apply(this,arguments)
        },

        destroy: function() {
            $.Widget.prototype.destroy.apply(this, arguments);
        }
        
    });
    
});
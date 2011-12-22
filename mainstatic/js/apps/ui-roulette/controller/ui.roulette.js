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
    "apps/ui-roulette/model/Rules",
    "apps/ui-roulette/model/User",
    "apps/ui-roulette/model/Points",
    "lib/vendor/raphael/raphael-min",
    "lib/vendor/jquery-ui/jquery-ui-1.8.16.custom.min",
    "lib/utils/pubsub"
], function ($, Rules, User, Points) {

    $.widget("ui.roulette", {
        options: {
            arrowId     : "#roulette-arrow",
            canvas      : "roulette-canvas",
            wagerId     : "#points-wagered",
            numPockets  : 8,
            numRotations: 3
        },

        _create: function() {
            var self = this;
            self.img = null;
            self.results = {};
            self.joker = false;

            self._createCanvas();

            //bind click if user can play
            if(User.points >= 10 && User.canSpin == "True") {
                $('#roulette-canvas').click(function(){
                    self._spinWheel(self._getRandomPocket());
                    $(this).unbind('click');
                });
            }
        },


        /**
         * Creates raphael version of image
         */
        _createCanvas: function() {
            var self = this, o = this.options;
            var paper = Raphael(o.canvas, 350, 350);

            self.img = paper.image($(o.arrowId).attr("src"), 145, 0, 58, 350);
            //stupid ie8 hack, set angle to 0 to force display
            self.img.attr("rotation", "0");
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
                self._getResult(pocket);
                self._updateInterface();
                self._save();
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

            return (pocketLocation + minimumRotation + offset);
        },

        /**
         * Calculate Random Arrow Location Based on number of elements
         */
        _getRandomPocket: function() {
            var o = this.options;
            
            return Math.floor(Math.random() * (o.numPockets));
        },

        /** Gets result based on landed pocket and wager, stores in widget object
         *
         * @param pocket
         */
        _getResult: function(pocket) {
            var self = this, o = this.options;
            var wager = self._getWager();

            self.results = Rules.applyRule(pocket, wager);

            //handle joker
            if(self.results.points == "joker") {
                self.results.points = "";
                self.joker = true;
                //to test here for existing badge and allow spin again
            }
        },

        /**
         * Returns user selected wager amount
         */
        _getWager: function() {
            var o = this.options;
            return $(o.wagerId + ' option:selected').val();
        },

        /**
         * Updates interface
         */
        _updateInterface: function() {
            var self = this;

            $('.rt-winnings').html(self.results.points);
            $('.rt-total').html((User.points + self.results.points));

            $('#result .txt').html(self.results.resultTxt);

            $("#wager-form").hide();
            $("#result").fadeIn();
        },

        /**
         * Save method, handles joker
         */
        _save: function() {
            var self = this;

            if(self.joker) {
                Points.saveJoker();
            } else {
                Points.save(self.results.points);
            }

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
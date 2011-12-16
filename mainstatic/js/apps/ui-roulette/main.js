/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 *
 * Date: 12/9/11
 * Time: 8:30 AM
 *
 * Boostrap file for roulette wheel
 *
 */

require([
    'jquery',
    'lib/utils/domReady',
    'apps/ui-roulette/controller/ui.roulette'
], function ($, domReady) {

    domReady.withResources(function () {
        $("#roulette").roulette();
    });

});

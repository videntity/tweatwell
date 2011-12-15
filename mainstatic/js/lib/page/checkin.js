/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 12/14/11
 * Time: 4:24 PM
 *
 * Utils for checkin page, not big enough for app structure
 */

$(function() {
    //comments
    $('.tw-comment-trigger').click(function(){
        $(this).parent('.tweat-comments').find('.tweat-comment-form').slideToggle();
        return false;
    });
});
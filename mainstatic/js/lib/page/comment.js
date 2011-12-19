/**
 * Copyright (c) 2011 DevPatch (http://www.devpatch.com)
 * Licensed under the GPL license
 *
 * Date: 12/19/11
 * Time: 2:58 PM
 *
 *  Utils for comments
 */

$(function() {

    //comments show hide
    $('.tw-comment-trigger').click(function(){
        $(this).parent('.tw-comments').find('.tw-comment-form').slideToggle();
        return false;
    });

});

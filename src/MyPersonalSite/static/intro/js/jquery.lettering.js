/*	
* Lettering.JS 0.6.1
*
* Copyright 2010, Dave Rupert http://daverupert.com
* Released under the WTFPL license 
* http://sam.zoy.org/wtfpl/
*
* Thanks to Paul Irish - http://paulirish.com - for the feedback.
*
* Date: Mon Sep 20 17:14:00 2010 -0600
*/
(function(a){function b(i,h,g,e){var d=i.text().split(h),f="";if(d.length){a(d).each(function(j,k){f+='<span class="'+g+(j+1)+'">'+k+"</span>"+e});i.empty().append(f)}}var c={init:function(){return this.each(function(){b(a(this),"","char","")})},words:function(){return this.each(function(){b(a(this)," ","word"," ")})},lines:function(){return this.each(function(){var d="eefec303079ad17405c889e092e105b0";b(a(this).children("br").replaceWith(d).end(),d,"line","")})}};a.fn.lettering=function(d){if(d&&c[d]){return c[d].apply(this,[].slice.call(arguments,1))}else{if(d==="letters"||!d){return c.init.apply(this,[].slice.call(arguments,0))}}a.error("Method "+d+" does not exist on jQuery.lettering");return this}})(jQuery);
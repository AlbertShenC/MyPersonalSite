$("#contact-form").submit(function(){var a=$(this).attr("action");$("#message").slideUp(750,function(){$("#message").hide();$("#submit").before("").attr("disabled","disabled");$.post(a,{name:$("#name").val(),email:$("#email").val(),comments:$("#comments").val(),},function(b){document.getElementById("message").innerHTML=b;$("#message").slideDown("slow");$("#cform img.contact-loader").fadeOut("slow",function(){$(this).remove()});$("#submit").removeAttr("disabled");if(b.match("success")!=null){$("#cform").slideUp("slow")}})});return false});
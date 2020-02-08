//回到顶部
$(function () {
    $('#to-top').click(function () {
        $('html,body').animate({scrollTop: 0}, 500);
    });
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('#to-top').fadeIn(300);
        } else {
            $('#to-top').stop().fadeOut(300);
        }
    }).scroll();
});

//标题栏鼠标滑过显示下拉
$(function() {
	var $dropdownLi = $('ul.navbar-nav > li.dropdown');
	$dropdownLi.mouseover(function() {
		$(this).addClass('show');
		$(this).children('a.dropdown-toggle').attr('aria-expanded', 'true');
		$(this).children('div.dropdown-menu').addClass('show')
	}).mouseout(function() {
		$(this).removeClass('show');
		$(this).children('a.dropdown-toggle').attr('aria-expanded', 'false');
		$(this).children('div.dropdown-menu').removeClass('show')
	})
});

//下滑时隐藏导航条
$(function () {
	var header = document.querySelector(".blog-navbar");
	var headroom = new Headroom(header);
	headroom.init();
});

/*!
 * KiCad js
 */

(function(){
	
if( $('.navbar').hasClass('transparent') )
{
	$(window).scroll(function() {
		if($(this).scrollTop() < 430) { 
			$('.navbar').addClass('transparent');
		} else {
			$('.navbar').removeClass('transparent');
		}
	});
}

	$(window).resize(function() {
		var mobileLimit = 760;
		if ($(window).width() < mobileLimit) {
			$('.navbar').addClass('navbar-static-top');
			$('.navbar').removeClass('navbar-fixed-top');
			$('header').addClass('page-header-decor-no-margin');
		}
		else 
		{
			$('.navbar').removeClass('navbar-static-top');
			$('.navbar').addClass('navbar-fixed-top');
			$('header').removeClass('page-header-decor-no-margin');
		}
	});
	$(window).trigger('resize');

})();
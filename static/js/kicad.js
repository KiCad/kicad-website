/*!
 * KiCad js
 */

(function(){
	
if( $('.navbar').hasClass('transparent') )
{
	$(window).scroll(function() {

		if($(this).scrollTop() < 430) { 
			$('.navbar').addClass('transparent'); // adding the opaque class
		} else {
			$('.navbar').removeClass('transparent'); // removing the opaque class
		}
	});
}
})();
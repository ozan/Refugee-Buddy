$(function () {
	// remove messages when close button clicked
	$('.messages .close-button').bind('click', function () {
		$(this).parent().fadeOut().slideUp('fast', function () {
			$(this).remove();
			$('.messages').each(function () {
				if ($(this).children().length === 0) {
					$(this).remove();
				}
			});
		});
	});
});
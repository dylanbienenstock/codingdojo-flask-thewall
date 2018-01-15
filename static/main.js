$(function() {
	$(document).on("click", ".message-box", function() {
		var messageId = $(this).attr("data-message-id");
		var container = $("#reply-container-" + messageId);
		container.stop().slideToggle();
	});
});
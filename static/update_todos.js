$(document).ready(function() {
	$("#submit_todo").hide();
	$("input[name='priority']").on('click', function(evt) {
		$.post('/add_todo', $('.add-todo').serialize()).done(function(data) {
			$('.todos').replaceWith($($.parseHTML(data)).filter(".todos"));
			$('.add-todo').trigger("reset");
		});
	});
});
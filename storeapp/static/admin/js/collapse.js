(function($) {
	$(document).ready(function() {
		// Add anchor tag for Show/Hide link
		$("fieldset.collapse").each(function(i, elem) {
			// Don't hide if fields in this fieldset have errors
			if ($(elem).find("div.errors").length == 0) {
				$(elem).addClass("collapsed").find("h2").first().append(' (<a id="fieldsetcollapser' +
					i +'" class="collapse-toggle" href="#">' + gettext("Show") +
					'</a>)');
			}
		});
		// Add toggle to anchor tag
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
		$("fieldset.collapse a.collapse-toggle").toggle(
			function() { // Show
				$(this).text(gettext("Hide")).closest("fieldset").removeClass("collapsed").trigger("show.fieldset", [$(this).attr("id")]);
				return false;
			},
			function() { // Hide
				$(this).text(gettext("Show")).closest("fieldset").addClass("collapsed").trigger("hide.fieldset", [$(this).attr("id")]);
				return false;
			}
		);
=======
=======
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
		$("fieldset.collapse a.collapse-toggle").click(function(ev) {
			if ($(this).closest("fieldset").hasClass("collapsed")) {
				// Show
				$(this).text(gettext("Hide")).closest("fieldset").removeClass("collapsed").trigger("show.fieldset", [$(this).attr("id")]);
			} else {
				// Hide
				$(this).text(gettext("Show")).closest("fieldset").addClass("collapsed").trigger("hide.fieldset", [$(this).attr("id")]);
			}
			return false;
		});
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
	});
})(django.jQuery);

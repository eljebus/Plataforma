(function($) {
	$.fn.actions = function(opts) {
		var options = $.extend({}, $.fn.actions.defaults, opts);
		var actionCheckboxes = $(this);
		var list_editable_changed = false;
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
		checker = function(checked) {
=======
		var checker = function(checked) {
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
		var checker = function(checked) {
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
		var checker = function(checked) {
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
			if (checked) {
				showQuestion();
			} else {
				reset();
			}
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
			$(actionCheckboxes).attr("checked", checked)
				.parent().parent().toggleClass(options.selectedClass, checked);
		}
=======
			$(actionCheckboxes).prop("checked", checked)
				.parent().parent().toggleClass(options.selectedClass, checked);
		},
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
			$(actionCheckboxes).prop("checked", checked)
				.parent().parent().toggleClass(options.selectedClass, checked);
		},
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
			$(actionCheckboxes).prop("checked", checked)
				.parent().parent().toggleClass(options.selectedClass, checked);
		},
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
		updateCounter = function() {
			var sel = $(actionCheckboxes).filter(":checked").length;
			$(options.counterContainer).html(interpolate(
			ngettext('%(sel)s of %(cnt)s selected', '%(sel)s of %(cnt)s selected', sel), {
				sel: sel,
				cnt: _actions_icnt
			}, true));
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
			$(options.allToggle).attr("checked", function() {
=======
			$(options.allToggle).prop("checked", function() {
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
			$(options.allToggle).prop("checked", function() {
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
			$(options.allToggle).prop("checked", function() {
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
				if (sel == actionCheckboxes.length) {
					value = true;
					showQuestion();
				} else {
					value = false;
					clearAcross();
				}
				return value;
			});
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
		}
=======
		},
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
		},
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
		},
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
		showQuestion = function() {
			$(options.acrossClears).hide();
			$(options.acrossQuestions).show();
			$(options.allContainer).hide();
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
		}
=======
		},
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
		},
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
		},
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
		showClear = function() {
			$(options.acrossClears).show();
			$(options.acrossQuestions).hide();
			$(options.actionContainer).toggleClass(options.selectedClass);
			$(options.allContainer).show();
			$(options.counterContainer).hide();
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
		}
=======
		},
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
		},
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
		},
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
		reset = function() {
			$(options.acrossClears).hide();
			$(options.acrossQuestions).hide();
			$(options.allContainer).hide();
			$(options.counterContainer).show();
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
		}
=======
		},
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
		},
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
		},
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
		clearAcross = function() {
			reset();
			$(options.acrossInput).val(0);
			$(options.actionContainer).removeClass(options.selectedClass);
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
		}
=======
		};
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
		};
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
		};
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
		// Show counter by default
		$(options.counterContainer).show();
		// Check state of checkboxes and reinit state if needed
		$(this).filter(":checked").each(function(i) {
			$(this).parent().parent().toggleClass(options.selectedClass);
			updateCounter();
			if ($(options.acrossInput).val() == 1) {
				showClear();
			}
		});
		$(options.allToggle).show().click(function() {
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
			checker($(this).attr("checked"));
=======
			checker($(this).prop("checked"));
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
			checker($(this).prop("checked"));
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
			checker($(this).prop("checked"));
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
			updateCounter();
		});
		$("div.actions span.question a").click(function(event) {
			event.preventDefault();
			$(options.acrossInput).val(1);
			showClear();
		});
		$("div.actions span.clear a").click(function(event) {
			event.preventDefault();
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
			$(options.allToggle).attr("checked", false);
=======
			$(options.allToggle).prop("checked", false);
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
			$(options.allToggle).prop("checked", false);
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
			$(options.allToggle).prop("checked", false);
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
			clearAcross();
			checker(0);
			updateCounter();
		});
		lastChecked = null;
		$(actionCheckboxes).click(function(event) {
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
			if (!event) { var event = window.event; }
			var target = event.target ? event.target : event.srcElement;
			if (lastChecked && $.data(lastChecked) != $.data(target) && event.shiftKey == true) {
				var inrange = false;
				$(lastChecked).attr("checked", target.checked)
=======
=======
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
			if (!event) { event = window.event; }
			var target = event.target ? event.target : event.srcElement;
			if (lastChecked && $.data(lastChecked) != $.data(target) && event.shiftKey === true) {
				var inrange = false;
				$(lastChecked).prop("checked", target.checked)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
					.parent().parent().toggleClass(options.selectedClass, target.checked);
				$(actionCheckboxes).each(function() {
					if ($.data(this) == $.data(lastChecked) || $.data(this) == $.data(target)) {
						inrange = (inrange) ? false : true;
					}
					if (inrange) {
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
						$(this).attr("checked", target.checked)
=======
						$(this).prop("checked", target.checked)
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
						$(this).prop("checked", target.checked)
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
						$(this).prop("checked", target.checked)
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
							.parent().parent().toggleClass(options.selectedClass, target.checked);
					}
				});
			}
			$(target).parent().parent().toggleClass(options.selectedClass, target.checked);
			lastChecked = target;
			updateCounter();
		});
		$('form#changelist-form table#result_list tr').find('td:gt(0) :input').change(function() {
			list_editable_changed = true;
		});
		$('form#changelist-form button[name="index"]').click(function(event) {
			if (list_editable_changed) {
				return confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."));
			}
		});
		$('form#changelist-form input[name="_save"]').click(function(event) {
			var action_changed = false;
			$('div.actions select option:selected').each(function() {
				if ($(this).val()) {
					action_changed = true;
				}
			});
			if (action_changed) {
				if (list_editable_changed) {
					return confirm(gettext("You have selected an action, but you haven't saved your changes to individual fields yet. Please click OK to save. You'll need to re-run the action."));
				} else {
					return confirm(gettext("You have selected an action, and you haven't made any changes on individual fields. You're probably looking for the Go button rather than the Save button."));
				}
			}
		});
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
	}
=======
	};
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
	};
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
	};
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
	/* Setup plugin defaults */
	$.fn.actions.defaults = {
		actionContainer: "div.actions",
		counterContainer: "span.action-counter",
		allContainer: "div.actions span.all",
		acrossInput: "div.actions input.select-across",
		acrossQuestions: "div.actions span.question",
		acrossClears: "div.actions span.clear",
		allToggle: "#action-toggle",
		selectedClass: "selected"
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
	}
=======
	};
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
	};
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
	};
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214
})(django.jQuery);

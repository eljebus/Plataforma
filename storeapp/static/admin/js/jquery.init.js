/* Puts the included jQuery into our own namespace using noConflict and passing
 * it 'true'. This ensures that the included jQuery doesn't pollute the global
 * namespace (i.e. this preserves pre-existing values for both window.$ and
 * window.jQuery).
 */
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
var django = {
    "jQuery": jQuery.noConflict(true)
};
=======
var django = django || {};
django.jQuery = jQuery.noConflict(true);
>>>>>>> 9bf5737486435174b671ca752f3fb50ab92d0c1a
=======
var django = django || {};
django.jQuery = jQuery.noConflict(true);
>>>>>>> 4157af1dcf4cac4cd7759dd2e39135ae038ddfbd
=======
var django = django || {};
django.jQuery = jQuery.noConflict(true);
>>>>>>> 8e10ecd6f2e11ef996d80983b30e3f4e8c02a214

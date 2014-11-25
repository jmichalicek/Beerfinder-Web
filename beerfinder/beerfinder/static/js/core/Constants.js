define([], function() {
    var constants = {};
    constants.GEOLOCATION_FAIL_DENIED = 1;
    constants.GEOLOCATION_FAIL_UNAVAILABLE = 2;
    constants.GEOLOCATION_FAIL_TIMEOUT = 3;
    constants.GEOLOCATION_DENIED_MESSAGE = "You have declined access to your location.  Some features will not work.";
    constants.GEOLOCATION_UNAVAILABLE_MESSAGE = "We were unable to determine your location.  Some features will not work.";
    constants.GEOLOCATION_TIMEOUT_MESSAGE = constants.GEOLOCATION_UNAVAILABLE_MESSAGE;
    return Object.freeze(constants);
});

define([], function() {
    var constants = {};
    constants.GEOLOCATION_FAIL_DENIED = 1;
    constants.GEOLOCATION_FAIL_UNAVAILABLE = 2;
    constants.GEOLOCATION_FAIL_TIMEOUT = 3;
    return Object.freeze(constants);
});

define([], function() {
    var channels = {};
    channels.GEOLOCATION =  'GeoLocation';
    channels.GEOLOCATION_SUCCESS = channels.GEOLOCATION + '.success';
    channels.GEOLOCATION_START = channels.GEOLOCATION + '.start';
    channels.GEOLOCATION_DENIED = channels.GEOLOCATION + '.denied';
    channels.GEOLOCATION_UNAVAILABLE = channels.GEOLOCATION + '.unavailable';
    channels.GEOLOCATION_TIMEOUT = channels.GEOLOCATION + '.timeout';
    channels.GEOLOCATION_DONE = channels.GEOLOCATION + '.done'; // done for any reason
    channels.ERRORS = 'Errors';
    channels.ERRORS_CLEAR = channels.ERRORS + '.clear';
    channels.ERRORS_SET = channels.ERRORS + '.set';
    channles.ERRORS_APPEND = channels.ERRORS + '.append';
    return Object.freeze(channels);
});

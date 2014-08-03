define([], function() {
    var channels = {};
    channels.GEOLOCATION =  'GeoLocation';
    channels.GEOLOCATION_SUCCESS = channels.GEOLOCATION + '.success';
    channels.GEOLOCATION_START = channels.GEOLOCATION + '.start';
    channels.GEOLOCATION_DENIED = channels.GEOLOCATION + '.denied';
    channels.GEOLOCATION_UNAVAILABLE = channels.GEOLOCATION + '.unavailable';
    channels.GEOLOCATION_TIMEOUT = channels.GEOLOCATION + '.timeout';
    channels.GEOLOCATION_DONE = channels.GEOLOCATION + '.done'; // done for any reason
    return Object.freeze(channels);
});

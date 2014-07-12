define([], function() {
    var channels = {};
    channels.GEOLOCATION =  'GeoLocation';
    channels.GEOLOCATION_SUCCESS = channels.GEOLOCATION + '.success';
    channels.GEOLOCATION_START = channels.GEOLOCATION + '.start';
   
    return Object.freeze(channels);
});

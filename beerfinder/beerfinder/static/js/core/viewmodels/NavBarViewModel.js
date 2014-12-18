define(['knockout', 'pubsub', 'core/PubSubChannels'], function(ko, PubSub, PubSubChannels) {
    return function () {
        "use strict";
        var self = this;

        this.location = ko.observable();
        this.locationUpdating = ko.observable(false);

        this.geoLocationLowAccuracy = function () {
            /* Callback to use for if high accuracy geolocation fails we can try low accuracy instead */
            navigator.geolocation.getCurrentPosition(self.geoLocationCallback, self.publishGeoLocationError,
                                                     {enableHighAccuracy: false, timeout: 5000, maximumAge: 30000});
        };

        this.updateLocation = function () {
            self.locationUpdating(true);
            PubSub.publish(PubSubChannels.GEOLOCATION_START, {});
            navigator.geolocation.getCurrentPosition(self.locationSuccess, self.geoLocationLowAccuracy,
                                                     {enableHighAccuracy: true, timeout: 5000, maximumAge: 30000});
            $('#nav-update-location').blur();
        };

        this.locationSuccess = function (position) {
            self.locationUpdating(false);
            PubSub.publish(PubSubChannels.GEOLOCATION_SUCCESS, position);
        };

        this.locationError = function () {
            self.locationUpdating(false);
        };

        self.geoLocationStartMessageHandler = function (msg, data) {
            self.locationUpdating(true);
        };

        self.geoLocationSuccessMessageHandler = function (msg, data) {
            self.locationUpdating(false);
        };

        PubSub.subscribe(PubSubChannels.GEOLOCATION_SUCCESS, self.geoLocationSuccessMessageHandler);
        PubSub.subscribe(PubSubChannels.GEOLOCATION_START, self.geoLocationStartMessageHandler);
        PubSub.subscribe(PubSubChannels.GEOLOCATION_DONE, self.geoLocationSuccessMessageHandler);

    };
});

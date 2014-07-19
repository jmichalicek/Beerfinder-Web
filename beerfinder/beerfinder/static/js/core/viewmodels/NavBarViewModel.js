define(['knockout', 'pubsub', 'core/PubSubChannels'], function(ko, PubSub, PubSubChannels) {
    return function () {
        "use strict";
        var self = this;

        this.location = ko.observable();
        this.locationUpdating = ko.observable(false);
        this.updateLocation = function () {
            self.locationUpdating(true);  // viewModel does not listen to it's own sent messages
            PubSub.publish(PubSubChannels.GEOLOCATION_START, {});
            navigator.geolocation.getCurrentPosition(self.locationSuccess, self.locationError);
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

        PubSub.subscribe(PubSubChannels.GEOLOCATION_SUCCESS, self.getLocationSuccessMessageHandler);
        PubSub.subscribe(PubSubChannels.GEOLOCATION_START, self.getLocationStartMessageHandler);

    };
});
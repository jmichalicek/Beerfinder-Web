define(['knockout', 'pubsub', 'core/PubSubChannels'], function(ko, PubSub, PubSubChannels) {
    return function () {
        "use strict";
        var self = this;

        this.location = ko.observable();
        this.updateLocation = function () {
            PubSub.publish(PubSubChannels.GEOLOCATION_START, {});
            navigator.geolocation.getCurrentPosition(self.locationSuccess, self.locationError);
        };

        this.locationSuccess = function (position) {
            PubSub.publish(PubSubChannels.GEOLOCATION_SUCCESS, position);
        };

        this.locationError = function () {
        };

    };
});
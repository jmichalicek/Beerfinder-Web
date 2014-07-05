define([], function() {
    return function () {
        "use strict";
        var self = this;

        this.successCallbacks = [];
        this.failureCallbacks = [];
        this.location = null;

        this.doSuccesCallbacks = function (position) {
            var callbackCount = self.successCallbacks.length;
            for(var i = 0; i < callbackCount; i++) {
                self.successCallbacks[i](position);
            };
        };

        this.doFailureCallbacks = function (err) {
            var callbackCount = self.failureCallbacks.length;
            for(var i = 0; i < callbackCount; i++) {
                self.failureCallbacks[i](err);
            }
        };

        this.locationSuccess = function (position) {
            self.location = position;
            self.doSuccesCallbacks(position);
        };

        this.registerSuccessCallback = function (callable) {
            self.successCallbacks.push(callable);
        };

        this.registerFailureCallback = function (callable) {
            self.failureCallbacks.push(callable);
        };

        this.getLocation = function (maximumAge) {
            /* should maybe default to 0 and just specify longer times if desired when called */
            maximumAge = (!!maximumAge || maximumAge === 0 ) ? maximumAge : 30000;
            navigator.geolocation.getCurrentPosition(self.locationSuccess, self.doFailureCallbacks, {maximumAge: maximumAge});
        };
    };
});
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

        this.getLocation = function () {
            navigator.geolocation.getCurrentPosition(self.locationSuccess, self.doFailureCallbacks, {maximumAge: 300000});
        };
    };
});
define(['knockout', 'pubsub', 'core/PubSubChannels'], function(ko, PubSub, PubSubChannels) {
    return function () {
        "use strict";
        var self = this;

        this.errorMessages = ko.observableArray([]);

        this.clearErrorMessages = function (msg, data) {
            self.errorMessages([]);
        };

        this.setErrorMessages = function (msg, data) {
            self.errorMessages(data);
        };

        this.appendErrorMessages = function (msg, data) {
            var m = self.errorMessages();
            m.concat(data);
            self.errorMessages(m);
        };

        PubSub.subscribe(PubSubChannels.ERRORS_CLEAR, self.clearErrorMessages);
        PubSub.subscribe(PubSubChannels.ERRORS_SET, self.setErrorMessages);
        PubSub.subscribe(PubSubChannels.ERRORS_APPEND, self.appendErrorMessages);
    };
});

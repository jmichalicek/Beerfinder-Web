define(['knockout'], function (ko) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};
        
        self.firstName = ko.observable(data.first_name);
        self.lastName = ko.observable(data.last_name);
        self.email = ko.observable(data.email);
        self.username = ko.observable(data.username);
        self.showNameOnSightings =  ko.observable(data.show_name_on_sightings);
        self.sendWatchlistEmail = ko.observable(data.send_watchlist_email);
        
        this.toApiFormData = function () {
            return {first_name: self.firstName(),
                    last_name: self.lastName(),
                    email: self.email(),
                    username: self.username(),
                    show_name_on_sightings: self.showNameOnSightings(),
                    send_watchlist_email: self.sendWatchlistEmail(),
                   }
        };
        
    };
});
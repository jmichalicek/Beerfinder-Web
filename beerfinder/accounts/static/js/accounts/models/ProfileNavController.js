define(['knockout'], function (ko) {
    return function () {
        "use strict";
        var self = this;
        this.ProfileSections = {
            PROFILE: 'profile',
            WATCHLIST: 'watchlist'
        };

        this.activeView = ko.observable(self.ProfileSections.PROFILE);
    };
});

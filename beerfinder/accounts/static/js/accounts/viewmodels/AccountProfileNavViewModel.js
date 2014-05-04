/*
var ProfileSections = {
    PROFILE: 'profile',
    WATCHLIST: 'watchlist'
};

var activeView = ko.observable(ProfileSections.PROFILE);
*/

define(['knockout'], function (ko) {

    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.profileNavController = data.profileNavController;

        this.showProfile = function () {
            self.profileNavController.activeView(self.profileNavController.ProfileSections.PROFILE);
        };

        this.showWatchList = function () {
            self.profileNavController.activeView(self.profileNavController.ProfileSections.WATCHLIST);
        };
    };
});

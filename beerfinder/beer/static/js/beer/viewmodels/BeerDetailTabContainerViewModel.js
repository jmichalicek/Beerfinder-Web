var SightingTabs = {RECENT: 'recent', NEARBY: 'nearby'};

define(['knockout'], function(ko) {
    return function() {
        "use strict";
        var self = this;

        this.activeSightingTab = ko.observable(SightingTabs.RECENT);

        this.changeTab = function (section) {
            self.activeSightingTab(section);
        };
    };
});
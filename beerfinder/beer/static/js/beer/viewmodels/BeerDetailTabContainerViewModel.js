var BeerDetailTabContainerViewModel = function() {
    var self = this;
    this.activeSightingTab = ko.observable(SightingTabs.RECENT);

    this.changeTab = function (section) {
        self.activeSightingTab(section);
    };
};
// TODO: Paginate sighting lists

var SightingTabs = {RECENT: 'recent', NEARBY: 'nearby'};

var ViewModel = function (data) {
    var self = this;
    this.activeNavSection = ko.observable('beer_list');
    this.beer = ko.observable(new BeerModel(data.beer));
    this.sightings = ko.observableArray();
    //this.activeSightingTab = ko.observable(SightingTabs.RECENT);

    /*this.getSightings = function () {
        $.ajax({url: '/api/sightings/',
                method: 'GET',
                data: {beer_slug: self.beer().slug()}
               }).done(function (data) {
                   ko.utils.arrayForEach(data.results, function(item) {
                       self.sightings.push(new SightingModel(item));
                   });
               });
    };*/

    // TODO: Maybe add something to api which shows whether beer is in the user's watchlist or not
    // and have remove from watchlist if it is already there and change that after adding
    this.addToWatchlist = function (data) {
        $.ajax({
            url: '/api/watchlist/',
            type: 'POST',
            data: {'beer': self.beer().slug()}
        }).done(function (data) {
            alert("Added to watchlist");
        }).fail(function (data) {
            console.log("error adding beer to watchlist: " + data);
        });
    };

    /*this.changeTab = function (section) {
        self.activeSightingTab(section);
    };*/
};

var TabContainerViewModel = function() {
    var self = this;
    this.activeSightingTab = ko.observable(SightingTabs.RECENT);
    
    this.changeTab = function (section) {
        self.activeSightingTab(section);
    };
};

var RecentSightingListViewModel = function (data) {
    'use strict';
    var self = this;
    data = typeof data !== 'undefined' ? data : {};

    this.tabManager = data.tabManager;
    this.parentViewModel = data.parentView;
    this.sightings = ko.observableArray();
    this.getSightings = function () {
        $.ajax({url: '/api/sightings/',
                method: 'GET',
                data: {beer_slug: self.parentViewModel.beer().slug()}
               }).done(function (data) {
                   ko.utils.arrayForEach(data.results, function(item) {
                       self.sightings.push(new SightingModel(item));
                   });
               });
    };
};


var NearbySightingListViewModel = function (data) {
    'use strict';
    var self = this;
    data = typeof data !== 'undefined' ? data : {};
    this.location = {};
    this.tabManager = data.tabManager;
    this.parentViewModel = data.parentView;
    this.sightings = ko.observableArray();

    this.initialize = function () {
        navigator.geolocation.getCurrentPosition(self.getNearbySightings);
    };

    this.getNearbySightings = function (position) {
        // to be used as a callback for html5 geolocation
        self.location = position;
        self.getSightings();
    }

    this.getSightings = function () {
        if(!self.location.coords) {
            self.initialize();
            return false;
        }
        var requestParams = {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude, beer_slug: self.parentViewModel.beer().slug()};
        $.ajax({url: '/api/sightings/nearby/',
                method: 'GET',
                data: requestParams,
               }).done(function (data) {
                   ko.utils.arrayForEach(data.results, function(item) {
                       self.sightings.push(new SightingModel(item));
                   });
               });
    };
};
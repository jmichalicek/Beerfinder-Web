
define(['jquery', 'knockout', 'vendor/infinitescroll', 'pubsub', 'core/PubSubChannels', 'sighting/models/SightingModel', 'core/models/LocationManagerModel', 'beer/models/BeerModel'], function($, ko, infinitescroll, PubSub, PubSubChannels, SightingModel, LocationManagerModel, BeerModel) {
    return function (data) {
        'use strict';
        var self = this;
        data = typeof data !== 'undefined' ? data : {};
        
        this.showLoadingSpinner = ko.observable(false);
        this.location = data.location || {};
        this.tabManager = data.tabManager;
        this.parentViewModel = data.parentView;
        this.sightings = ko.observableArray();
        this.beer = ko.observable(new BeerModel(data.beer));
        
        this.initialize = function () {
            self.showLoadingSpinner(true);
            navigator.geolocation.getCurrentPosition(self.getNearbySightings, {maximumAge: 30000});
        };
        
        this.getNearbySightings = function (position) {
            // to be used as a callback for html5 geolocation
            self.location = position;
            self.getSightings();
        };
        
        this.getSightings = function () {
            if(!self.location.coords) {
                self.initialize();
                return false;
            }
            self.parentViewModel.beer().getNearbySightings(self.location.coords.latitude,
                                                           self.location.coords.longitude
                                                          ).done(function (data) {
                                                              ko.utils.arrayForEach(data.results, function(item) {
                                                                  self.sightings.push(new SightingModel(item));
                                                              });
                                                          }).always(function (data) {
                                                              self.showLoadingSpinner(false);
                                                          });
        };


        this.geoLocationComplete = function (msg, data) {
            /* data is going to be a location object with coords, etc */
            self.sightings([]);
            self.getNearbySightings(data);
        };

        // initialization stuff
        self.locationManager.registerSuccessCallback(self.getNearbySightings);
        //PubSub.subscribe('GeoLocation.start', self.geoLocationStartedListener);
        PubSub.subscribe(PubSubChannels.GEOLOCATION_SUCCESS, self.geoLocationComplete);
    };
});

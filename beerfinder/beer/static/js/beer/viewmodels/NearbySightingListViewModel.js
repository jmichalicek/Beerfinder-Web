
define(['jquery', 'knockout', 'vendor/infinitescroll', 'sighting/models/SightingModel', 'core/models/LocationManagerModel'], function($, ko, infinitescroll, SightingModel, LocationManagerModel) {
    return function (data) {
        'use strict';
        var self = this;
        data = typeof data !== 'undefined' ? data : {};
        
        this.showLoadingSpinner = ko.observable(false);
        this.location = data.location || {};
        this.tabManager = data.tabManager;
        this.parentViewModel = data.parentView;
        this.sightings = ko.observableArray();
        this.locationManager = data.locationManager || new LocationManagerModel();
        
        this.initialize = function () {
            self.showLoadingSpinner(true);
            self.locationManager.getLocation();
        };
        
        this.getNearbySightings = function (position) {
            // to be used as a callback for html5 geolocation
            self.location = position;
            self.getSightings();
        };
        
        this.getSightings = function () {
            if(!self.location.location.coords) {
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

        // initialization stuff
        self.locationManager.registerSuccessCallback(self.getNearbySightings);
    };
});

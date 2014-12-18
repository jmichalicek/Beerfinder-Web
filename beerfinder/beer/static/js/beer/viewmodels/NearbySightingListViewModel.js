
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


        this.geoLocationComplete = function (position) {
            self.location = position
            self.sightings([]);
            self.getNearbySightings(position);
        };

        this.getLocationSuccessMessageHandler = function (msg, data) {
            /* data is going to be a location object with coords, etc */
            self.geoLocationComplete(data);
        };

        this.publishGeoLocationError = function (data) {
            if(data.code === Constants.GEOLOCATION_FAIL_DENIED) {
                PubSub.publish(PubSubChannels.GEOLOCATION_DENIED, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_DENIED_MESSAGE]);
            } else if(data.code === Constants.GEOLOCATION_FAIL_UNAVAILABLE) {
                PubSub.publish(PubSubChannels.GEOLOCATION_UNAVAILABLE, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_UNAVAILABLE_MESSAGE]);
            } else if(data.code === Constants.GEOLOCATION_FAIL_TIMEOUT) {
                PubSub.publish(PubSubChannels.GEOLOCATION_TIMEOUT, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_TIMEOUT_MESSAGE]);
            }
            
            PubSub.publish(PubSubChannels.GEOLOCATION_DONE, data);
        };


        this.geoLocationLowAccuracy = function () {
            /* Callback to use for if high accuracy geolocation fails we can try low accuracy instead */
            navigator.geolocation.getCurrentPosition(self.geoLocationCallback, self.publishGeoLocationError,
                                                     {enableHighAccuracy: false, timeout: 5000, maximumAge: 30000});
        };

        this.initialize = function () {
            self.showLoadingSpinner(true);
            navigator.geolocation.getCurrentPosition(self.geoLocationComplete, self.geoLocationLowAccuracy,
                                                     {enableHighAccuracy: true, timeout: 10000, maximumAge: 30000});
        };

        // initialization stuff
        //PubSub.subscribe('GeoLocation.start', self.geoLocationStartedListener);
        PubSub.subscribe(PubSubChannels.GEOLOCATION_SUCCESS, self.getLocationSuccessMessageHandler);
    };
});

define(['jquery', 'knockout', 'moment', 'vendor/infinitescroll', 'sighting/models/SightingModel', 'beer/models/BeerModel'], function($, ko, moment, infinitescroll, SightingModel, BeerModel) {
    return function (data) {
        'use strict';
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.tabManager = data.tabManager;
        this.parentViewModel = data.parentView;
        this.sightings = ko.observableArray();
        this.beer = ko.observable(new BeerModel(data.beer));
        this.formatSightingDate = function (date) {
            
        }

        this.getSightings = function () {
            self.parentViewModel.beer().getRecentSightings().done(function (data) {
                ko.utils.arrayForEach(data.results, function(item) {
                    self.sightings.push(new SightingModel(item));
                });
            });  
        };
    };
});
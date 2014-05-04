define(['jquery', 'knockout', 'vendor/infinitescroll', 'sighting/models/SightingModel'], function($, ko, infinitescroll, SightingModel) {
    return function (data) {
        'use strict';
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.tabManager = data.tabManager;
        this.parentViewModel = data.parentView;
        this.sightings = ko.observableArray();

        this.getSightings = function () {
            self.parentViewModel.beer().getRecentSightings().done(function (data) {
                ko.utils.arrayForEach(data.results, function(item) {
                    self.sightings.push(new SightingModel(item));
                });
            });  
        };
    };
});
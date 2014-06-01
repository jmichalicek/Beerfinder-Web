define(['jquery', 'knockout', 'moment', 'beer/models/BeerModel', 'sighting/models/SightingImageModel'],
       function($, ko, moment, BeerModel, SightingImageModel) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.id = ko.observable(data.id);
        this.beer = ko.observable(new BeerModel(data.beer));
        this.date_sighted = ko.observable(moment(data.date_sighted));
        this.venue = ko.observable(data.venue);
        this.sighted_by = ko.observable(data.sighted_by);
        this.servingTypes = ko.observableArray(data.serving_types || []);
        this.url = ko.observable(data.url);
        this.webUrl = ko.computed(function () {
            return '/sightings/' + self.id() + '/';
        });

        this.distance = ko.observable(data.distance || 0)

        this.images = ko.observableArray([]);
        this.primaryImage = ko.computed(function () {
            return self.images()[0];
        });

        // setup the images
        ko.utils.arrayForEach(data.images, function (image) {
            self.images.push(new SightingImageModel(image));
        });

    };
});
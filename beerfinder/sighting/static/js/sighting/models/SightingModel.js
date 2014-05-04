define(['jquery', 'knockout', 'beer/models/BeerModel'], function($, ko, BeerModel) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.id = ko.observable(data.id);
        this.beer = ko.observable(new BeerModel(data.beer));
        this.date_sighted = ko.observable(data.date_sighted);
        this.venue = ko.observable(data.venue);
        this.sighted_by = ko.observable(data.sighted_by);
        this.image = ko.observable(data.image);
        this.url = ko.observable(data.url);
        this.webUrl = ko.computed(function () {
            return '/sightings/' + self.id() + '/';
        });

        this.distance = ko.observable(data.distance || 0)
    };
});
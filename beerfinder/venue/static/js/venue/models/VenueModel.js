define(['knockout'], function (ko) {

    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};
        
        this.id = ko.observable(data.id);
        this.name = ko.observable(data.name || '');
        this.streetAddress = ko.observable(data.street_address || '');
        this.city = ko.observable(data.city || '');
        this.state = ko.observable(data.state || '');
        this.postalCode = ko.observable(data.postal_code || '');
        this.foursquareId = ko.observable(data.foursquare_id || '');
        this.url = ko.observable(data.url || '');
        this.latitude = ko.observable(data.latitude || '');
        this.longitude = ko.observable(data.longitude || '');
    };
});
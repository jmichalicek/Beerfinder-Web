define(['knockout', 'beer/models/BeerModel'], function(ko, BeerModel) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};
    
        this.beer = ko.observable(new BeerModel(data.beer) || new BeerModel({}));
        this.url = ko.observable(data.url || '');
        this.id = ko.observable(data.id || null);
        this.user = ko.observable(data.user || ''); /* AccountModel ? */
        this.dateAdded = ko.observable(data.date_created || '');
    };
});
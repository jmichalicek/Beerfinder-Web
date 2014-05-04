var WatchedBeerModel = function (data) {
    "use strict";
    var self = this;
    data = typeof data !== 'undefined' ? data : {};
    
    this.beer = ko.observable(data.beer || new BeerModel({}));
    this.url = ko.observable(data.url || '');
    this.id = ko.observable(data.id || null);
    this.user = ko.observable(data.user || '');
    this.dateAdded = ko.observable(data.date_created || '');
};
// TODO: Paginate sighting lists
define(['jquery', 'knockout', 'beer/models/BeerModel'], function($, ko, BeerModel) {
    return function (data) {
        "use strict";
        var self = this;

        this.activeNavSection = ko.observable('beer_list');
        this.beer = ko.observable(new BeerModel(data.beer));
        this.sightings = ko.observableArray();

        // TODO: Maybe add something to api which shows whether beer is in the user's watchlist or not
        // and have remove from watchlist if it is already there and change that after adding
        this.addToWatchlist = function (data) {
            $.ajax({
                url: '/api/watchlist/',
                type: 'POST',
                data: {'beer': self.beer().slug()}
            }).done(function (data) {
                alert("Added to watchlist");
            }).fail(function (data) {
                console.log("error adding beer to watchlist: " + data);
            });
        };
    };
});
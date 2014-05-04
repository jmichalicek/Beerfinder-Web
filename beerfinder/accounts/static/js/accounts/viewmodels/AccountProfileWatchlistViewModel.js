define(['jquery', 'knockout', 'watchlist/models/WatchedBeerModel'], function ($, ko, WatchedBeerModel) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.profileNavController = ko.observable(data.profileNavController);

        this.isActive = ko.computed(function () {
            return self.profileNavController().activeView() == self.profileNavController().ProfileSections.WATCHLIST;
        });

        // TODO: infinite scroll for watchlist
        this.watchlist = ko.observableArray([]);

        this.getWatchlist = function () {
            $.ajax({
                url: '/api/watchlist/',
                type: 'GET'
            }).done(function (data) {
                var currentList = self.watchlist();
                ko.utils.arrayForEach(data.results, function(item) {
                    currentList.push(new WatchedBeerModel(item));
                });
                self.watchlist(currentList);
                // self.nextPage = data.next_page;
            }).fail(function (data) {
                console.log("Ooops" + data);
            });
        };
        
        this.removeFromWatchlist = function (watchedBeer) {
            $.ajax({
                url: watchedBeer.url(),
                type: 'DELETE',
                dataType: 'text',
                cache: false,
            }).done(function (data) {
                self.watchlist.remove(watchedBeer);
            }).fail(function (data) {
                console.log(data);
            });
        }
    };
});
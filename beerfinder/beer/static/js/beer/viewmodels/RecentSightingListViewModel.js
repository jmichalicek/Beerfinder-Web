var RecentSightingListViewModel = function (data) {
    'use strict';
    var self = this;
    data = typeof data !== 'undefined' ? data : {};

    this.tabManager = data.tabManager;
    this.parentViewModel = data.parentView;
    this.sightings = ko.observableArray();

    this.getSightings = function () {
        /*$.ajax({url: '/api/sightings/',
                method: 'GET',
                data: {beer_slug: self.parentViewModel.beer().slug()}
                })*/
        self.parentViewModel.beer().getRecentSightings().done(function (data) {
            ko.utils.arrayForEach(data.results, function(item) {
                self.sightings.push(new SightingModel(item));
            });
        });

    };
};
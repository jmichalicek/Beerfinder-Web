define(['jquery', 'knockout', 'beer/models/BreweryModel', 'beer/models/StyleModel'],
       function($, ko, BreweryModel, StyleModel) {
    return function (data) {
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.BASE_URL = '/api/beer/';

        this.id = ko.observable(data.id);
        this.name = ko.observable(data.name);
        this.brewery = ko.observable(new BreweryModel(ko.toJS(data.brewery)));
        this.slug = ko.observable(data.slug);
        this.style = ko.observable(data.style ? new StyleModel(ko.toJS(data.style)) : undefined);
        this.watcherCount = ko.observable(data.watcher_count);

        this.viewUrl = ko.computed(function () {
            return '/beer/'.concat(self.slug(), '/');
        });

        this.detailUrl = ko.computed(function () {
            return self.BASE_URL.concat(self.slug(), '/');
        });

        this.addSightingUrl = ko.computed(function () {
            return '/sightings/add_sighting/?beer=' + self.slug();
        });

        this.getRecentSightings = function () {
            return $.ajax({url: '/api/sightings/',
                           method: 'GET',
                           data: {beer: self.slug()}
                          });
        };

        this.getNearbySightings = function (latitude, longitude) {
            var requestParams = {latitude:latitude, longitude: longitude, beer: self.slug()};
            return $.ajax({url: '/api/nearby_sightings/',
                           method: 'GET',
                           data: requestParams,
                          });
        };

        this.recentSightingsWebURL = ko.computed(function () {
            return '/sightings/?beer=' + self.slug();
        });

        this.nearbySightingsWebURL = ko.computed(function () {
            return '/sightings/nearby/?beer=' + self.slug();
        });

        /*
         * save an existing beer.  Currently this will probably blow up if the beer does not already exist
         */
        this.save = function() {
            var url = self.BASE_URL;
            if(self.slug() && self.id()) {
                var url = self.detailUrl();
            }

            var id = self.id();
            var name = self.name();
            var slug = self.slug();
            var brewery_name = self.brewery().name();
            var brewery_id = self.brewery().id();
            var style_id = self.style().id();
            return $.ajax({url: url,
                           method: 'PUT',
                           data: {id: id, name: name, slug: slug, brewery: brewery_id, style: style_id}
                          });
        };

        /*
         * Create this beer on the server
         */
        this.create = function () {
            var url = self.BASE_URL;
            var postData = {beer: self.name(), brewery: self.brewery().name()};
            if(self.style() && self.style().id()) {
                postData.style = self.style().id();
            }
            return $.ajax({url: url,
                           method: 'POST',
                           data: postData
                          });
        };
    };
});

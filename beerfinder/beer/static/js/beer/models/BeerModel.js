define(['jquery', 'knockout', 'beer/models/BreweryModel'], function($, ko, BreweryModel) {
    return function (data) {
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.BASE_URL = '/api/beer/';

        this.id = ko.observable(data.id);
        this.name = ko.observable(data.name);
        this.brewery = ko.observable(new BreweryModel(data.brewery));
        this.slug = ko.observable(data.slug);
        
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
            return $.ajax({url: '/api/sightings/nearby/',
                           method: 'GET',
                           data: requestParams,
                          });
        };

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
            return $.ajax({url: url,
                           method: 'PUT',
                           data: {id: self.id(), name: self.name(), slug: self.slug(), brewery: self.brewery().id()}
                          });
        };

        /*
         * Create this beer on the server
         */
        this.create = function () {
            var url = self.BASE_URL;
            return $.ajax({url: url,
                           method: 'POST',
                           data: {beer: self.name(), brewery: self.brewery().name()}
                          });
        };
    };
});

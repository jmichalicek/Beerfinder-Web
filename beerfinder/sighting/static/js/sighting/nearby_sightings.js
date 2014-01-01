// TODO: move severa of these models out because they will be used elsewhere

var VenueModel = function (data) {
    this.id = data.id;
    this.name = ko.observable(data.name);
};

var BreweryModel = function (data) {
    this.id = data.id;
    this.name = ko.observable(data.name);
}

var BeerModel = function (data) {
    this.id = data.id;
    this.name = ko.observable(data.name);
    this.brewery = ko.observable(data.brewer);
};

var SightingModel = function (data) {
    this.id = ko.observable(data.id);
    this.beer = ko.observable(data.beer);
    this.date_sighted = ko.observable(data.date_sighted);
    this.venue = ko.observable(data.venue);
    this.sighted_by = ko.observable(data.sighted_by);
};

var ViewModel = function () {
    var self = this;

    this.location = {}; // TODO: populate this.

    this.sightings = ko.observableArray();

    this.getSightings = function() {
        // TODO: pagination
        $.ajax({url: '/api/sightings/', // TODO: make this nearby sightings
                method: 'GET',
               }).done(function (data) {
                   ko.utils.arrayForEach(data, function(item) {
                       self.sightings.push(new SightingModel(item));
                   });
               });
    };

    this.initialize = function () {
        self.getSightings();
    };
};
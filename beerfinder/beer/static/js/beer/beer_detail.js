var ViewModel = function (data) {
    var self = this;

    this.beer = ko.observable(new BeerModel(data.beer));
    this.sightings = ko.observableArray();

    this.getSightings = function () {
        $.ajax({url: '/api/sightings/',
                method: 'GET',
                data: {beer_slug: self.beer().slug()}
               }).done(function (data) {
                   ko.utils.arrayForEach(data, function(item) {
                       self.sightings.push(new SightingModel(item));
                   });
               });
    };
};

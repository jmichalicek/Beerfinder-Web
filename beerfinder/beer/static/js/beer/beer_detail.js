var ViewModel = function (data) {
    var self = this;
    this.activeNavSection = ko.observable('beer_list');
    this.beer = ko.observable(new BeerModel(data.beer));
    this.sightings = ko.observableArray();

    this.getSightings = function () {
        $.ajax({url: '/api/sightings/',
                method: 'GET',
                data: {beer_slug: self.beer().slug()}
               }).done(function (data) {
                   ko.utils.arrayForEach(data.results, function(item) {
                       self.sightings.push(new SightingModel(item));
                   });
               });
    };
};

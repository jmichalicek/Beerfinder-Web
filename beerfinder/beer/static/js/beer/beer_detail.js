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

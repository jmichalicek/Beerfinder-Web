var ViewModel = function () {
    var self = this;

    this.beers = ko.observableArray();

    this.getBeerList = function() {
        // TODO: pagination
        $.ajax({url: '/api/beer/',
                method: 'GET',
                data: {},
               }).done(function (data) {
                   ko.utils.arrayForEach(data, function(item) {
                       self.beers.push(new BeerModel(item));
                   });
               });
    };

    this.initialize = function () {
        self.getBeerList();
    };
};

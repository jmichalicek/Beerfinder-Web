var ViewModel = function (data) {
    var self = this;

    this.beer = ko.observable(new BeerModel(data.beer));

};

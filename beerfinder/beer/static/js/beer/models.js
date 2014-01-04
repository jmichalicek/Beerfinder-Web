var BreweryModel = function (data) {
    this.id = data.id;
    this.name = ko.observable(data.name);
}

var BeerModel = function (data) {
    this.id = data.id;
    this.name = ko.observable(data.name);
    this.brewery = ko.observable(data.brewery);
};

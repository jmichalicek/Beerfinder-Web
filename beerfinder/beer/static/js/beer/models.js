var BreweryModel = function (data) {
    this.id = data.id;
    this.name = ko.observable(data.name);
}

var BeerModel = function (data) {
    var self = this;
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.brewery = ko.observable(data.brewery);
    this.slug = ko.observable(data.slug);

    this.detailUrl = ko.computed(function () {
        return '/beer/' + self.slug() + '/';
    });

    this.addSightingUrl = ko.computed(function () {
        return '/add_sighting/?beer=' + self.slug();
    });
};

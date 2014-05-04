var BreweryModel = function (data) {
    var self = this;
    data = typeof data !== 'undefined' ? data : {};

    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}
var SightingModel = function (data) {
    this.id = ko.observable(data.id);
    this.beer = ko.observable(data.beer);
    this.date_sighted = ko.observable(data.date_sighted);
    this.venue = ko.observable(data.venue);
    this.sighted_by = ko.observable(data.sighted_by);
};

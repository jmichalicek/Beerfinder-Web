var ViewModel = function (data) {
    var self = this;
    this.sighting = ko.observable(new SightingModel(data.sighting));
};
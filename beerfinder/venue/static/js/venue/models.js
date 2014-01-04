var VenueModel = function (data) {
    this.id = data.id;
    this.name = ko.observable(data.name);
};

var FoursquareVenueModel = function (data) {
    "use strict";
    var self = this;
    data = typeof data !== 'undefined' ? data : {};

    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.location = ko.observable(data.location);
};

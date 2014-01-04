// Be sure to load js/sightings/models.js first

var ViewModel = function () {
    var self = this;

    this.location = {}; // TODO: populate this.

    this.sightings = ko.observableArray();

    this.getSightings = function() {
        // TODO: pagination
        $.ajax({url: '/api/sightings/nearby/',
                method: 'GET',
                data: {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude},
               }).done(function (data) {
                   ko.utils.arrayForEach(data, function(item) {
                       self.sightings.push(new SightingModel(item));
                   });
               });
    };

    this.initialize = function () {
        navigator.geolocation.getCurrentPosition(self.getNearbySightings);
    };

    this.getNearbySightings = function (position) {
        // to be used as a callback for html5 geolocation
        self.location = position;
        self.getSightings();
    }
};
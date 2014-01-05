// Be sure to load js/sightings/models.js first

var ViewModel = function () {
    var self = this;

    this.location = {}; // TODO: populate this.

    this.sightings = ko.observableArray();
    this.activeNavSection = ko.observable('sightings_list');

    this.getSightings = function() {
        // TODO: pagination
        $.ajax({url: '/api/sightings/',
                method: 'GET',
               }).done(function (data) {
                   ko.utils.arrayForEach(data, function(item) {
                       self.sightings.push(new SightingModel(item));
                   });
               });
    };
};
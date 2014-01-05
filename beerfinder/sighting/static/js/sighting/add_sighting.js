// Be sure to load js/sightings/models.js first
// look at https://github.com/thinkloop/knockout-js-infinite-scroll/blob/master/infinitescroll.js
// for infinite scrolling the locations

var ViewModel = function (data) {
    var self = this;

    this.selectedVenue = ko.observable(null);
    this.location = {}; // TODO: populate this.
    this.venues = ko.observableArray();
    this.comment = ko.observable("");
    this.beer = ko.observable(data.beer);
    this.image = ko.observable(null);

    this.sightingReady = ko.computed(function () {
        return self.selectedVenue() && self.beer(); // probably will add more checks/conditions here
    });

    this.submitSighting = function () {
        var formData = new FormData();
        formData.append('foursquare_venue_id', self.selectedVenue().id());
        formData.append('comment', self.comment());
        formData.append('beer', self.beer().slug);
        if(self.image()) {
            formData.append('sighting_image', self.image());
        }

        $.ajax({url: '/api/sightings/',
                method: 'POST',
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
               }).done(function (data) {
                   window.location = '/sightings/' + data['id'] + '/';
               }).error(function (data) {
                   // todo: real error handling for varying errors.  Trying again may be pointless.
                   // also, display this in a better manner
                   alert('There was an error addinging your sighting. Please try again.');
               });
    };

    this.setSelectedVenue = function (venue) {
        self.selectedVenue(venue);
    };

    this.clearSelectedVenue = function () {
        self.selectedVenue(null);
    };

    this.getLocation = function () {
        navigator.geolocation.getCurrentPosition(self.getNearbyVenues);
    };

    this.getNearbyVenues = function (position) {
        // to be used as a callback for html5 geolocation
        self.location = position;
        requestParams = {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude};

//        var searchName = searchName || null;
//        if(searchName != null) {
//            requestParams[name] = searchName;
//        }

        $.ajax({url: '/api/foursquare_venues/',
                method: 'GET',
                data: requestParams,
               }).done(function (data) {
                   ko.utils.arrayForEach(data['groups'], function(group) {
                       // this is an ugly mess of stuff
                       ko.utils.arrayForEach(group['items'], function(item) {
                           var v = item['venue'];
                           self.venues.push(new FoursquareVenueModel(v));
                       });
                   });
               });
    };

    this.searchVenues = function (name) {
        //self
    };
};
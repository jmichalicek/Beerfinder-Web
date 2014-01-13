// Be sure to load js/sightings/models.js first
// look at https://github.com/thinkloop/knockout-js-infinite-scroll/blob/master/infinitescroll.js
// for infinite scrolling the locations

var ViewModel = function (data) {
    var self = this;

    this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling
    this.venuesPerRequest = 50;
    this.maxResults = null;

    this.searchTerm = ko.observable('');

    this.activeNavSection = ko.observable('');
    this.selectedVenue = ko.observable(null);
    this.location = {}; // TODO: populate this.

    this.venue_list = ko.observableArray();
    this.venues = ko.observableArray();
    this.searchVenues = ko.observableArray(); // for venues returned via search

    this.comment = ko.observable("");
    this.beer = ko.observable(data.beer);
    this.image = ko.observable(null);

    this.discoverView = ko.observable(true); // determine whether to show discover or search lists
    this.searchListVisible = ko.computed(function () {
        return !self.selectedVenue() && !self.discoverView();
    });
    this.venueListVisible = ko.computed(function () {
        return !self.selectedVenue() && self.discoverView();
    });

    // stuff to enable infinite scroll
    this.venues.extend({
        infinitescroll: {}
    });

    // detect resize
    $(window).resize(function() {
        updateViewportDimensions();
    });

    // detect scroll
    $(venue_list).scroll(function() {
        // we need to pause watching this while an ajax request is being made
        // or we make a bunch of requests for the same data and make a mess of things
        self.venues.infinitescroll.scrollY($(venue_list).scrollTop());
        
        // add more items if scroll reaches the last 15 items
        if (self.venues.peek().length - self.venues.infinitescroll.lastVisibleIndex.peek() <= 50) {
            self.getNearbyVenues();
        }
    });

    // update dimensions of infinite-scroll viewport and item
    function updateViewportDimensions() {
        var itemsRef = $('#venue_list'),
        itemRef = $('.venue_item').first(),
        itemsWidth = itemsRef.width(),
        itemsHeight = itemsRef.height(),
        itemWidth = itemRef.outerWidth(),
        itemHeight = itemRef.outerHeight();

        self.venues.infinitescroll.viewportWidth(itemsWidth);
        self.venues.infinitescroll.viewportHeight(itemsHeight);
        self.venues.infinitescroll.itemWidth(itemWidth);
        self.venues.infinitescroll.itemHeight(itemHeight);

    }
    updateViewportDimensions();

    // end infinite scroll stuff

    this.sightingReady = ko.computed(function () {
        return self.selectedVenue() && self.beer(); // probably will add more checks/conditions here
    });

    this.submitSighting = function () {
        var i = $('#sighting_image');
        var im = document.getElementById('sighting_image');
        var formData = new FormData();
        formData.append('foursquare_venue_id', self.selectedVenue().id());
        formData.append('comment', self.comment());
        formData.append('beer', self.beer().slug);
        formData.append('image', $('#sighting_image')[0].files[0]);

        $.ajax({url: '/api/sightings/',
                type: 'POST',
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
        navigator.geolocation.getCurrentPosition(self.geoLocationCallback);
    };

    this.geoLocationCallback = function (position) {
        self.location = position;
        self.getNearbyVenues();
    };

    this.getNearbyVenues = function () { 
        var offset = self.venues.peek().length;
        if(!self.requestInProgress && (self.maxResults == null || offset < self.maxResults)) {
            self.requestInProgress = true;

           
            requestParams = {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude,
                             offset: offset};
            
            $.ajax({url: '/api/foursquare_venues/',
                    type: 'GET',
                    data: requestParams,
                   }).done(function (data) {
                       var existingItems = self.venues();
                       self.maxResults = data['totalResults'];
                       ko.utils.arrayForEach(data['groups'], function(group) {
                           // this is an ugly mess of stuff
                       ko.utils.arrayForEach(group['items'], function(item) {
                           var v = item['venue'];
                           existingItems.push(new FoursquareVenueModel(v));
                       });
                       });
                       self.venues(existingItems);
                   }).complete(function () {
                       self.requestInProgress = false;
                   });
        }
    };

    this.submitSearchHandler = function () {
        if(self.searchTerm().length < 1) {
            // just do regular explore if the search term was empty
            self.discoverView(true);
            self.getNearbyVenues();
        } else {
            self.discoverView(false);
            self.searchForVenue();
        }
    };

    this.searchForVenue = function () {
        requestParams = {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude,
                         query: self.searchTerm()};

        $.ajax({url: '/api/foursquare_venues/search/',
                type: 'GET',
                data: requestParams,
               }).done(function (data) {
                   var resultItems = [];
                   ko.utils.arrayForEach(data['venues'], function(venue) {
                       resultItems.push(new FoursquareVenueModel(venue));
                   });
                   self.searchVenues(resultItems);
               });
    };
};
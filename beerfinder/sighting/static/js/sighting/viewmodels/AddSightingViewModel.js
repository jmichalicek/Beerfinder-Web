// look at https://github.com/thinkloop/knockout-js-infinite-scroll/blob/master/infinitescroll.js
// for infinite scrolling the locations
define(['jquery', 'knockout', 'vendor/infinitescroll', 'venue/models/VenueModel', 'venue/models/FoursquareVenueModel',
        'beer/models/ServingTypeModel', 'beer/models/BeerModel', 'sighting/models/SightingModel'], function ($, ko, infinitescroll, VenueModel, FoursquareVenueModel, ServingTypeModel, BeerModel, SightingModel) {

    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};
        
        this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling
        this.venuesPerRequest = 50;
        this.maxResults = null;
        
        this.searchTerm = ko.observable('');
        
        this.activeNavSection = ko.observable('');
        this.selectedVenue = ko.observable(null);
        this.location = {}; // TODO: populate this.
        this.selectedServingTypes = ko.observableArray([]);
        
        this.venues = ko.observableArray();
        this.searchVenues = ko.observableArray(); // for venues returned via search
        
        this.comment = ko.observable("");
        this.beer = ko.observable(new BeerModel(data.beer));
        this.image = ko.observable(null);

        this.servingTypes = ko.observableArray([]);
        this.submitInProgress = ko.observable(false);
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
        $('#venue_list').scroll(function() {
            // we need to pause watching this while an ajax request is being made
            // or we make a bunch of requests for the same data and make a mess of things
            self.venues.infinitescroll.scrollY($('#venue_list').scrollTop());
            
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
            return self.selectedVenue() && self.beer() && !self.submitInProgress(); // probably will add more checks/conditions here
        });
        
        this.showSpinner = ko.observable(false);
        this.submitSighting = function () {
          
            self.showSpinner(true);
            self.submitInProgress(true);
            var i = $('#sighting_image');
            var im = document.getElementById('sighting_image');
            var formData = new FormData();
            // find a way to do this without using formdata?
            // currently using formdata due to the image upload
            formData.append('foursquare_venue_id', self.selectedVenue().id());
            formData.append('comment', self.comment());
            formData.append('beer', self.beer().slug());
            formData.append('image', $('#sighting_image')[0].files[0]);

            // cannot just append an array with FormData objects
            ko.utils.arrayForEach(self.selectedServingTypes(), function (item) {
                formData.append('serving_types', item);
            });
            
            $.ajax({url: '/api/sightings/',
                    type: 'POST',
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                   }).done(function (data) {
                       var sighting = new SightingModel(data);
                       window.location = sighting.webUrl();
                   }).error(function (data) {
                       // todo: real error handling for varying errors.  Trying again may be pointless.
                       // also, display this in a better manner
                       alert('There was an error addinging your sighting. Please try again.');
                   }).complete(function (data) {
                       self.showSpinner(false);
                       self.submitInProgress(false);
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
                
                
                var requestParams = {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude,
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
            var requestParams = {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude,
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

        /* Populate servingtTypes array so that the form can be populated */
        this.getServingTypes = function () {
            $.ajax({
                url: '/api/serving_types/',
                type: 'GET',
            }).done(function (data) {
                var resultItems = [];
                ko.utils.arrayForEach(data['results'], function(item) {
                    resultItems.push(new ServingTypeModel(item));
                });
                self.servingTypes(resultItems);
            });
        };
    };
});
// look at https://github.com/thinkloop/knockout-js-infinite-scroll/blob/master/infinitescroll.js
// for infinite scrolling the locations
define(['jquery', 'underscore', 'knockout', 'vendor/infinitescroll', 'pubsub', 'core/Constants', 'core/PubSubChannels', 'venue/models/VenueModel', 'venue/models/FoursquareVenueModel',
        'beer/models/ServingTypeModel', 'beer/models/BeerModel', 'sighting/models/SightingModel'], function ($, _, ko, infinitescroll, PubSub, Constants, PubSubChannels, VenueModel, FoursquareVenueModel, ServingTypeModel, BeerModel, SightingModel) {

    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.showLoadingSpinner = ko.observable(false);
        this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling
        this.venuesPerRequest = 50;
        this.maxResults = null;

        this.searchTerm = ko.observable('');

        this.activeNavSection = ko.observable('');
        this.selectedVenue = ko.observable(null);
        this.location = data.location || {};
        this.selectedServingTypes = ko.observableArray([]);

        this.venues = ko.observableArray();
        this.searchVenues = ko.observableArray(); // for venues returned via search

        this.comment = ko.observable("");
        this.beer = ko.observable(new BeerModel(data.beer));
        this.image = ko.observable(null);

        this.servingTypes = ko.observableArray([]);
        this.submitInProgress = ko.observable(false);
        this.discoverView = ko.observable(true); // determine whether to show discover or search lists
        this.venueSelected = ko.observable(false);  // probably unnecessary now that selectedVenue usage is fixed
        this.imageUploadError = ko.observable(false);

        this.sighting = ko.observable(null); // assigned after successfully submitting a sighting

        this.searchListVisible = ko.computed(function () {
            return !self.venueSelected() && !self.discoverView();
        });
        this.venueListVisible = ko.computed(function () {
            return !self.venueSelected() && self.discoverView();
        });


        this.showImageThumbnail = function (data, e) {
            // make this a knockout binding?
            var x = data;
            var element = e.currentTarget;
            var files = !!element.files ? element.files : [];

            if(!files.length || !window.FileReader) {
                return;
            }

            if(/^image/.test(files[0].type)) {
                var reader = new FileReader();
                reader.readAsDataURL(files[0]);
                reader.onloadend = function() { // set image data as background of div
                    self.image(this.result);
                }
            }
        };

        this.clearImage = function (data, e) {
            var target = $(e.currentTarget).data('target');
            var fileField = $('#' + target);
            //fileField.replaceWith(fileField.val('').clone(true, true));
            fileField.val('');
            fileField.files = [];
            self.image(undefined);
        };

        // stuff to enable infinite scroll
        this.venues.extend({
            infinitescroll: {}
        });

        // detect resize
        $(window).resize(function() {
            debouncedUpdateViewport();
        });

        this.handleScroll = _.debounce(function () {
            self.venues.infinitescroll.scrollY($(window).scrollTop());
            // add more items if scroll reaches the last 15 items
            if (self.venues.peek().length - self.venues.infinitescroll.lastVisibleIndex.peek() <= 20) {
                self.debouncedNearbyVenues();
            }

            updateViewportDimensions();
        }, 250);
        $(document).scroll(self.handleScroll);


        // update dimensions of infinite-scroll viewport and item
        function updateViewportDimensions() {
            var itemsRef = $(window),//$('#venue_list'),
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
        var debouncedUpdateViewport = _.debounce(updateViewportDimensions, 250);

        // end infinite scroll stuff

        this.sightingReady = ko.computed(function () {
            return self.selectedVenue() && self.beer() && !self.submitInProgress(); // probably will add more checks/conditions here
        });

        this.showSpinner = ko.observable(false);

        this.postSighting = function () {
            // Could make these 2 separate forms now and really simplify things

            var formData = new FormData();
            // find a way to do this without using formdata?
            // currently using formdata due to the image upload
            formData.append('venue_foursquare_id', self.selectedVenue().id());
            formData.append('comment', self.comment());
            formData.append('beer_slug', self.beer().slug());
            // cannot just append an array with FormData objects
            ko.utils.arrayForEach(self.selectedServingTypes(), function (item) {
                formData.append('serving_type_ids', item);
            });

            return $.ajax({url: '/api/sightings/',
                           type: 'POST',
                           data: formData,
                           cache: false,
                           contentType: false,
                           processData: false,
                          });
        };

        this.postImage = function () {
            self.showLoadingSpinner(true);
            self.imageUploadError(false);
            var i = $('#sighting_image');
            var im = document.getElementById('sighting_image');
            var formData = new FormData();
            // should just be able to use im here...
            // rename this field to 'image' on the serializer?
            formData.append('original', $('#sighting_image')[0].files[0]);
            formData.append('sighting', self.sighting().id());

            return $.ajax({url: '/api/sighting_images/',
                           type: 'POST',
                           data: formData,
                           cache: false,
                           contentType: false,
                           processData: false,
                          }).done(function (data) {
                              window.location = self.sighting().webUrl();
                          }).error(function (data) {
                              self.showLoadingSpinner(false);
                              self.submitInProgress(false);
                              self.imageUploadError(true);
                          });;
        };

        this.submitSighting = function () {
            // TODO: Save created sighting on viewmodel, then if image upload fails
            // display html with button to retry uploading the image
            self.showLoadingSpinner(true);
            self.submitInProgress(true);
            self.postSighting().done(function (data) {
                self.sighting(new SightingModel(data));
                if(!$('#sighting_image')[0].files[0]) {
                    window.location = self.sighting().webUrl();
                } else {
                    // postImage will handle redirect or showing image error
                    self.postImage();
                }
            }).error(function (data) {
                self.showLoadingSpinner(false);
                self.submitInProgress(false);
                // TODO: show real error in the page, not a js alert
                alert('There was an error addinging your sighting. Please try again.');
            });
        };

        this.setSelectedVenue = function (venue) {
            self.selectedVenue(venue);
            self.venueSelected(true);
        };

        this.clearSelectedVenue = function () {
            self.venueSelected(false);
            self.selectedVenue(null);
            // force data into displayItems() and then updateViewportDimensions()
            // to work around weird bug where displayItems() is not being repopulated
            // when the view becomes visible again.
            self.venues.infinitescroll.displayItems(self.venues().slice(0,50));
            updateViewportDimensions();
        };

        this.geoLocationCallback = function (position) {
            self.location = position;
            PubSub.publish(PubSubChannels.GEOLOCATION_SUCCESS, position);
            PubSub.publish(PubSubChannels.GEOLOCATION_DONE, position);
            // will be handled by the pubsub handler
            //self.getNearbyVenues();
        };

        this.publishGeoLocationError = function (data) {
            if(data.code === Constants.GEOLOCATION_FAIL_DENIED) {
                PubSub.publish(PubSubChannels.GEOLOCATION_DENIED, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_DENIED_MESSAGE]);
            } else if(data.code === Constants.GEOLOCATION_FAIL_UNAVAILABLE) {
                PubSub.publish(PubSubChannels.GEOLOCATION_UNAVAILABLE, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_UNAVAILABLE_MESSAGE]);
            } else if(data.code === Constants.GEOLOCATION_FAIL_TIMEOUT) {
                PubSub.publish(PubSubChannels.GEOLOCATION_TIMEOUT, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_TIMEOUT_MESSAGE]);
            }

            PubSub.publish(PubSubChannels.GEOLOCATION_DONE, data);
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
                       }).always(function () {
                           self.requestInProgress = false;
                           self.showLoadingSpinner(false);
                           updateViewportDimensions();
                       });
            }
        };

        this.debouncedNearbyVenues = _.debounce(self.getNearbyVenues, 250);

        this.submitSearchHandler = function () {
            // maybe this should be renamed now.  It is used when not searching as well.
            if(self.searchTerm().length < 1) {
                // just do regular explore if the search term was empty
                self.returnToDiscoverView();
            } else {
                self.discoverView(false);
                self.searchForVenue();
            }
        };

        this.returnToDiscoverView = function () {
            /**
             * Handler for when Return To List is clicked to end search
             */
            self.searchTerm('');
            self.discoverView(true);
            self.searchVenues([]);
            // this needs reset directly because hiding the div with the ul
            // for this list when going to search mode confuses it.
            self.venues.infinitescroll.displayItems(self.venues());
            updateViewportDimensions();
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
                       updateViewportDimensions();
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

        this.geoLocationSuccessMessageHandler = function (msg, data) {
            /* data is going to be a location object with coords, etc */
            self.selectedVenue(null);
            self.venues([]);
            self.location = data;
            self.getNearbyVenues();
        };

        this.publishGeoLocationError = function (data) {
            if(data.code === Constants.GEOLOCATION_FAIL_DENIED) {
                PubSub.publish(PubSubChannels.GEOLOCATION_DENIED, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_DENIED_MESSAGE]);
            } else if(data.code === Constants.GEOLOCATION_FAIL_UNAVAILABLE) {
                PubSub.publish(PubSubChannels.GEOLOCATION_UNAVAILABLE, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_UNAVAILABLE_MESSAGE]);
            } else if(data.code === Constants.GEOLOCATION_FAIL_TIMEOUT) {
                PubSub.publish(PubSubChannels.GEOLOCATION_TIMEOUT, data);
                PubSub.publish(PubSubChannels.ERRORS_SET, [Constants.GEOLOCATION_TIMEOUT_MESSAGE]);
            }

            PubSub.publish(PubSubChannels.GEOLOCATION_DONE, data);
        };

        this.geoLocationLowAccuracy = function () {
            /* Callback to use for if high accuracy geolocation fails we can try low accuracy instead */
            navigator.geolocation.getCurrentPosition(self.geoLocationCallback, self.publishGeoLocationError,
                                                     {enableHighAccuracy: false, timeout: 5000, maximumAge: 30000});
        };

        this.initialize = function () {
            PubSub.publish(PubSubChannels.GEOLOCATION_START, {});
            self.showLoadingSpinner(true);
            PubSub.subscribe(PubSubChannels.GEOLOCATION_SUCCESS, self.geoLocationSuccessMessageHandler);


            PubSub.publish(PubSubChannels.GEOLOCATION_START, {});
            navigator.geolocation.getCurrentPosition(self.geoLocationCallback, self.geoLocationLowAccuracy, {enableHighAccuracy: true, timeout: 10000, maximumAge: 30000});
        };
    };
});

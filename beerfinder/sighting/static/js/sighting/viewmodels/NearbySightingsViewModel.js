define(['jquery', 'knockout', 'underscore', 'vendor/infinitescroll', 'pubsub', 'core/Constants', 'core/PubSubChannels', 'core/QueryStringParser', 'sighting/models/SightingModel'], function ($, ko, _, infinitescroll,  PubSub, Constants, PubSubChannels, QueryStringParser, SightingModel) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        self.showLoadingSpinner = ko.observable(false);
        this.location = data.location || {};
        this.activeNavSection = ko.observable('nearby_sightings');
        this.sightings = ko.observableArray();

        //new
        this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling

        this.sightings = ko.observableArray();
        this.queryString = new QueryStringParser(window.location.href);

        // stuff to enable infinite scroll
        this.nextPage = '';
        this.previousPage = '';
        this.sightings.extend({
            infinitescroll: {}
        });

        // detect scroll
        this.shouldDoRequestPage = function () {
            /* Determine if we shoud request another infinite scroll page */
            return self.sightings.peek().length - self.sightings.infinitescroll.lastVisibleIndex.peek() <= 25;
        };

        // detect scroll
        this.handleScroll = _.debounce(function () {
            self.sightings.infinitescroll.scrollY($('body').scrollTop());

            if (self.shouldDoRequestPage()) {
                if(!self.requestInProgress && self.nextPage) {
                    _.debounce(self.getSightings(), 250);
                }
            }

            updateViewportDimensions();

        }, 250);
        $(document).scroll(function() {
            self.handleScroll();
        });

        // update dimensions of infinite-scroll viewport and item
        function updateViewportDimensions() {
            //var itemsRef = $('#sighting_list'),
            var itemsRef = $('#page_body'),
            itemRef = $('#sighting_list .sighting_item').first(),
            itemsWidth = itemsRef.width(),
            itemsHeight = itemsRef.height(),
            itemWidth = itemRef.outerWidth(true),
            itemHeight = itemRef.outerHeight(true);

            self.sightings.infinitescroll.viewportWidth(itemsWidth);
            self.sightings.infinitescroll.viewportHeight(itemsHeight);
            // normally infinitescroll.itemWidth would use itemWidth from above,
            // but jQuery is being weird and picking it up as the wrong width.
            // Since this definitely should be only 1 column, just use the container width
            // as a kludge until I can figure out wtf is going wrong.
            self.sightings.infinitescroll.itemWidth(itemWidth);
            self.sightings.infinitescroll.itemHeight(itemHeight);
        }
        updateViewportDimensions();


        // end infinite scroll stuff


        //end new

        this.getSightings = function() {
            // TODO: pagination
            var url = '/api/nearby_sightings/';

            var dfd = new $.Deferred();
            self.showLoadingSpinner(true);
            self.requestInProgress = true;

            var requestParams = {};

            if(self.nextPage) {
                // drf 3.1 change
                //requestParams['page'] = self.nextPage;
                url = self.nextPage;
            } else {
                // with drf 3.1, our next url already has this
                requestParams = {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude};
            }

            if (self.queryString.params['beer']) {
                requestParams['beer'] = self.queryString.params['beer'][0];
            }

            self.requestInProgress = true;
            $.ajax({url: url,
                    type: 'GET',
                    data: requestParams,
                   }).done(function (data) {
                       var currentList = self.sightings();
                       ko.utils.arrayForEach(data.results, function(item) {
                           currentList.push(new SightingModel(item));
                       });
                       self.sightings(currentList);
                       self.nextPage = data.next;
                       dfd.resolve(data);
                   }).fail(function (data) {
                       console.log(data);
                       dfd.resolve(false);
                   }).always(function () {
                       self.requestInProgress = false;
                       self.showLoadingSpinner(false);
                       updateViewportDimensions();
                   });
            return dfd.promise();
        };

        this.publishGeoLocationSuccess = function (position) {
            PubSub.publish(PubSubChannels.GEOLOCATION_SUCCESS, position);
            PubSub.publish(PubSubChannels.GEOLOCATION_DONE, position);
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
            self.showLoadingSpinner(true);
            PubSub.publish(PubSubChannels.GEOLOCATION_START, {});
            navigator.geolocation.getCurrentPosition(self.publishGeoLocationSuccess, self.geoLocationLowAccuracy,  {enableHighAccuracy: true, timeout: 10000, maximumAge: 30000});
        };

        this.doLocationUpdated = function (position) {
            self.location = position;
            self.sightings([]);
            self.getSightings();
        };

        this.getLocationSuccessMessageHandler = function (msg, data) {
            /* data is going to be a location object with coords, etc */
            self.doLocationUpdated(data);
        };

        // initialization stuff
        PubSub.subscribe(PubSubChannels.GEOLOCATION_SUCCESS, self.getLocationSuccessMessageHandler);

    };
});

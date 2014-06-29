define(['jquery', 'knockout', 'underscore', 'vendor/infinitescroll', 'sighting/models/SightingModel'], function ($, ko, _, infinitescroll, SightingModel) {
    return function () {
        "use strict";
        var self = this;

        self.showLoadingSpinner = ko.observable(false);
        this.location = {}; // TODO: populate this.
        this.activeNavSection = ko.observable('nearby_sightings');
        this.sightings = ko.observableArray();
    
        //new
        this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling
        
        this.sightings = ko.observableArray();
    
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
        $('#sighting_list').scroll(function() {
            // we need to pause watching this while an ajax request is being made
            // or we make a bunch of requests for the same data and make a mess of things
            self.sightings.infinitescroll.scrollY($('#sighting_list').scrollTop());
            
            if (self.shouldDoRequestPage()) {
                if(!self.requestInProgress && self.nextPage) {
                    _.debounce(self.getSightings(), 250);
                }
            }
        });
        
        // update dimensions of infinite-scroll viewport and item
        function updateViewportDimensions() {
            var itemsRef = $('#sighting_list'),
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
            self.sightings.infinitescroll.itemWidth(itemsWidth);
            self.sightings.infinitescroll.itemHeight(itemHeight);
        }
        updateViewportDimensions();
        

        // end infinite scroll stuff


        //end new

        this.getSightings = function() {
            // TODO: pagination
            var url = '/api/sightings/nearby/';
            var requestParams = {};
            if(self.nextPage) {
                url = self.nextPage;
            } else {
                requestParams = {latitude: self.location.coords.latitude, longitude: self.location.coords.longitude};
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
                   }).always(function () {
                       self.requestInProgress = false;
                       self.showLoadingSpinner(false);
                   });  
        };

        this.initialize = function () {
            self.showLoadingSpinner(true);
            navigator.geolocation.getCurrentPosition(self.getNearbySightings);
        };

        this.getNearbySightings = function (position) {
            // to be used as a callback for html5 geolocation
            self.location = position;
            self.getSightings();
        };
    };
});
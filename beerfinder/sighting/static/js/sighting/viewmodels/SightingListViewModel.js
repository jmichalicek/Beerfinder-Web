// Be sure to load js/sightings/models.js first
define(['jquery', 'underscore', 'knockout', 'vendor/infinitescroll', 'sighting/models/SightingModel'], function($, _, ko, infinitescroll, SightingModel) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.showLoadingSpinner = ko.observable(false);
        this.location = {}; // TODO: populate this.

        this.sightings = ko.observableArray();
        this.activeNavSection = ko.observable('sightings_list');
        this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling

        this.sightings = ko.observableArray();
    
        // stuff to enable infinite scroll
        this.nextPage = '';
        this.previousPage = '';
        this.sightings.extend({
            infinitescroll: {}
        });

        // detect scroll
        $('#sighting_list').scroll(function() {
            // we need to pause watching this while an ajax request is being made
            // or we make a bunch of requests for the same data and make a mess of things
            self.sightings.infinitescroll.scrollY($('#sighting_list').scrollTop());

            if (self.sightings.peek().length - self.sightings.infinitescroll.lastVisibleIndex.peek() <= 25) {
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

        this.getSightings = function() {
            self.showLoadingSpinner(true);
            self.requestInProgress = true;
            var url = '/api/sightings/';

            if(self.nextPage) {
                url = self.nextPage;
            }

            $.ajax({url: url,
                    type: 'GET',
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
    };
});
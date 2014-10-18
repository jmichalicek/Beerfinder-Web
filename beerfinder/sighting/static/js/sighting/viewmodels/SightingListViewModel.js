// Be sure to load js/sightings/models.js first
define(['jquery', 'underscore', 'knockout', 'vendor/infinitescroll', 'core/QueryStringParser', 'sighting/models/SightingModel'], function($, _, ko, infinitescroll, QueryStringParser, SightingModel) {
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
        this.queryString = new QueryStringParser(window.location.href);
    
        // stuff to enable infinite scroll
        this.nextPage = '';
        this.previousPage = '';
        this.sightings.extend({
            infinitescroll: {}
        });

        this.shouldDoRequestPage = function () {
            /* Determine if we shoud request another infinite scroll page */
            return self.sightings.peek().length - self.sightings.infinitescroll.lastVisibleIndex.peek() <= 25;
        };
        // detect scroll
        $(document).scroll(function() {
            // we need to pause watching this while an ajax request is being made
            // or we make a bunch of requests for the same data and make a mess of things
            self.sightings.infinitescroll.scrollY($('body').scrollTop());

            if (self.shouldDoRequestPage()) {
                if(!self.requestInProgress && self.nextPage) {
                    _.debounce(self.getSightings(), 250);
                }
            }
            _.debounce(updateViewportDimensions(), 250);
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
            self.sightings.infinitescroll.itemWidth(itemWidth);
            self.sightings.infinitescroll.itemHeight(itemHeight);
        }
        updateViewportDimensions();
    
        // end infinite scroll stuff

        this.getSightings = function() {
            var dfd = new $.Deferred();
            self.showLoadingSpinner(true);
            self.requestInProgress = true;
            var url = '/api/sightings/';

            var requestParams = {}
            if(self.nextPage) {
                requestParams['page'] = self.nextPage;
            }

            if (self.queryString.params['beer']) {
                requestParams['beer'] = self.queryString.params['beer'][0];
            }

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

        // view initialization... maybe should go into an init() method
        this.prefillSightingList = function () {
            self.getSightings().done(function (data) {
                if(self.shouldDoRequestPage() && data.next) {
                    self.prefillSightingList();
                };
            });
        };
        this.prefillSightingList();

        

        // end initialization
    };
});

var Modes = Object.freeze({LIST: 'list',
                           SEARCH: 'search'});

define(['jquery', 'underscore', 'knockout', 'vendor/infinitescroll', 'beer/models/BreweryModel', 'beer/models/BeerModel'], function($, _, ko, infinitescroll, BreweryModel, BeerModel) {

    return function () {
        "use strict";
        var self = this;

        this.showLoadingSpinner = ko.observable(false);

        this.mode = ko.observable(Modes.LIST);  // other option is search
        this.searchTerm = ko.observable();
        this.beerDataListOptions = ko.observableArray([]);

        this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling
        this.itemsPerRequest = 50;
        this.morePages = ko.observable(true);

        this.activeNavSection = ko.observable('beer_list');
        this.beers = ko.observableArray();
        //this.beer_list = ko.observableArray();

        // stuff to enable infinite scroll
        this.nextPage = '';
        this.previousPage = '';
        this.beers.extend({
            infinitescroll: {}
        });

        // detect resize
        $(window).resize(function() {
            updateViewportDimensions();
        });

        // detect scroll
        this.handleScroll = _.debounce(function () {
            self.beers.infinitescroll.scrollY($('body').scrollTop());

            // add more items if scroll reaches the last 15 items
            if (self.beers.peek().length - self.beers.infinitescroll.lastVisibleIndex.peek() <= 50) {
                // only do it if there's not already a request in progress and we have a next page to get
                if(!self.requestInProgress && self.nextPage) {
                    self.getBeerList();
                }
            }

        }, 250);

        $(document).scroll(function() {
            self.handleScroll();
        });

        // update dimensions of infinite-scroll viewport and item
        function updateViewportDimensions() {
            //var itemsRef = $('#beer_list'),
            var itemsRef = $('#page_body'),
            itemRef = $('#beer_list .beer-item').first(),
            itemsWidth = itemsRef.width(),
            itemsHeight = itemsRef.height(),
            itemWidth = itemRef.outerWidth(),
            itemHeight = itemRef.outerHeight(true);

            self.beers.infinitescroll.viewportWidth(itemsWidth);
            self.beers.infinitescroll.viewportHeight(itemsHeight);
            self.beers.infinitescroll.itemWidth(itemWidth);
            self.beers.infinitescroll.itemHeight(itemHeight);

        }
        updateViewportDimensions();

        // end infinite scroll stuff


        this.getBeerList = function() {
            self.requestInProgress = true;
            var url = '/api/beer/';
            var requestParams = {};
            // this may end up being handled in a separate function, separate observableArray,
            // and eventually even separate endpoint.
            // This was here based on misreading a response.  I think I won't need it.
            if(self.mode() === Modes.SEARCH) {
                requestParams['search'] = self.searchTerm();
            }

            if(self.nextPage) {
                // drf 3.1 change
                //requestParams['page'] = self.nextPage;
                url = self.nextPage;
            }

            $.ajax({url: url,
                    method: 'GET',
                    data: requestParams,
                   }).done(function (data) {
                       var currentList = self.beers();
                       ko.utils.arrayForEach(data.results, function(item) {
                           currentList.push(new BeerModel(item));
                       });
                       self.beers(currentList);
                       self.nextPage = data.next;
                   }).complete(function () {
                       self.requestInProgress = false;
                       if(self.nextPage) {
                           self.morePages(true);
                       } else {
                           self.morePages(false);
                       }

                       updateViewportDimensions();
                   });
        };

        this.submitSearchHandler = function () {
            self.beers([]);
            self.nextPage = '';
            var term = self.searchTerm().trim();
            if(term.length < 1) {
                self.mode(Modes.LIST);
            } else {
                self.mode(Modes.SEARCH);
            }
            self.searchTerm(term); // because of the trim
            self.getBeerList();
        };

        this.getBeerSuggestions = _.debounce(function () {
            var requestData = {};
            if(self.searchTerm()) {
                requestData.name = self.searchTerm();
            } else {
                return true;
            }

            $.ajax({
                url: '/api/beer/',
                data: requestData,
                type: 'GET'
            }).done(function (data) {
                var suggestions = [];
                ko.utils.arrayForEach(data.results, function(beer) {
                    suggestions.push(new BeerModel(beer));
                });
                self.beerDataListOptions(suggestions);
            });
            return true;
        }, 400);

        this.initialize = function () {
            self.getBeerList();
        };
    };
});

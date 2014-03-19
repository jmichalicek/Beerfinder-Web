var Modes = Object.freeze({LIST: 'list',
                           SEARCH: 'search'});

var ViewModel = function () {
    var self = this;

   // var Modes = Object.freeze({LIST: 'list',
   //                            SEARCH: 'search'});

    this.mode = ko.observable(Modes.LIST);  // other option is search
    this.searchTerm = ko.observable();
    this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling
    this.itemsPerRequest = 50;
    this.morePages = ko.observable(true);

    this.activeNavSection = ko.observable('beer_list');
    this.beers = ko.observableArray();
    this.beer_list = ko.observableArray();
  
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
    $(beer_list).scroll(function() {
        // we need to pause watching this while an ajax request is being made
        // or we make a bunch of requests for the same data and make a mess of things
        self.beers.infinitescroll.scrollY($(beer_list).scrollTop());

        // add more items if scroll reaches the last 15 items
        if (self.beers.peek().length - self.beers.infinitescroll.lastVisibleIndex.peek() <= 50) {
            // only do it if there's not already a request in progress and we have a next page to get
            if(!self.requestInProgress && self.nextPage) {
                self.getBeerList();
            }
        }
    });

    // update dimensions of infinite-scroll viewport and item
    function updateViewportDimensions() {
        var itemsRef = $('#beer_list'),
        itemRef = $('.beer_item').first(),
        itemsWidth = itemsRef.width(),
        itemsHeight = itemsRef.height(),
        itemWidth = itemRef.outerWidth(),
        itemHeight = itemRef.outerHeight();

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
        if(self.nextPage) {
            url = self.nextPage;
        }

        var requestParams = {};
        // this may end up being handled in a separate function, separate observableArray,
        // and eventually even separate endpoint.
        // This was here based on misreading a response.  I think I won't need it.
        if(self.mode() === Modes.SEARCH) {
        //    url += self.nextPage ? '&' : '?';
        //    url += 'search=' + self.searchTerm();
            requestParams = {search: self.searchTerm()};
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


    this.initialize = function () {
        self.getBeerList();
    };
};

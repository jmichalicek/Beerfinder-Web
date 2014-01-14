var ViewModel = function () {
    var self = this;

    this.searchTerm = ko.observable();
    this.requestInProgress = false;  // for determining whether or not to request more data based on scrolling
    this.itemsPerRequest = 50;
    this.maxResults = null;

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
            self.getBeerList();
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
        // TODO: pagination
        $.ajax({url: '/api/beer/' + self.nextPage,
                method: 'GET',
                data: {},
               }).done(function (data) {
                   var currentList = self.beers();
                   ko.utils.arrayForEach(data.results, function(item) {
                       currentList.push(new BeerModel(item));
                   });
                   self.beers(currentList);
               });
    };

    this.submitSearchHandler = function () {
//        if(self.searchTerm().length < 1) {
//            // just do regular explore if the search term was empty
//            self.discoverView(true);
//            self.getNearbyVenues();
//        } else {
//            self.discoverView(false);
//            self.searchForVenue();
//        }
    };


    this.initialize = function () {
        self.getBeerList();
    };
};

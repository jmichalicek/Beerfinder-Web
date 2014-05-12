//"id": 36, 
//"original": "sighting_images/2014/05/11/IMAG0009_13.jpg",
//"thumbnail": "sighting/images/2014/05/11/IMAG0009_13.jpg.thumbnail.jpg", "small": "sighting/images/2014/05/11/IMAG0009_13.jpg.sma//ll.jpg", "medium": "sighting/images/2014/05/11/IMAG0009_13.jpg.medium.jpg", "original_height": 3264, "original_width": 1840}

define(['jquery', 'knockout'], function($, ko) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};
        
        this.originalUrl = ko.observable(data.original)
        this.thumbnailUrl = ko.observable(data.thumbnail)
        this.smallUrl = ko.observable(data.small)
        this.mediumUrl = ko.observable(data.medium)

        this.originalWidth = ko.observable(data.original_width)
        this.originalHeight = ko.observable(data.original_height)
    };
});
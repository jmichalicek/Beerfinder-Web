define(['jquery', 'knockout'], function($, ko) {
    return function (data) {
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.BASE_URL = '/api/beer_styles/';

        this.id = ko.observable(data.id);
        this.name = ko.observable(data.name || '');
        this.slug = ko.observable(data.slug || '');        
    };
});

define(['jquery', 'knockout', 'sighting/models/SightingModel', 'sighting/models/SightingCommentModel', 'ko.toggleClass', 'ko.googleMap'], function ($, ko, SightingModel, SightingCommentModel, toggleClass, googleMap) {
    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.showLoadingSpinner = ko.observable(false);
        this.nextCommentPage = ko.observable(1);
        this.sighting = ko.observable(new SightingModel(data.sighting));
        this.activeNavSection = ko.observable('');
        this.comments = ko.observableArray([]);
        this.showMap = ko.observable(false);
        this.showComment = ko.observable(false);
        this.commentToggleText = ko.computed(function () {
            return self.showComment() ? "Cancel" : "Add Comment";
        });

        // need venue lat/lon
        this.sightingLocationMap = ko.observable({lat: ko.observable(-70),
                                                  lng: ko.observable(130)});

        this.toggleShowComment = function () {
            self.showComment(!self.showComment());
        }

        this.getComments = function () {
            var url = '/api/sightings/' + self.sighting().id() + '/comments/';
            var params = {};
            $.ajax({
                url: url,
                data: {page: self.nextCommentPage()}
            }).done(function (data) {
                var currentComments = self.comments()
                ko.utils.arrayForEach(data.results, function(comment) {
                    currentComments.push(new SightingCommentModel(comment));
                });
                self.comments(currentComments);
                self.nextCommentPage(data.next);
            });
        };

        this.addComment = function (formElement) {
            var formData = new FormData(formElement);
            $.ajax({
                url: self.sighting().url() + 'add_comment/',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                dataType: 'json'
            }).done(function (data) {
                //TODO: Something still not right... getting a 201 response but this is not happening
                self.comments.unshift(new SightingCommentModel(data));
                self.showComment(false);
            }).fail(function (data) {
                console.log(data);
            });
        };

        this.imageUrl = ko.computed(function () {
            var image = self.sighting().primaryImage();
            if(!image) {
                return '';
            }
            // not really the right way to do this fallback with knockout, but it works
            var pic = document.getElementById('sighting_image');
            if(pic) {
                pic.onerror = function () {
                    pic.src = image.originalUrl();
                };
            }
            return image.mediumUrl() ? image.mediumUrl() : image.originalUrl();
        });

        this.toggleMap = function () {
            self.showMap(!self.showMap());
        };
    };
});
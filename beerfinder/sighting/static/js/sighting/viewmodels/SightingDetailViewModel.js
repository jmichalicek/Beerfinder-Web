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

        this.sightingLocationMap = ko.observable({
            lat: ko.computed(function () {
                return parseFloat(self.sighting().venue().latitude())
            }),
            lng: ko.computed(function () {
                return parseFloat(self.sighting().venue().longitude())
            })
        });

        this.toggleShowComment = function () {
            self.showComment(!self.showComment());
        }

        this.getComments = function () {
            var url = '/api/sighting_comments/';
            var params = {
                sighting: self.sighting().id(),
                page: self.nextCommentPage()
            };
            $.ajax({
                url: url,
                data: params,
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
                url: '/api/sighting_comments/',
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

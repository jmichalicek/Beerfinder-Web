var ViewModel = function (data) {
    var self = this;
    this.sighting = ko.observable(new SightingModel(data.sighting));
    this.activeNavSection = ko.observable('');
    this.comments = ko.observable([]);

    this.getComments = function () {
        $.ajax({
            url: '/api/sightings/' + self.sighting().id() + '/comments/'
        }).done(function (data) {
            var currentComments = self.comments()
            ko.utils.arrayForEach(data.results, function(comment) {
                currentComments.push(new SightingCommentModel(comment));
            });
            self.comments(currentComments);
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
        }).fail(function (data) {
        });
    };
};
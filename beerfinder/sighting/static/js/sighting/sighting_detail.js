var ViewModel = function (data) {
    var self = this;
    this.nextCommentPage = ko.observable(null);
    this.sighting = ko.observable(new SightingModel(data.sighting));
    this.activeNavSection = ko.observable('');
    this.comments = ko.observableArray([]);
    this.showComment = ko.observable(false);
    this.commentToggleText = ko.computed(function () {
        return self.showComment() ? "Cancel" : "Add Comment";
    });

    this.toggleShowComment = function () {
        self.showComment(!self.showComment());
    }
    this.getComments = function () {
        var url = self.nextCommentPage() ||  '/api/sightings/' + self.sighting().id() + '/comments/';
        $.ajax({
            url: url,
            data: {page: self.commentPage}
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
        }).fail(function (data) {
        });
    };
};
var SightingCommentModel = function (data) {
    "use strict";
    var self = this;
    data = typeof data !== 'undefined' ? data : {};

    this.id = ko.observable(data.id);
    this.date_created = ko.observable(data.date_created);
    this.comment_by = ko.observable(data.comment_by);
    this.text = ko.observable(data.text);
};

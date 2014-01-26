var EditProfileViewModel = function (data) {
    var self = this;

    this.profile = ko.observable(new MyAccountModel({}));

    this.updateProfile = function () {
    };

    this.getProfile = function () {
        $.ajax({
            url: '/api/profile/me/',
            type: 'GET'
        }).done(function (data) {
            self.profile(new MyAccountModel(data));
        });
    }

    self.getProfile();
};
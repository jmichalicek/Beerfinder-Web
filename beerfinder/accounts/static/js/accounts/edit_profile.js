var ProfileSections = {
    PROFILE: 'profile',
    WATCHLIST: 'watchlist'
};

var activeView = ko.observable(ProfileSections.PROFILE);

var NavViewModel = function () {
    this.showProfile = function () {
        activeView(ProfileSections.PROFILE);
    };

    this.showWatchList = function () {
        activeView(ProfileSections.WATCHLIST);
    };
}


var EditProfileViewModel = function (data) {
    var self = this;

    this.isActive = ko.computed(function () {
        return activeView() == ProfileSections.PROFILE;
    });

    this.profile = ko.observable(new MyAccountModel({}));

    this.showSaveProfileSuccess = ko.observable(false);
    this.showSaveProfileError = ko.observable(false);
    this.saveProfileErrorText = ko.observable("");

    this.showChangePasswordSuccess = ko.observable(false);
    this.showChangePasswordError = ko.observable(false);
    this.changePasswordErrorText = ko.observable("");

    this.saveProfile = function (formElement) {
        //var formData = new FormData(formElement);

        $.ajax({
            url: '/api/profile/me/',
            type: 'POST',
            data: $(formElement).serialize(),
        }).done(function (){
            self.showSaveProfileSuccess(true);
        }).fail(function () {
            self.showSaveProfileError(true);
            self.saveProfileErrorText("Uh oh!");
        });
    };

    this.getProfile = function () {
        $.ajax({
            url: '/api/profile/me/',
            type: 'GET'
        }).done(function (data) {
            self.profile(new MyAccountModel(data));
        }).fail(function (data) {
            console.log("Error getting profile: " + data);
        });
    };
    
    this.changePassword = function (formElement) {
        $.ajax({
            url: '/api/profile/change_password/',
            type: 'POST',
            data: $(formElement).serialize()
        }).done(function () {
            self.showChangePasswordSuccess(true);
        }).fail(function (data) {
            // TODO: Parse data and get actual error(s) to display
            self.showChangePasswordError(true);
            self.changePasswordErrorText("Oh No!");
        }).complete(function () {
            $('#id_oldpassword').val('');
            $('#id_password1').val('');
            $('#id_password2').val('');
        });
    };

    self.getProfile();
};

var WatchlistViewModel = function (data) {
    var self = this;

    this.isActive = ko.computed(function () {
        return activeView() == ProfileSections.WATCHLIST;
    });

    // TODO: infinite scroll for watchlist
    this.watchlist = ko.observableArray([]);

    this.getWatchlist = function () {
        $.ajax({
            url: '/api/watchlist/',
            type: 'GET'
        }).done(function (data) {
            var currentList = self.watchlist();
            ko.utils.arrayForEach(data.results, function(item) {
                currentList.push(new WatchedBeerModel(item));
            });
            self.watchlist(currentList);
            // self.nextPage = data.next_page;
        }).fail(function (data) {
            console.log("Ooops" + data);
        });
    };

    this.removeFromWatchlist = function (watchedBeer) {
        $.ajax({
            url: watchedBeer.url(),
            type: 'DELETE',
            dataType: 'text',
            cache: false,
        }).done(function (data) {
            self.watchlist.remove(watchedBeer);
        }).fail(function (data) {
            console.log(data);
        });
    }
};
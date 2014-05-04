define(['jquery', 'knockout', 'accounts/models/MyAccountModel'], function ($, ko, MyAccountModel) {

    return function (data) {
        "use strict";
        var self = this;
        data = typeof data !== 'undefined' ? data : {};

        this.profileNavController = ko.observable(data.profileNavController);

        this.isActive = ko.computed(function () {
            return self.profileNavController().activeView() == self.profileNavController().ProfileSections.PROFILE;
        });
        
        this.profile = ko.observable(new MyAccountModel({}));
        
        this.showSaveProfileSuccess = ko.observable(false);
        this.showSaveProfileError = ko.observable(false);
        this.saveProfileErrorText = ko.observable("");
        
        this.showChangePasswordSuccess = ko.observable(false);
        this.showChangePasswordError = ko.observable(false);
        this.changePasswordErrorText = ko.observable("");
        
        this.saveProfile = function (formElement) {
            $.ajax({
                url: '/api/profile/me/',
                type: 'POST',
                data: self.profile().toApiFormData(),
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
});
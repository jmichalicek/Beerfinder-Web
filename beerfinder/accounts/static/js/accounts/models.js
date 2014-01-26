var MyAccountModel = function (data) {
    var self = this;

    self.firstName = ko.observable(data.first_name);
    self.lastName = ko.observable(data.last_name);
    self.email = ko.observable(data.email);
    self.username = ko.observable(data.username);
    self.showNameOnSightings =  ko.observable(data.show_name_on_sightings);
    
}
var MyAccountModel = function (data) {
    var self = this;

    self.firstName = ko.observable(data.first_name);
    self.lastName = ko.observable(data.last_name);
    
}
define(['jquery', 'knockout', 'beer/models/BeerModel', 'beer/models/BreweryModel'], function($, ko, BeerModel, BreweryModel) {
    return function (data) {
        var self = this;

        // we basically just have a form to submit
        // there's probably a good way to do this with BeerModel... I guess this is where using backbone comes in handy
        this.beerName = ko.observable('');
        this.breweryName = ko.observable('');
        this.formErrors = ko.observableArray([]);

        this.addBeer = function() {
            var beer = new BeerModel({name: self.beerName(),
                                      brewery: new BreweryModel({name: self.breweryName()})
                                     });
            beer.create().done(function (data) {
                location = '/beer/'.concat(data.slug, '/');
            }).fail(function (data) {
                errors = data.responseJSON;
                var errorList = [];
                ko.utils.arrayForEach(_.keys(errors), function (key) {
                    ko.utils.arrayForEach(errors[key], function (value) {
                        if(key !== 'non_field_errors' && key !== '__all__') {
                            errorList.push(key + ': ' + value);
                        } else {
                            errorList.push(value);
                        }
                    });
                });
                self.formErrors(errorList);
            });
        };
    };
});
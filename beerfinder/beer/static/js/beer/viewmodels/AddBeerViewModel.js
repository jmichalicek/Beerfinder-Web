define(['jquery', 'knockout', 'underscore', 'beer/models/BeerModel', 'beer/models/BreweryModel', 'beer/models/StyleModel'],
       function($, ko, _, BeerModel, BreweryModel, StyleModel) {
    return function (data) {
        var self = this;

        // we basically just have a form to submit
        // there's probably a good way to do this with BeerModel... I guess this is where using backbone comes in handy
        this.beerName = ko.observable('');
        this.breweryName = ko.observable('');
        this.styles = ko.observableArray([]);
        this.selectedStyle = ko.observable();
        this.formErrors = ko.observableArray([]);
        this.stylePickerVisible = ko.observable(false);
        
        this.showStylePicker = function () {
            self.stylePickerVisible(true);
        };

        this.selectStyle = function (style) {
            self.selectedStyle(style);
            self.stylePickerVisible(false);
        };

        this.addBeer = function() {
            var beer = new BeerModel({name: self.beerName(),
                                      brewery: new BreweryModel({name: self.breweryName()}),
                                      style: new StyleModel(self.selectedStyle()),
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

        this.getStyles = function () {
            $.ajax({
                url: '/api/beer_styles/',
                type: 'GET'
            }).done(function (data) {
                var styles = [];
                ko.utils.arrayForEach(data.results, function (style) {
                    styles.push(new StyleModel(style));
                });
                self.styles(styles);
            });
        };
    };
});
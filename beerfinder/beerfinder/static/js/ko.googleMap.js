(function (factory) {
    // Module systems magic dance.

    if (typeof require === "function" && typeof exports === "object" && typeof module === "object") {
        // CommonJS or Node: hard-coded dependency on "knockout"
        factory(require("knockout"), exports);
    } else if (typeof define === "function" && define["amd"]) {
        // AMD anonymous module with hard-coded dependency on "knockout"
        define(["knockout", "exports"], factory);
    } else {
        // <script> tag: use the global `ko` object
        factory(ko, {});
    }
}(function (ko, exports) {
    ko.bindingHandlers.googleMap = {
        init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
            var mapObj = ko.utils.unwrapObservable(valueAccessor());
            var latLng = new google.maps.LatLng(
                ko.utils.unwrapObservable(mapObj.lat),
                ko.utils.unwrapObservable(mapObj.lng));
            var mapOptions = {center: latLng,
                              zoom: 5, 
                              mapTypeId: google.maps.MapTypeId.ROADMAP};
            
            mapObj.googleMap = new google.maps.Map(element, mapOptions);
        },
    };
});
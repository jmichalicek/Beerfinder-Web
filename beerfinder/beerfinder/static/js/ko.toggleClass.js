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
    ko.bindingHandlers.toggleClass = {
        //TODO : update to allow specification of events to bind to.
        // TODO: update to allow specifying a target to toggle the class on?
        // TODO: Update to allow a smaller binding context than document, like jQuery's .on() does, but don't force use of jQuery
        init: function(element, valueAccessor) {
            var value = ko.unwrap(valueAccessor());
            document.addEventListener("click", function(event) {
                // retrieve an event if it was called manually
                event = event || window.event;
                
                // retrieve the related element
                var el = event.target || event.srcElement;
                
                if(el == element) {
                    //required to make the "return false" to affect
                    event.preventDefault();
                    element.classList.toggle(value);
                }
            }, true);
           
        },
        update: function(element, valueAccessor) {} 
    };
}));
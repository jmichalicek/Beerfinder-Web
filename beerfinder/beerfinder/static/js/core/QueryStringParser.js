/* Simple function for getting querystring params */

define([], function () {
    return function (url) {
        "use strict";
        var self = this;
        
        this.url = typeof url !== 'undefined' ? url : '';
        this.params = {};
    
        this.getParams = function (url) {
            /* Takes a full url such as
               http://www.example.com/?foo=bar
               */

            url = typeof url !== 'undefined' ? url : '';

            var parts = url.split('?', 2),
                params = {},
                what = Object.prototype.toString;

            if (parts.length > 1) {
                // assuming ampersand, but technically semicolon can also be a separator
                // not sure how this will behave if there is an ampersand in a value... can't remmeber how it gets encoded
                var splitQS = parts[1].split('&');
                for(var i=0; i<splitQS.length; i++) {
                    var current = splitQS[i].split('=', 2);
                    var key = current[0];
                    var value = current[1];
                    
                    // make params[key] an array and append to it to deal with multiple keys of the same name
                    if (!params[key] || what.call(params[key] !== "[object Array]")) {
                        /* I sure hope you didn't have anything important in there! */
                        params[key] = [];
                    }
                    params[key].push(value);
                }
            }
            return params;
        };
        
        self.params = self.getParams(self.url);
    };
});
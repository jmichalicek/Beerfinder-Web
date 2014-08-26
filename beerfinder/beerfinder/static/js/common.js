/* require.config({
    baseUrl: "/static/js/",
    paths: {
        core: 'core',
        beer: 'beer',
        accounts: 'accounts',
        sighting: 'sighting',
        watchlist: 'watchlist',
        venue: 'venue',
        vendor: 'vendor',
        moment: 'vendor/moment-with-langs',
        knockout: '//ajax.aspnetcdn.com/ajax/knockout/knockout-3.1.0',
        jquery: '//ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min',
        jqueryui: '//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min',
        bootstrap: '//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min',
            //underscore: '//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.6.0/underscore-min',
        underscore: '//cdnjs.cloudflare.com/ajax/libs/lodash.js/2.4.1/lodash.underscore.min',
        lodash: '//cdnjs.cloudflare.com/ajax/libs/lodash.js/2.4.1/lodash.underscore.min',
        pubsub: 'vendor/pubsub',
    },

    shim: {
        infinitescroll: ['knockout'],
        bootstrap: ['jquery'],
        jqueryui: ['jquery'],
        csrf:  ['jquery'],
        //'underscore' : {
        //    exports : '_'
        //},
    },
    deps: ['jquery', 'bootstrap', 'knockout', 'csrf'],
    callback: function () {
        jQuery.ajaxSettings.traditional = true;
        $.ajaxSetup({
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
        });
    }
}); */

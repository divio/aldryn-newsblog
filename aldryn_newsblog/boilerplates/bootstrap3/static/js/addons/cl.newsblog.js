/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

//######################################################################################################################
// #NAMESPACES#
var Cl = window.Cl || {};

//######################################################################################################################
// #UTILS#
(function ($) {
    'use strict';

    Cl.newsBlog = {

        // INFO: autoinit certain functionalities
        init: function () {
            var that = this;

            $('.js-aldryn-newsblog-article-search').each(function () {
                that._search($(this));
            });
        },

        // INFO: handles search form
        _search: function (container) {
            var form = container.find('form');

            form.on('submit', function (e) {
                e.preventDefault();

                $.ajax({
                    'type': 'get',
                    'url': form.prop('action'),
                    'data': form.serialize()
                }).always(function (data) {
                    form.siblings('.js-search-results').html(data);
                });
            });
        }

    };

    // autoload
    if ($('.js-aldryn-newsblog-article-search').length) {
        Cl.newsBlog.init();
    }

})(jQuery);

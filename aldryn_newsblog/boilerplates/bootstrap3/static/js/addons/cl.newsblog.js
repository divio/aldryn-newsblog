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

        init: function () {
            var that = this;

            // there might be more addons available within one page
            $('.js-aldryn-newsblog-article-search').each(function () {
                that._search($(this));
            });
        },

        _search: function (container) {
            var form = container.find('form');

            form.on('submit', function (e) {
                e.preventDefault();

                $.ajax({
                    type: 'GET',
                    url: form.prop('action'),
                    data: form.serialize()
                }).always(function (data) {
                    form.siblings('.js-search-results').html(data);
                }).fail(function () {
                    alert('REQUEST TIMEOUT');
                });
            });
        }

    };

    // autoload
    $(function () {
        if ($('.js-aldryn-newsblog-article-search').length) {
            Cl.newsBlog.init();
        }
    });

})(jQuery);

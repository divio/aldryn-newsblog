/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global Cl, $, describe, window, it, expect, beforeEach, afterEach, fixture, spyOn */

// #############################################################################
// UNIT TEST
describe('cl.newsblog.js:', function () {
    beforeEach(function () {
        fixture.setBase('frontend/fixtures');
        this.markup = fixture.load('search.html');
        this.preventEvent = { preventDefault: function () {} };
    });

    afterEach(function () {
        fixture.cleanup();
    });

    it('has available Cl namespace', function () {
        expect(Cl).toBeDefined();
    });

    it('has a public method _search', function () {
        expect(Cl.newsBlog._search).toBeDefined();
    });

    describe('Cl.newsBlog.init(): ', function () {
        it('returns undefined', function () {
            expect(Cl.newsBlog.init()).toEqual(undefined);
        });

        it('runs _search()', function () {
            spyOn(Cl.newsBlog, '_search');
            Cl.newsBlog.init();

            // validate that _search was called inside Cl.newsBlog.init()
            expect(Cl.newsBlog._search).toHaveBeenCalled();
            // validate 2 call as 2 js-aldryn-newsblog-article-search is
            // specified in search.html
            expect(Cl.newsBlog._search.calls.count()).toEqual(2);
        });
    });

    describe('Cl.newsBlog._search: ', function () {
        it('returns undefined', function () {
            // validate the return of undefined
            expect(Cl.newsBlog._search(
                $('.js-aldryn-newsblog-article-search').eq(1)))
                    .toEqual(undefined);
        });

        it('has correct url parameter in ajax request', function () {
            spyOn($, 'ajax').and.returnValue({
                always: function () {
                    return { fail: function () {} };
                }
            });

            Cl.newsBlog._handler.call(
                $('.js-aldryn-newsblog-article-search .form-inline')[0],
                    this.preventEvent);

            var callArgs = $.ajax.calls.allArgs()[0][0];

            // validate ajax request url
            expect(callArgs.url).toEqual(
                '/en/blog/search/'
            );
        });

        it('has correct data parameter in ajax request', function () {
            spyOn($, 'ajax').and.returnValue({
                always: function () {
                    return { fail: function () {} };
                }
            });
            Cl.newsBlog._handler.call(
                $('.js-aldryn-newsblog-article-search .form-inline')[0],
                    this.preventEvent);

            var callArgs = $.ajax.calls.allArgs()[0][0];

            // validate ajax request data
            expect(callArgs.data).toEqual(
                'csrfmiddlewaretoken=Ui0tGBmn0Thq5LUeUS2m4zAF20H0M8up&' +
                'max_articles=10&q='
            );
        });

        it('has ajax request with "always" function adding results data ' +
            'correctly', function () {
            // emulate always after ajax call
            spyOn($, 'ajax').and.returnValue({
                always: function (callback) {
                    callback('<h2>Test results</h2>');

                    return { fail: function () {} };
                }
            });

            Cl.newsBlog._handler.call(
                $('.js-aldryn-newsblog-article-search .form-inline')[0],
                    this.preventEvent);

            // validate search results got updated with new info
            expect($('.js-search-results')[0].innerHTML).toEqual(
                '<h2>Test results</h2>');
        });

        it('has ajax request with "fail" function alert working ' +
            'correctly', function () {
            // emulate fail after always after ajax call
            spyOn($, 'ajax').and.returnValue({
                always: function () {
                    return {
                        fail: function (callback) {
                            callback();
                        }
                    };
                }
            });

            spyOn(window, 'alert');

            Cl.newsBlog._handler.call(
                $('.js-aldryn-newsblog-article-search .form-inline')[0],
                    this.preventEvent);

            // validate alert text
            expect(window.alert).toHaveBeenCalledWith('REQUEST TIMEOUT');
        });
    });

});

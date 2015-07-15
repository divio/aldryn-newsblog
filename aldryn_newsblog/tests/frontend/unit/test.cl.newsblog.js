/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global Cl, describe, it, expect, beforeEach, afterEach, fixture, spyOn */

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

    });

});

/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global Cl, describe, it, expect, beforeEach, afterEach, fixture, spyOn */

// #############################################################################
// UNIT TEST
describe('cl.blognews.js:', function () {
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

});

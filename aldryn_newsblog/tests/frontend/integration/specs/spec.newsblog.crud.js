/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser */

// #############################################################################
// INTEGRATION TEST
var newsBlogPage = require('../pages/page.newsblog.crud.js');

describe('Aldryn Newsblog tests: ', function () {
    it('logs in to the site with valid username and password', function () {
        // go to the main page
        browser.get(newsBlogPage.site);

        // check if the page already exists
        newsBlogPage.testLink.isPresent().then(function (present) {
            if (present === true) {
                // go to the main page
                browser.get(newsBlogPage.site + '?edit');
            } else {
                // click edit mode link
                newsBlogPage.editModeLink.click();
            }

            // wait for username input to appear
            browser.wait(browser.isElementPresent(newsBlogPage.usernameInput),
                newsBlogPage.mainElementsWaitTime);

            // login to the site
            newsBlogPage.cmsLogin();
        });
    });

});

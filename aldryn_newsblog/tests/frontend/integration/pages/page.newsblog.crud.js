/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global by, element, browser, expect */

// #############################################################################
// INTEGRATION TEST PAGE OBJECT

var newsBlogPage = {
    site: 'http://127.0.0.1:8000/en/',
    mainElementsWaitTime: 12000,
    iframeWaitTime: 15000,

    // log in, log out
    editModeLink: element(by.css('.inner a[href="/?edit"]')),
    usernameInput: element(by.id('id_cms-username')),
    passwordInput: element(by.id('id_cms-password')),
    loginButton: element(by.css('.cms_form-login input[type="submit"]')),
    userMenus: element.all(by.css('.cms_toolbar-item-navigation > li > a')),
    testLink: element(by.css('.selected a')),

    cmsLogin: function (credentials) {
        // object can contain username and password, if not set it will
        // fallback to 'admin'
        credentials = credentials ||
            { username: 'admin', password: 'admin' };

        newsBlogPage.usernameInput.clear();

        // fill in email field
        newsBlogPage.usernameInput.sendKeys(
            credentials.username).then(function () {
            newsBlogPage.passwordInput.clear();

            // fill in password field
            newsBlogPage.passwordInput.sendKeys(
                credentials.password);
        }).then(function () {
            newsBlogPage.loginButton.click();

            // wait for user menu to appear
            browser.wait(browser.isElementPresent(
                newsBlogPage.userMenus.first()),
                newsBlogPage.mainElementsWaitTime);

            // validate user menu
            expect(newsBlogPage.userMenus.first().isDisplayed())
                .toBeTruthy();
        });
    }

};

module.exports = newsBlogPage;

/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global by, element, expect */

// #############################################################################
// INTEGRATION TEST PAGE OBJECT

var cmsProtractorHelper = require('cms-protractor-helper');

var newsBlogPage = {
    site: 'http://127.0.0.1:8000/en/',

    // log in, log out
    editModeLink: element(by.css('.inner a[href="/?edit"]')),
    usernameInput: element(by.id('id_cms-username')),
    passwordInput: element(by.id('id_cms-password')),
    loginButton: element(by.css('.cms_form-login input[type="submit"]')),
    userMenus: element.all(by.css('.cms_toolbar-item-navigation > li > a')),
    testLink: element(by.css('.selected a')),

    // adding new page
    userMenuDropdown: element(by.css(
        '.cms_toolbar-item-navigation-hover')),
    administrationOptions: element.all(by.css(
        '.cms_toolbar-item-navigation a[href="/en/admin/"]')),
    sideMenuIframe: element(by.css('.cms_sideframe-frame iframe')),
    pagesLink: element(by.css('.model-page > th > a')),
    addPageLink: element(by.css('.sitemap-noentry .addlink')),
    titleInput: element(by.id('id_title')),
    slugErrorNotification: element(by.css('.errors.slug')),
    saveButton: element(by.css('.submit-row [name="_save"]')),
    editPageLink: element(by.css('.col1 [href*="preview/"]')),

    // adding new apphook config
    breadcrumbsLinks: element.all(by.css('.breadcrumbs a')),
    newsBlogConfigsLink: element(by.css('.model-newsblogconfig > th > a')),
    editConfigsLink: element(by.css('.row1 > th > a')),
    addConfigsButton: element(by.css('.object-tools .addlink')),
    namespaceInput: element(by.id('id_namespace')),
    applicationTitleInput: element(by.id('id_app_title')),
    successNotification: element(by.css('.messagelist .success')),

    // adding new article
    addArticleButton: element(by.css('.model-article .addlink')),
    englishLanguageTab: element(by.css(
        '.parler-language-tabs > .empty > a[href*="language=en"]')),
    saveAndContinueButton: element(by.css('.submit-row [name="_continue"]')),
    editArticleLinks: element.all(by.css(
        '.results th > [href*="/aldryn_newsblog/article/"]')),

    // adding article to the page
    aldrynNewsBlogBlock: element(by.css('.aldryn-newsblog-list')),
    advancedSettingsOption: element(by.css(
        '.cms_toolbar-item-navigation [href*="advanced-settings"]')),
    modalIframe: element(by.css('.cms_modal-frame iframe')),
    applicationSelect: element(by.id('application_urls')),
    newsBlogOption: element(by.css('option[value="NewsBlogApp"]')),
    saveModalButton: element(by.css('.cms_modal-buttons .cms_btn-action')),
    newsBlogMetaBlock: element(by.css('.aldryn-newsblog-meta')),
    articleLink: element(by.css('.aldryn-newsblog-list h2 > a')),

    // deleting article
    deleteButton: element(by.css('.deletelink-box a')),
    sidebarConfirmationButton: element(by.css('#content [type="submit"]')),

    cmsLogin: function (credentials) {
        // object can contain username and password, if not set it will
        // fallback to 'admin'
        credentials = credentials ||
            { username: 'admin', password: 'admin' };

        newsBlogPage.usernameInput.clear();

        // fill in email field
        return newsBlogPage.usernameInput.sendKeys(credentials.username)
            .then(function () {
            newsBlogPage.passwordInput.clear();

            // fill in password field
            return newsBlogPage.passwordInput.sendKeys(credentials.password);
        }).then(function () {
            newsBlogPage.loginButton.click();

            // wait for user menu to appear
            cmsProtractorHelper.waitFor(newsBlogPage.userMenus.first());

            // validate user menu
            expect(newsBlogPage.userMenus.first().isDisplayed()).toBeTruthy();
        });
    }

};

module.exports = newsBlogPage;

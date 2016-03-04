/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global browser, by, element, expect */

// #############################################################################
// INTEGRATION TEST PAGE OBJECT

var page = {
    site: 'http://127.0.0.1:8000/en/',

    // log in, log out
    editModeLink: element(by.css('.inner a[href="/?edit"]')),
    usernameInput: element(by.id('id_username')),
    passwordInput: element(by.id('id_password')),
    loginButton: element(by.css('input[type="submit"]')),
    userMenus: element.all(by.css('.cms-toolbar-item-navigation > li > a')),

    // adding new page
    modalCloseButton: element(by.css('.cms-modal-close')),
    userMenuDropdown: element(by.css(
        '.cms-toolbar-item-navigation-hover')),
    administrationOptions: element.all(by.css(
        '.cms-toolbar-item-navigation a[href="/en/admin/"]')),
    sideMenuIframe: element(by.css('.cms-sideframe-frame iframe')),
    pagesLink: element(by.css('.model-page > th > a')),
    addPageLink: element(by.css('.object-tools .addlink')),
    titleInput: element(by.id('id_title')),
    slugErrorNotification: element(by.css('.errors.slug')),
    saveButton: element(by.css('.submit-row [name="_save"]')),
    editPageLink: element(by.css('.cms-tree-item-preview [href*="preview/"]')),
    testLink: element(by.cssContainingText('a', 'Test')),
    sideFrameClose: element(by.css('.cms-sideframe-close')),

    // adding new apphook config
    breadcrumbs: element(by.css('.breadcrumbs')),
    breadcrumbsLinks: element.all(by.css('.breadcrumbs a')),
    newsBlogConfigsLink: element(by.css('.model-newsblogconfig > th > a')),
    editConfigsLink: element(by.css('.row1 > th > a')),
    addConfigsButton: element(by.css('.object-tools .addlink')),
    namespaceInput: element(by.id('id_namespace')),
    applicationTitleInput: element(by.id('id_app_title')),
    successNotification: element(by.css('.messagelist .success')),

    // adding new article
    addArticleButton: element(by.css('.model-article .addlink')),
    editArticlesLink: element(by.css('.model-article .changelink')),
    englishLanguageTab: element(by.css(
        '.parler-language-tabs > .empty > a[href*="language=en"]')),
    saveAndContinueButton: element(by.css('.submit-row [name="_continue"]')),
    editArticleLinksTable: element(by.css('.results')),
    editArticleLinks: element.all(by.css(
        '.results th > [href*="/aldryn_newsblog/article/"]')),

    // adding article to the page
    aldrynNewsBlogBlock: element(by.css('.aldryn-newsblog-list')),
    advancedSettingsOption: element(by.css(
        '.cms-toolbar-item-navigation [href*="advanced-settings"]')),
    modalIframe: element(by.css('.cms-modal-frame iframe')),
    applicationSelect: element(by.id('application_urls')),
    newsBlogOption: element(by.css('option[value="NewsBlogApp"]')),
    saveModalButton: element(by.css('.cms-modal-buttons .cms-btn-action')),
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

        page.usernameInput.clear();

        // fill in email field
        page.usernameInput.sendKeys(
            credentials.username).then(function () {
            page.passwordInput.clear();

            // fill in password field
            return page.passwordInput.sendKeys(
                credentials.password);
        }).then(function () {
            return page.loginButton.click();
        }).then(function () {
            // this is required for django1.6, because it doesn't redirect
            // correctly from admin
            browser.get(page.site);

            // wait for user menu to appear
            browser.wait(browser.isElementPresent(
                page.userMenus.first()),
                page.mainElementsWaitTime);

            // validate user menu
            expect(page.userMenus.first().isDisplayed())
                .toBeTruthy();
        });
    }

};

module.exports = page;

/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser, By, expect */

// #############################################################################
// INTEGRATION TEST
var newsBlogPage = require('../pages/page.newsblog.crud.js');
var cmsProtractorHelper = require('cms-protractor-helper');

describe('Aldryn Newsblog tests: ', function () {
    // create random article name
    var articleName = 'Test article ' + cmsProtractorHelper.randomDigits(4);

    it('logs in to the site with valid username and password', function () {
        // go to the main page
        browser.get(newsBlogPage.site);

        // check if the page already exists
        return newsBlogPage.testLink.isPresent().then(function (present) {
            if (present === true) {
                // go to the main page
                browser.get(newsBlogPage.site + '?edit');
            } else {
                // click edit mode link
                newsBlogPage.editModeLink.click();
            }

            // wait for username input to appear
            cmsProtractorHelper.waitFor(newsBlogPage.usernameInput);

            // login to the site
            newsBlogPage.cmsLogin();
        });
    });

    it('creates a new test page', function () {
        // click the example.com link in the top menu
        return newsBlogPage.userMenus.first().click().then(function () {
            // wait for top menu dropdown options to appear
            cmsProtractorHelper.waitFor(newsBlogPage.userMenuDropdown);

            return newsBlogPage.administrationOptions.first().click();
        }).then(function () {
            // wait for modal iframe to appear
            cmsProtractorHelper.waitFor(newsBlogPage.sideMenuIframe);

            // switch to sidebar menu iframe
            browser.switchTo().frame(browser.findElement(
                By.css('.cms_sideframe-frame iframe')));

            cmsProtractorHelper.waitFor(newsBlogPage.pagesLink);

            newsBlogPage.pagesLink.click();

            // wait for iframe side menu to reload
            cmsProtractorHelper.waitFor(newsBlogPage.addConfigsButton);

            // check if the page already exists and return the status
            return newsBlogPage.addPageLink.isPresent();
        }).then(function (present) {
            if (present === true) {
                // page is absent - create new page
                cmsProtractorHelper.waitFor(newsBlogPage.addPageLink);

                newsBlogPage.addPageLink.click();

                cmsProtractorHelper.waitFor(newsBlogPage.titleInput);

                return newsBlogPage.titleInput.sendKeys('Test').then(function () {
                    newsBlogPage.saveButton.click();

                    return newsBlogPage.slugErrorNotification.isPresent();
                }).then(function (present) {
                    if (present === false) {
                        cmsProtractorHelper.waitFor(newsBlogPage.editPageLink);

                        // wait till the editPageLink will become clickable
                        browser.sleep(500);

                        // validate/click edit page link
                        newsBlogPage.editPageLink.click();

                        // switch to default page content
                        browser.switchTo().defaultContent();

                        cmsProtractorHelper.waitFor(newsBlogPage.testLink);

                        // validate test link text
                        return newsBlogPage.testLink.getText().then(function (title) {
                            expect(title).toEqual('Test');
                        });
                    }
                });
            }
        });
    });

    it('creates a new apphook config', function () {
        // check if the focus is on sidebar ifarme
        return newsBlogPage.editPageLink.isPresent().then(function (present) {
            if (present === false) {
                // wait for modal iframe to appear
                cmsProtractorHelper.waitFor(newsBlogPage.sideMenuIframe);

                // switch to sidebar menu iframe
                return browser.switchTo().frame(browser.findElement(By.css(
                    '.cms_sideframe-frame iframe')));
            }
        }).then(function () {
            cmsProtractorHelper.waitFor(newsBlogPage.breadcrumbsLinks.first());

            // click the Home link in breadcrumbs
            newsBlogPage.breadcrumbsLinks.first().click();

            cmsProtractorHelper.waitFor(newsBlogPage.newsBlogConfigsLink);

            newsBlogPage.newsBlogConfigsLink.click();

            // check if the apphook config already exists and return the status
            return newsBlogPage.editConfigsLink.isPresent();
        }).then(function (present) {
            if (present === false) {
                // apphook config is absent - create new apphook config
                cmsProtractorHelper.waitFor(newsBlogPage.addConfigsButton);

                newsBlogPage.addConfigsButton.click();

                cmsProtractorHelper.waitFor(newsBlogPage.namespaceInput);

                return newsBlogPage.namespaceInput.sendKeys('aldryn_newsblog')
                    .then(function () {
                    return newsBlogPage.applicationTitleInput.sendKeys('Test title');
                }).then(function () {
                    newsBlogPage.saveButton.click();

                    cmsProtractorHelper.waitFor(newsBlogPage.successNotification);
                });
            }
        });
    });

    it('creates a new article', function () {
        cmsProtractorHelper.waitFor(newsBlogPage.breadcrumbsLinks.first());

        // click the Home link in breadcrumbs
        newsBlogPage.breadcrumbsLinks.first().click();

        cmsProtractorHelper.waitFor(newsBlogPage.addArticleButton);

        newsBlogPage.addArticleButton.click();

        cmsProtractorHelper.waitFor(newsBlogPage.englishLanguageTab);

        return newsBlogPage.englishLanguageTab.click().then(function () {
            cmsProtractorHelper.waitFor(newsBlogPage.titleInput);

            return newsBlogPage.titleInput.sendKeys(articleName);
        }).then(function () {
            browser.actions().mouseMove(newsBlogPage.saveAndContinueButton)
                .perform();
            newsBlogPage.saveButton.click();

            cmsProtractorHelper.waitFor(newsBlogPage.successNotification);

            // validate success notification
            expect(newsBlogPage.successNotification.isDisplayed())
                .toBeTruthy();
            // validate edit article link
            expect(newsBlogPage.editArticleLinks.first().isDisplayed())
                .toBeTruthy();
        });
    });

    it('adds a new article on the page', function () {
        // switch to default page content
        browser.switchTo().defaultContent();

        // add articles to the page only if they were not added before
        return newsBlogPage.aldrynNewsBlogBlock.isPresent().then(function (present) {
            if (present === false) {
                // click the Page link in the top menu
                return newsBlogPage.userMenus.get(1).click().then(function () {
                    // wait for top menu dropdown options to appear
                    cmsProtractorHelper.waitFor(newsBlogPage.userMenuDropdown);

                    newsBlogPage.advancedSettingsOption.click();

                    // wait for modal iframe to appear
                    cmsProtractorHelper.waitFor(newsBlogPage.modalIframe);

                    // switch to modal iframe
                    browser.switchTo().frame(browser.findElement(By.css(
                        '.cms_modal-frame iframe')));

                    cmsProtractorHelper.selectOption(newsBlogPage.applicationSelect,
                        'NewsBlog', newsBlogPage.newsBlogOption);

                    // switch to default page content
                    browser.switchTo().defaultContent();

                    cmsProtractorHelper.waitFor(newsBlogPage.saveModalButton);

                    browser.actions().mouseMove(newsBlogPage.saveModalButton)
                        .perform();
                    return newsBlogPage.saveModalButton.click();
                }).then(function () {
                    // wait for aldryn-newsblog block to appear
                    cmsProtractorHelper.waitFor(newsBlogPage.aldrynNewsBlogBlock);

                    // validate aldryn-newsblog block
                    expect(newsBlogPage.aldrynNewsBlogBlock.isDisplayed())
                        .toBeTruthy();
                    // validate aldryn-newsblog meta block
                    expect(newsBlogPage.newsBlogMetaBlock.isDisplayed())
                        .toBeTruthy();
                    // validate article link
                    expect(newsBlogPage.articleLink.isDisplayed())
                        .toBeTruthy();
                });
            }
        });
    });

    it('deletes article', function () {
        // wait for modal iframe to appear
        cmsProtractorHelper.waitFor(newsBlogPage.sideMenuIframe);

        // switch to sidebar menu iframe
        browser.switchTo()
            .frame(browser.findElement(By.css('.cms_sideframe-frame iframe')));

        // wait for edit event link to appear
        cmsProtractorHelper.waitFor(newsBlogPage.editArticleLinks.first());

        // validate edit article links texts to delete proper article
        return newsBlogPage.editArticleLinks.first().getText().then(function (text) {
            if (text === articleName) {
                return newsBlogPage.editArticleLinks.first().click();
            } else {
                return newsBlogPage.editArticleLinks.get(1).getText()
                    .then(function (text) {
                    if (text === articleName) {
                        return newsBlogPage.editArticleLinks.get(1).click();
                    } else {
                        return newsBlogPage.editArticleLinks.get(2).getText()
                            .then(function (text) {
                            if (text === articleName) {
                                return newsBlogPage.editArticleLinks.get(2).click();
                            }
                        });
                    }
                });
            }
        }).then(function () {
            // wait for delete button to appear
            cmsProtractorHelper.waitFor(newsBlogPage.deleteButton);

            browser.actions().mouseMove(newsBlogPage.saveAndContinueButton)
                .perform();
            return newsBlogPage.deleteButton.click();
        }).then(function () {
            // wait for confirmation button to appear
            cmsProtractorHelper.waitFor(newsBlogPage.sidebarConfirmationButton);

            newsBlogPage.sidebarConfirmationButton.click();

            cmsProtractorHelper.waitFor(newsBlogPage.successNotification);

            // validate success notification
            expect(newsBlogPage.successNotification.isDisplayed()).toBeTruthy();

            // switch to default page content
            browser.switchTo().defaultContent();

            // refresh the page to see changes
            browser.refresh();
        });
    });

});

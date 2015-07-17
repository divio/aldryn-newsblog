/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser, By, expect */

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
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.usernameInput);
            }, newsBlogPage.mainElementsWaitTime);

            // login to the site
            newsBlogPage.cmsLogin();
        });
    });

    it('creates a new test page', function () {
        // click the example.com link in the top menu
        newsBlogPage.userMenus.first().click().then(function () {
            // wait for top menu dropdown options to appear
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.userMenuDropdown);
            }, newsBlogPage.mainElementsWaitTime);

            newsBlogPage.administrationOptions.first().click();
        }).then(function () {
            // wait for modal iframe to appear
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.sideMenuIframe);
            }, newsBlogPage.iframeWaitTime);

            // switch to sidebar menu iframe
            browser.switchTo().frame(browser.findElement(
                By.css('.cms_sideframe-frame iframe')));

            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.pagesLink);
            }, newsBlogPage.mainElementsWaitTime);

            newsBlogPage.pagesLink.click();

            // check if the page already exists and return the status
            return newsBlogPage.addPageLink.isPresent();
        }).then(function (present) {
            if (present === true) {
                // page is absent - create new page
                browser.wait(function () {
                    return browser.isElementPresent(newsBlogPage.addPageLink);
                }, newsBlogPage.mainElementsWaitTime);

                newsBlogPage.addPageLink.click();

                browser.wait(function () {
                    return browser.isElementPresent(newsBlogPage.titleInput);
                }, newsBlogPage.mainElementsWaitTime);

                newsBlogPage.titleInput.sendKeys('Test').then(function () {
                    newsBlogPage.saveButton.click();

                    newsBlogPage.slugErrorNotification.isPresent()
                        .then(function (present) {
                        if (present === false) {
                            browser.wait(function () {
                                return browser.isElementPresent(newsBlogPage.editPageLink);
                            }, newsBlogPage.mainElementsWaitTime);

                            // wait till the editPageLink will become clickable
                            browser.sleep(500);

                            // validate/click edit page link
                            newsBlogPage.editPageLink.click();

                            // switch to default page content
                            browser.switchTo().defaultContent();

                            browser.wait(function () {
                                return browser.isElementPresent(newsBlogPage.testLink);
                            }, newsBlogPage.mainElementsWaitTime);

                            // validate test link text
                            newsBlogPage.testLink.getText()
                                .then(function (title) {
                                expect(title).toEqual('Test');
                            });
                        }
                    });
                });
            }
        });
    });

    it('creates a new apphook config', function () {
        // check if the focus is on sidebar ifarme
        newsBlogPage.editPageLink.isPresent().then(function (present) {
            if (present === false) {
                // wait for modal iframe to appear
                browser.wait(function () {
                    return browser.isElementPresent(newsBlogPage.sideMenuIframe);
                }, newsBlogPage.iframeWaitTime);

                // switch to sidebar menu iframe
                browser.switchTo().frame(browser.findElement(By.css(
                    '.cms_sideframe-frame iframe')));
            }
        }).then(function () {
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.breadcrumbsLinks.first());
            }, newsBlogPage.mainElementsWaitTime);

            // click the Home link in breadcrumbs
            newsBlogPage.breadcrumbsLinks.first().click();

            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.newsBlogConfigsLink);
            }, newsBlogPage.mainElementsWaitTime);

            newsBlogPage.newsBlogConfigsLink.click();

            // check if the apphook config already exists and return the status
            return newsBlogPage.editConfigsLink.isPresent();
        }).then(function (present) {
            if (present === false) {
                // apphook config is absent - create new apphook config
                browser.wait(function () {
                    return browser.isElementPresent(newsBlogPage.addConfigsButton);
                }, newsBlogPage.mainElementsWaitTime);

                newsBlogPage.addConfigsButton.click();

                browser.wait(function () {
                    return browser.isElementPresent(newsBlogPage.namespaceInput);
                }, newsBlogPage.mainElementsWaitTime);

                newsBlogPage.namespaceInput.sendKeys('aldryn_newsblog')
                    .then(function () {
                    newsBlogPage.applicationTitleInput.sendKeys('Test title');
                }).then(function () {
                    newsBlogPage.saveButton.click();

                    browser.wait(function () {
                        return browser.isElementPresent(newsBlogPage.successNotification);
                    }, newsBlogPage.mainElementsWaitTime);
                });
            }
        });
    });

    it('creates a new article', function () {
        browser.wait(function () {
            return browser.isElementPresent(newsBlogPage.breadcrumbsLinks.first());
        }, newsBlogPage.mainElementsWaitTime);

        // click the Home link in breadcrumbs
        newsBlogPage.breadcrumbsLinks.first().click();

        browser.wait(function () {
            return browser.isElementPresent(newsBlogPage.addArticleButton);
        }, newsBlogPage.mainElementsWaitTime);

        newsBlogPage.addArticleButton.click();

        browser.wait(function () {
            return browser.isElementPresent(newsBlogPage.languageTabs.get(1));
        }, newsBlogPage.mainElementsWaitTime);

        newsBlogPage.languageTabs.get(1).click().then(function () {
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.titleInput);
            }, newsBlogPage.mainElementsWaitTime);

            // create random article name
            var articleName = 'Test article ' +
                (Math.floor(Math.random() * 10001));

            newsBlogPage.titleInput.sendKeys(articleName);
        }).then(function () {
            browser.actions().mouseMove(newsBlogPage.saveAndContinueButton)
                .perform();
            newsBlogPage.saveButton.click();

            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.successNotification);
            }, newsBlogPage.mainElementsWaitTime);

            // validate success notification
            expect(newsBlogPage.successNotification.isDisplayed())
                .toBeTruthy();
            // validate edit article link
            expect(newsBlogPage.editArticleLinks.first().isDisplayed())
                .toBeTruthy();
        });
    });

});

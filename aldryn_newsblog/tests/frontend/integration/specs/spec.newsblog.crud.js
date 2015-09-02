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
    var articleName = 'Test article ' + (Math.floor(Math.random() * 10001));

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

            return newsBlogPage.administrationOptions.first().click();
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

            // wait for iframe side menu to reload
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.addConfigsButton);
            }, newsBlogPage.mainElementsWaitTime);

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

                    return newsBlogPage.slugErrorNotification.isPresent();
                }).then(function (present) {
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
                return browser.switchTo().frame(browser.findElement(By.css(
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
                    return newsBlogPage.applicationTitleInput.sendKeys('Test title');
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
            return browser.isElementPresent(newsBlogPage.englishLanguageTab);
        }, newsBlogPage.mainElementsWaitTime);

        newsBlogPage.englishLanguageTab.click().then(function () {
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.titleInput);
            }, newsBlogPage.mainElementsWaitTime);

            return newsBlogPage.titleInput.sendKeys(articleName);
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

    it('adds a new article on the page', function () {
        // switch to default page content
        browser.switchTo().defaultContent();

        // add articles to the page only if they were not added before
        newsBlogPage.aldrynNewsBlogBlock.isPresent().then(function (present) {
            if (present === false) {
                // click the Page link in the top menu
                newsBlogPage.userMenus.get(1).click().then(function () {
                    // wait for top menu dropdown options to appear
                    browser.wait(function () {
                        return browser.isElementPresent(newsBlogPage.userMenuDropdown);
                    }, newsBlogPage.mainElementsWaitTime);

                    newsBlogPage.advancedSettingsOption.click();

                    // wait for modal iframe to appear
                    browser.wait(function () {
                        return browser.isElementPresent(newsBlogPage.modalIframe);
                    }, newsBlogPage.iframeWaitTime);

                    // switch to modal iframe
                    browser.switchTo().frame(browser.findElement(By.css(
                        '.cms_modal-frame iframe')));

                    cmsProtractorHelper.selectOption(newsBlogPage.applicationSelect,
                        'NewsBlog', newsBlogPage.newsBlogOption);

                    // switch to default page content
                    browser.switchTo().defaultContent();

                    browser.wait(function () {
                        return browser.isElementPresent(newsBlogPage.saveModalButton);
                    }, newsBlogPage.mainElementsWaitTime);

                    browser.actions().mouseMove(newsBlogPage.saveModalButton)
                        .perform();
                    return newsBlogPage.saveModalButton.click();
                }).then(function () {
                    // wait for aldryn-newsblog block to appear
                    browser.wait(function () {
                        return browser.isElementPresent(newsBlogPage.aldrynNewsBlogBlock);
                    }, newsBlogPage.mainElementsWaitTime);

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
        browser.wait(function () {
            return browser.isElementPresent(newsBlogPage.sideMenuIframe);
        }, newsBlogPage.iframeWaitTime);

        // switch to sidebar menu iframe
        browser.switchTo()
            .frame(browser.findElement(By.css('.cms_sideframe-frame iframe')));

        // wait for edit event link to appear
        browser.wait(function () {
            return browser.isElementPresent(newsBlogPage.editArticleLinks.first());
        }, newsBlogPage.mainElementsWaitTime);

        // validate edit article links texts to delete proper article
        newsBlogPage.editArticleLinks.first().getText().then(function (text) {
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
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.deleteButton);
            }, newsBlogPage.mainElementsWaitTime);

            browser.actions().mouseMove(newsBlogPage.saveAndContinueButton)
                .perform();
            return newsBlogPage.deleteButton.click();
        }).then(function () {
            // wait for confirmation button to appear
            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.sidebarConfirmationButton);
            }, newsBlogPage.mainElementsWaitTime);

            newsBlogPage.sidebarConfirmationButton.click();

            browser.wait(function () {
                return browser.isElementPresent(newsBlogPage.successNotification);
            }, newsBlogPage.mainElementsWaitTime);

            // validate success notification
            expect(newsBlogPage.successNotification.isDisplayed())
                .toBeTruthy();

            // switch to default page content
            browser.switchTo().defaultContent();

            // refresh the page to see changes
            browser.refresh();
        });
    });

});

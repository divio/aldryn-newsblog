'use strict';

var helpers = require('djangocms-casper-helpers');
var globals = helpers.settings;
var casperjs = require('casper');
var cms = helpers(casperjs);
var xPath = casperjs.selectXPath;

casper.test.setUp(function (done) {
    casper.start()
        .then(cms.login())
        .run(done);
});

casper.test.tearDown(function (done) {
    casper.start()
        .then(cms.logout())
        .run(done);
});

casper.test.begin('Creation / deletion of the apphook', function (test) {
    casper
        .start(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            test.assertVisible('#content', 'Admin loaded');
            this.click(
                xPath(cms.getXPathForAdminSection({
                    section: 'Aldryn News & Blog',
                    row: 'Sections',
                    link: 'Add'
                }))
            );
        })
        .waitForUrl(/add/)
        .waitUntilVisible('#newsblogconfig_form')
        .then(function () {
            test.assertVisible('#newsblogconfig_form', 'Apphook creation form loaded');

            this.fill('#newsblogconfig_form', {
                namespace: 'Test namespace',
                app_title: 'Test Blog'
            }, true);
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The Section "Test Blog" was added successfully.',
                'Apphook config was created'
            );

            test.assertElementCount(
                '#result_list tbody tr',
                2,
                'There are 2 apphooks now'
            );

            this.clickLabel('Test Blog', 'a');
        })
        .waitUntilVisible('.deletelink', function () {
            this.click('.deletelink');
        })
        .waitForUrl(/delete/, function () {
            this.click('input[value="Yes, I\'m sure"]');
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The Section "Test Blog" was deleted successfully.',
                'Apphook config was deleted'
            );
        })
        .run(function () {
            test.done();
        });
});

cms._modifyPageAdvancedSettings = function _modifyPageAdvancedSettings(opts) {
    var that = this;

    return function () {
        return this.wait(1000).thenOpen(globals.adminPagesUrl)
            .waitUntilVisible('.cms-pagetree-jstree')
            .then(that.waitUntilAllAjaxCallsFinish())
            .then(that.expandPageTree())
            .then(function () {
                var pageId = that.getPageId(opts.page);

                this.thenOpen(globals.adminPagesUrl + pageId + '/advanced-settings/');
            })
            .waitForSelector('#page_form', function () {
                this.fill('#page_form', opts.fields);
            })
            .wait(100, function () {
                this.click('input.default');
            })
            .waitForUrl(/page/)
            .waitUntilVisible('.success')
            .then(that.waitUntilAllAjaxCallsFinish())
            .wait(1000);
    };
};

casper.test.begin('Creation / deletion of the article', function (test) {
    casper
        .start()
        .then(cms.addPage({ title: 'Blog' }))
        .then(cms._modifyPageAdvancedSettings({
            page: 'Blog',
            fields: {
                application_configs: 1,
                application_urls: 'NewsBlogApp'
            }
        }))
        .then(cms.publishPage({
            page: 'Blog'
        }))
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText('p', 'No items available', 'No articles yet');
        })
        .thenOpen(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            test.assertVisible('#content', 'Admin loaded');
            this.click(
                xPath(cms.getXPathForAdminSection({
                    section: 'Aldryn News & Blog',
                    row: 'Articles',
                    link: 'Add'
                }))
            );
        })
        .waitForUrl(/add/)
        .waitUntilVisible('#article_form')
        .then(function () {
            test.assertVisible('#article_form', 'Article creation form loaded');

            this.fill('#article_form', {
                title: 'Test article'
            }, true);
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The article "Test article" was added successfully.',
                'Article was created'
            );

            test.assertElementCount(
                '#result_list tbody tr',
                1,
                'There is 1 article available'
            );
        })
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText(
                '.article.unpublished h2 a',
                'Test article',
                'Article is available on the page'
            );
        })
        .thenOpen(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            this.click(
                xPath(cms.getXPathForAdminSection({
                    section: 'Aldryn News & Blog',
                    row: 'Articles'
                }))
            );
        })
        .waitForUrl(/article/, function () {
            this.clickLabel('Test article', 'a');
        })
        .waitUntilVisible('.deletelink', function () {
            this.click('.deletelink');
        })
        .waitForUrl(/delete/, function () {
            this.click('input[value="Yes, I\'m sure"]');
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The article "Test article" was deleted successfully.',
                'Article was deleted'
            );
        })
        .then(cms.removePage())
        .run(function () {
            test.done();
        });
});

casper.test.begin('Latest articles plugin', function (test) {
    casper
        .start()
        .then(cms.addPage({ title: 'Home' }))
        .then(cms.addPlugin({
            type: 'NewsBlogLatestArticlesPlugin',
            content: {
                id_latest_articles: 1
            }
        }))
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText(
                'p.cms-plugin',
                'No items available',
                'No articles yet'
            );
        })
        .then(cms.openSideframe())
        // add articles
        .withFrame(0, function () {
            this.waitForSelector('.cms-pagetree-breadcrumbs')
                .then(function () {
                    this.click('.cms-pagetree-breadcrumbs a:first-child');
                })
                .waitForUrl(/admin/)
                .waitForSelector('.dashboard', function () {
                    this.click(xPath(cms.getXPathForAdminSection({
                        section: 'Aldryn News & Blog',
                        row: 'Articles',
                        link: 'Add'
                    })));
                })
                .waitForSelector('#article_form', function () {
                    this.fill('#article_form', {
                        title: 'First article'
                    }, false);

                })
                // wait 3 seconds so the second article is definitely
                // created after the first one :)
                .wait(3000, function () {
                    this.click('input[value="Save and add another"]');
                })
                .waitForSelector('.success', function () {
                    test.assertSelectorHasText(
                        '.success',
                        'The article "First article" was added successfully. You may add another article below.',
                        'First article added'
                    );

                    this.fill('#article_form', {
                        title: 'Second article'
                    }, true);
                })
                .waitForSelector('.success');
        })
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText(
                'p.cms-plugin',
                'No items available',
                'Still no articles yet (no apphooked page yet)'
            );
        })
        .then(cms.addPage({ title: 'Blog' }))
        .then(cms.addApphookToPage({
            page: 'Blog',
            apphook: 'NewsBlogApp'
        }))
        .then(cms.publishPage({ page: 'Blog' }))
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText(
                '.article h2 a cms-plugin',
                'Second article',
                'Latest article is visible on the page'
            );
            test.assertElementCount(
                '.article cms-plugin',
                1,
                'Only one latest article is visible on the page'
            );
        })
        // remove articles
        .then(cms.openSideframe())
        .withFrame(0, function () {
            this.waitForSelector('.cms-pagetree-breadcrumbs')
                .then(function () {
                    this.click('.cms-pagetree-breadcrumbs a:first-child');
                })
                .waitForUrl(/admin/)
                .waitForSelector('.dashboard', function () {
                    this.click(xPath(cms.getXPathForAdminSection({
                        section: 'Aldryn News & Blog',
                        row: 'Articles'
                    })));
                })
                .waitForSelector('#changelist-form', function () {
                    this.click('th input[type="checkbox"]');
                    this.fill('#changelist-form', {
                        action: 'delete_selected'
                    }, true);

                })
                .waitForSelector('.delete-confirmation', function () {
                    this.click('input[value="Yes, I\'m sure"]');
                })
                .waitForSelector('.success', function () {
                    test.assertSelectorHasText(
                        '.success',
                        'Successfully deleted 2 articles.',
                        'Articles deleted'
                    );
                });
        })
        .then(cms.removePage())
        .then(cms.removePage())
        .run(function () {
            test.done();
        });
});

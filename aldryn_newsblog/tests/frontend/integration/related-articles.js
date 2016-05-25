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

casper.test.begin('Related articles', function (test) {
    casper
        .then(cms.addPage({ title: 'Home' }))
        .thenOpen(globals.editUrl)
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
                    test.assertDoesntExist('.field-related .add-related', 'Related articles "Add" are not shown');

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

                    test.assertDoesntExist('.field-related .add-related', 'Related articles "Add" are not shown');
                    test.assertSelectorHasText(
                        '.sortedm2m',
                        'First article',
                        'Correct related articles possibilities are shown'
                    );

                    this.fill('#article_form', {
                        title: 'Second article'
                    }, true);
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
        .run(function () {
            test.done();
        });
});

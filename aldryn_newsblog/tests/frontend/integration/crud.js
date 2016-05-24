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

/**
 * Returns xpath expression to find the "Add" link corresponding
 * to the specific row in the admin.
 *
 * @function generateXPathForAddLink
 * @param {Object} options
 * @param {String} options.section module name, e.g. Django CMS
 * @param {String} options.row module row, e.g Pages, Users
 */
var generateXPathForAddLink = function (options) {
    var section = options.section;
    var row = options.row;
    var xpath = '//div[.//caption/a[contains(text(), "' + section + '")]]';

    xpath += '//th[./a[contains(text(), "' + row + '")]]';
    xpath += '/following-sibling::td/a[contains(text(), "Add")]';

    return xpath;
};

casper.test.begin('Creation / deletion of the apphook', function (test) {
    casper
        .start(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            test.assertVisible('#content', 'Admin loaded');
            this.click(
                xPath(generateXPathForAddLink({
                    section: 'Aldryn News & Blog',
                    row: 'Application configurations'
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
                'The application configuration "NewsBlog / Test namespace" was added successfully.',
                'Apphook config was created'
            );

            test.assertElementCount(
                '#result_list tbody tr',
                2,
                'There are 2 apphooks now'
            );

            this.clickLabel('NewsBlog / Test namespace', 'a');
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
                'The application configuration "NewsBlog / Test namespace" was deleted successfully.',
                'Apphook config was deleted'
            );
        })
        .run(function () {
            test.done();
        });
});

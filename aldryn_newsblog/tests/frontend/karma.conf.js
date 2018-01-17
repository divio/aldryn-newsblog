/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';

// #############################################################################
// CONFIGURATION
module.exports = function (config) {
    var browsers = {
        PhantomJS: 'used for local testing'
    };

    var settings = {
        // base path that will be used to resolve all patterns (eg. files, exclude)
        basePath: '..',

        // frameworks to use
        // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
        frameworks: ['jasmine', 'fixture'],

        // list of files / patterns to load in the browser
        // tests/${path}
        files: [
            // these have to be specified in order since
            // dependency loading is not handled yet
            '../../aldryn_newsblog/boilerplates/bootstrap3/static/js/libs/*.js',
            '../../aldryn_newsblog/boilerplates/bootstrap3/static/js/addons/*.js',

            // tests themselves
            'frontend/unit/*.js',

            // fixture patterns
            {
                pattern: 'frontend/fixtures/**/*'
            }
        ],

        // list of files to exclude
        exclude: [],

        // preprocess matching files before serving them to the browser
        // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
        preprocessors: {
            '../../aldryn_newsblog/boilerplates/bootstrap3/static/js/addons/*.js': ['coverage'],
            // for fixtures
            '**/*.html': ['html2js'],
            '**/*.json': ['json_fixtures']
        },

        // optionally, configure the reporter
        coverageReporter: {
            reporters: [
                { type: 'html', dir: 'frontend/coverage/' },
                { type: 'lcov', dir: 'frontend/coverage/' }
            ]
        },

        // fixtures dependency
        // https://github.com/billtrik/karma-fixture
        jsonFixturesPreprocessor: {
            variableName: '__json__'
        },

        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ['progress', 'coverage'],

        // web server port
        port: 9876,

        // enable / disable colors in the output (reporters and logs)
        colors: true,

        // level of logging
        // possible values:
        // config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,

        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: true,

        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: Object.keys(browsers),

        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: false
    };

    config.set(settings);
};

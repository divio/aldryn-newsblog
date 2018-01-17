/* eslint strict: [2, "global"] */
/**
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';

// #############################################################################
// IMPORTS
var gulp = require('gulp');
var gutil = require('gulp-util');
var KarmaServer = require('karma').Server;
var eslint = require('gulp-eslint');
var integrationTests = require('djangocms-casper-helpers/gulp');
var path = require('path');
var child_process = require('child_process');

var argv = require('minimist')(process.argv.slice(2)); // eslint-disable-line

// #############################################################################
// SETTINGS
var PROJECT_ROOT = __dirname;
var PROJECT_PATH = {
    js: PROJECT_ROOT + '/aldryn_newsblog/boilerplates/bootstrap3/static/js/',
    tests: PROJECT_ROOT + '/aldryn_newsblog/tests/frontend'
};

var PROJECT_PATTERNS = {
    lint: [
        PROJECT_PATH.js + '/addons/*.js',
        PROJECT_PATH.tests + '/**/*.js',
        '!' + PROJECT_PATH.tests + '/coverage/**/*.js',
        PROJECT_ROOT + '/gulpfile.js'
    ]
};

var INTEGRATION_TESTS = [
    [
        'crud',
        'related-articles'
    ]
];


// #############################################################################
// LINTING
gulp.task('lint', function () {
    // DOCS: http://eslint.org
    return gulp.src(PROJECT_PATTERNS.lint)
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

// #########################################################
// TESTS
gulp.task('tests', ['tests:unit', 'tests:lint', 'tests:integration']);
gulp.task('tests:lint', ['lint']);
gulp.task('tests:unit', function (done) {
    var server = new KarmaServer({
        configFile: PROJECT_PATH.tests + '/karma.conf.js',
        singleRun: true
    }, done);

    server.start();
});

// gulp tests:integration [--clean] [--screenshots] [--tests=loginAdmin,toolbar]
var pathToBin = child_process.execSync('npm bin').toString().trim();
var pathToCasper = path.join(pathToBin, 'casperjs');

gulp.task('tests:integration', integrationTests({
    tests: INTEGRATION_TESTS,
    pathToTests: PROJECT_PATH.tests,
    argv: argv,
    dbPath: 'local.sqlite',
    serverCommand: 'test_settings.py server',
    logger: gutil.log.bind(gutil),
    waitForMigrations: 120,
    pathToCasper: pathToCasper
}));


gulp.task('tests:unit:watch', function () {
    var server = new KarmaServer({
        configFile: PROJECT_PATH.tests + '/karma.conf.js'
    });

    server.start();
});

// #############################################################################
// COMMANDS
gulp.task('default', ['lint']);

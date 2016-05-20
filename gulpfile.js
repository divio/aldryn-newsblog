/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';

// #############################################################################
// IMPORTS
var gulp = require('gulp');
var gutil = require('gulp-util');
var KarmaServer = require('karma').Server;
var jshint = require('gulp-jshint');
var jscs = require('gulp-jscs');
var integrationTests = require('djangocms-casper-helpers/gulp');

var argv = require('minimist')(process.argv.slice(2)); // eslint-disable-line

// #############################################################################
// SETTINGS
var PROJECT_ROOT = __dirname;
var PROJECT_PATH = {
    'js': PROJECT_ROOT + '/aldryn_newsblog/boilerplates/bootstrap3/static/js/',
    'tests': PROJECT_ROOT + '/aldryn_newsblog/tests/frontend'
};

var PROJECT_PATTERNS = {
    'lint': [
        PROJECT_PATH.js + '/addons/*.js',
        PROJECT_PATH.tests + '/**/*.js',
        '!' + PROJECT_PATH.tests + '/coverage/**/*.js',
        PROJECT_ROOT + '/gulpfile.js'
    ]
};

var INTEGRATION_TESTS = [
    [
        'loginAdmin'
    ]
];


// #############################################################################
// LINTING
gulp.task('lint', function () {
    return gulp.src(PROJECT_PATTERNS.lint)
        .pipe(jshint())
        .pipe(jscs())
        .on('error', function (error) {
            gutil.log('\n' + error.message);
            if (process.env.CI) {
                // force the process to exit with error code
                process.exit(1);
            }
        })
        .pipe(jshint.reporter('jshint-stylish'));
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

var child_process = require('child_process');
var spawn = require('child_process').spawn;
// gulp tests:integration [--clean] [--screenshots] [--tests=loginAdmin,toolbar]
gulp.task('tests:integration', integrationTests({
    child_process: child_process,
    spawn: spawn,
    tests: INTEGRATION_TESTS,
    pathToTests: PROJECT_PATH.tests,
    argv: argv,
    dbPath: 'local.sqlite',
    serverCommand: 'test_settings.py server',
    logger: gutil.log.bind(gutil)
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

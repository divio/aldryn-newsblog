/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';

// #############################################################################
// IMPORTS
var gulp = require('gulp');
var gutil = require('gulp-util');
var karma = require('karma').server;
var protractor = require('gulp-protractor').protractor;
var jshint = require('gulp-jshint');
var jscs = require('gulp-jscs');
var webdriverUpdate = require('gulp-protractor').webdriver_update;
var SauceTunnel = require('sauce-tunnel');
var tunnel;

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
        PROJECT_PATH.tests + '/*.js',
        PROJECT_PATH.tests + '/unit/*.js',
        PROJECT_PATH.tests + '/integration/*.js',
        PROJECT_ROOT + '/gulpfile.js'
    ]
};

var PORT = parseInt(process.env.PORT, 10) || 8000;

// #############################################################################
// LINTING
gulp.task('lint', function () {
    return gulp.src(PROJECT_PATTERNS.lint)
        .pipe(jshint())
        .pipe(jscs())
        .on('error', function (error) {
            gutil.log('\n' + error.message);
            if (process.env.CI) {
                // Force the process to exit with error code
                process.exit(1);
            }
        })
        .pipe(jshint.reporter('jshint-stylish'));
});

// #############################################################################
// TESTS
gulp.task('tests', ['tests:unit', 'tests:lint', 'tests:integration']);
gulp.task('tests:lint', ['lint']);
gulp.task('tests:unit', function (done) {
    // run javascript tests
    karma.start({
        configFile: PROJECT_PATH.tests + '/karma.conf.js',
        singleRun: true
    }, done);
});

gulp.task('tests:sauce:start', function (done) {
    if (!process.env.CI) {
        done();
        return;
    }
    tunnel = new SauceTunnel(
        process.env.SAUCE_USERNAME,
        process.env.SAUCE_ACCESS_KEY,
        process.env.TRAVIS_JOB_NUMBER
    );

    tunnel.start(function (isCreated) {
        if (!isCreated) {
            done('Failed to create Sauce tunnel.');
        }
        console.log('Connected to Sauce Labs.');
        done();
    });
});

gulp.task('tests:sauce:end', function (done) {
    if (!process.env.CI) {
        done();
        return;
    }
    tunnel.stop(function () {
        console.log('Stopping the server.');
        done();
    });
});

gulp.task('tests:webdriver', webdriverUpdate);
gulp.task('tests:integration', ['tests:webdriver', 'tests:sauce:start'], function () {
    return gulp.src([PROJECT_PATH.tests + '/integration/specs/*.js'])
        .pipe(protractor({
            configFile: PROJECT_PATH.tests + '/protractor.conf.js',
            args: ['--baseUrl', 'http://127.0.0.1:' + PORT]
        }))
        .on('error', function (error) {
            gutil.log(gutil.colors.red(
                'Error (' + error.plugin + '): ' + error.message
            ));
        })
        .on('end', function () {
            gulp.run('tests:sauce:end');
        });
});

gulp.task('tests:watch', function () {
    // run javascript tests
    karma.start({
        configFile: PROJECT_PATH.tests + '/karma.conf.js'
    });
});

// #############################################################################
// COMMANDS
gulp.task('default', ['lint']);

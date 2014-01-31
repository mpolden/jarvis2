/* jshint node: true, strict: false */

var gulp = require('gulp');
var jshint = require('gulp-jshint');
var less = require('gulp-less');

var paths = {
  js: ['gulpfile.js', 'app/static/js/app/*.js', 'app/static/widgets/*/*.js'],
  less: ['app/static/**/*.less']
};

gulp.task('lint', function() {
  return gulp.src(paths.js)
    .pipe(jshint('.jshintrc'))
    .pipe(jshint.reporter('default'));
});

gulp.task('less', function () {
  return gulp.src(paths.less)
    .pipe(less())
    .pipe(gulp.dest('app/static/'));
});

gulp.task('watch', function () {
  // Watch all JS files, except gulpfile.js
  gulp.watch(paths.js.slice(1), ['lint']);
  gulp.watch(paths.less, ['less']);
});

gulp.task('default', ['lint', 'less']);

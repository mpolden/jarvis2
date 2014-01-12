/* jshint node: true, strict: false */

var gulp = require('gulp');
var jshint = require('gulp-jshint');
var less = require('gulp-less');

var jsFiles = ['gulpfile.js', 'app/static/js/app/*.js',
               'app/static/widgets/*/*.js'];
var lessFiles = ['app/static/**/*.less'];

gulp.task('lint', function() {
  gulp.src(jsFiles)
    .pipe(jshint('.jshintrc'))
    .pipe(jshint.reporter('default'));
});

gulp.task('less', function () {
  gulp.src(lessFiles)
    .pipe(less())
    .pipe(gulp.dest('app/static/'));
});

gulp.task('watch', function () {
  // Watch all JS files, except gulpfile.js
  gulp.watch(jsFiles.slice(1), function () {
    gulp.run('lint');
  });

  gulp.watch(lessFiles, function () {
    gulp.run('less');
  });
});

gulp.task('default', function() {
  gulp.run('lint', 'less');
});

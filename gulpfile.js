/* jshint node: true, strict: false */

var gulp = require('gulp');
var jshint = require('gulp-jshint');
var less = require('gulp-less');
var concat = require('gulp-concat');

var paths = {
  src: {
    js: ['app/static/js/app/*.js', 'app/static/widgets/*/*.js'],
    less: ['app/static/**/*.less']
  },
  vendor: {
    css: ['node_modules/gridster/dist/jquery.gridster.min.css',
          'node_modules/normalize-css/normalize.css',
          'node_modules/rickshaw/rickshaw.min.css'],
    js: ['node_modules/angular/lib/angular.min.js',
         'node_modules/angular-truncate/src/truncate.js',
         'node_modules/d3/d3.min.js',
         'node_modules/jquery/dist/jquery.min.js',
         'node_modules/gridster/dist/jquery.gridster.min.js',
         'node_modules/moment/min/moment-with-langs.min.js',
         'node_modules/rickshaw/rickshaw.min.js',
         'node_modules/gauge/dist/gauge.min.js']
  }
};

gulp.task('lint', function() {
  return gulp.src(paths.src.js.concat('gulpfile.js'))
    .pipe(jshint('.jshintrc'))
    .pipe(jshint.reporter('default'));
});

gulp.task('less', function () {
  return gulp.src(paths.src.less)
    .pipe(less())
    .pipe(gulp.dest('app/static/'));
});

gulp.task('bundle-js', function() {
  gulp.src(paths.vendor.js)
    .pipe(concat('bundle.js'))
    .pipe(gulp.dest('app/static/vendor/'));
});

gulp.task('bundle-css', function() {
  gulp.src(paths.vendor.css)
    .pipe(concat('bundle.css'))
    .pipe(gulp.dest('app/static/vendor/'));
});

gulp.task('watch', function () {
  gulp.watch(paths.src.js, ['lint']);
  gulp.watch(paths.src.less, ['less']);
});

gulp.task('default', ['lint', 'less', 'bundle-js', 'bundle-css']);

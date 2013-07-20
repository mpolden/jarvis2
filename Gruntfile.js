/* jshint node: true, camelcase: false */

module.exports = function (grunt) {

  'use strict';

  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-jsbeautifier');

  var less_files = {};
  grunt.file.recurse('app/static',
    function (abspath, rootdir, subdir, filename) {
      if (grunt.file.isMatch('*.less', filename)) {
        less_files[abspath.replace(/\.less$/, '.css')] = abspath;
      }
    });

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    bower: {
      install: {
        options: {
          targetDir: './app/static',
          cleanBowerDir: true
        }
      }
    },
    jshint: {
      options: {
        bitwise: false,
        camelcase: true,
        curly: true,
        eqeqeq: true,
        es3: false,
        forin: true,
        immed: true,
        indent: 2,
        latedef: true,
        newcap: true,
        noarg: true,
        noempty: true,
        nonew: true,
        plusplus: true,
        quotmark: 'single',
        undef: true,
        unused: true,
        strict: true,
        trailing: true,
        maxparams: 5,
        maxdepth: 5,
        maxstatements: 20,
        maxcomplexity: 5,
        maxlen: 80
      },
      uses_defaults: 'Gruntfile.js',
      with_overrides: {
        options: {
          browser: true,
          globals: {
            angular: true,
            $: true,
            EventSource: true,
            Rickshaw: true
          }
        },
        files: {
          src: [
            'app/static/js/app/*.js',
            'app/static/widgets/*/*.js'
          ]
        }
      }
    },
    watch: {
      scripts: {
        files: [
          'app/static/js/app/*.js',
          'app/static/widgets/*/*.js',
          'app/static/widgets/*/*.less'
        ],
        tasks: ['jshint', 'less']
      }
    },
    jsbeautifier: {
      files: [
        'Gruntfile.js',
        'app/static/js/app/*.js',
        'app/static/widgets/*/*.js'
      ],
      options: {
        indent_size: 2,
        jslint_happy: true
      }
    },
    less: {
      development: {
        files: less_files
      }
    },
    uglify: {
      dist: {
        files: {
          'app/static/js/jquery-knob/jquery.knob.min.js': [
            'app/static/js/jquery-knob/jquery.knob.js'
          ]
        }
      }
    }
  });

  grunt.registerTask('hint', 'jshint');
  grunt.registerTask('build', ['bower', 'jsbeautifier', 'jshint', 'less']);
  grunt.registerTask('default', ['jsbeautifier', 'jshint', 'less']);
};

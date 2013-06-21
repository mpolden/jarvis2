module.exports = function (grunt) {

  'use strict';

  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    bower: {
      install: {
        options: {
          targetDir: './static',
          cleanBowerDir: true
        }
      }
    },
    jshint: {
      all: ['Gruntfile.js', 'static/js/app/*.js', 'static/widgets/*/*.js'],
      options: {
        curly: true,
        eqeqeq: true,
        forin: true,
        immed: true,
        indent: 2,
        latedef: true,
        newcap: true,
        noarg: true,
        noempty: true,
        nonew: true,
        quotmark: 'single',
        undef: true,
        unused: true,
        strict: true,
        trailing: true,
        maxdepth: 5,
        node: true,
        globals: {
          angular: true,
          $: true,
          EventSource: true
        }
      },
    },
    watch: {
      scripts: {
        files: ['static/js/*.js', 'widgets/*/*.js'],
        tasks: ['default'],
      }
    }
  });

  grunt.registerTask('default', 'jshint');
};

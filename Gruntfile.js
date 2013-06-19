module.exports = function (grunt) {

  'use strict';

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.initConfig({
    jshint: {
      all: ['Gruntfile.js', 'static/js/*.js', 'static/widgets/*/*.js'],
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
        globalstrict: true,
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

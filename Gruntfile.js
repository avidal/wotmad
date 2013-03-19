module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    watch: {
      less: {
        files: 'wotmad/assets/less/style.less',
        tasks: 'less'
      }
    },

    less: {
      production: {
        files: {
          "wotmad/assets/css/style.css": "wotmad/assets/less/style.less"
        }
      }
    }

  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['less']);

};

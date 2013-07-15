/**
 * Angular Truncate - Ellipsis for your templates
 * @version v0.1.0 - 2013-07-15
 * @link http://sparkalow.github.com/angular-truncate
 * @author Brian Mathews (sparkalow)
 * @license MIT License, http://www.opensource.org/licenses/MIT
 */
angular.module("truncate",[]).filter("characters",function(){return function(a,b,c){if(isNaN(b))return a;if(0>=b)return"";if(a&&a.length>=b){if(a=a.substring(0,b),c)for(;" "===a.charAt(a.length-1);)a=a.substr(0,a.length-1);else{var d=a.lastIndexOf(" ");-1!==d&&(a=a.substr(0,d))}return a+"..."}return a}}).filter("words",function(){return function(a,b){if(isNaN(b))return a;if(0>=b)return"";if(a){var c=a.split(/\s+/);c.length>b&&(a=c.slice(0,b).join(" ")+"...")}return a}});
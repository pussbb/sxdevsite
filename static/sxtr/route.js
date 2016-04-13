// Generated by CoffeeScript 1.10.0
(function() {
  var AuthorizedUserResolver, GuestOnlyResolver, LogOutResolver, PAGE_URL, config, pageUrl;

  PAGE_URL = window.location.origin + "/static/sxtr/pages";

  pageUrl = function(name) {
    return PAGE_URL + "/" + name;
  };

  LogOutResolver = function($q, $location, Auth, $route) {
    Auth.logout().then(function() {
      return $location.path('/');
    });
    return $q.reject();
  };

  LogOutResolver.$inject = ['$q', '$location', 'Auth', '$route'];

  GuestOnlyResolver = function($q, $location, Auth) {
    Auth.initialized.promise.then(function() {
      if (Auth.isAuthorized()) {
        $q.reject();
        return $location.path('forbidden', $location);
      }
    });
    return $q.resolve();
  };

  GuestOnlyResolver.$inject = ['$q', '$location', 'Auth'];

  AuthorizedUserResolver = function($q, $location, Auth, $route) {
    Auth.initialized.promise.then(function() {
      if (!Auth.isAuthorized()) {
        $q.reject();
        return $location.path('login');
      }
    });
    return $q.resolve();
  };

  AuthorizedUserResolver.$inject = ['$q', '$location', 'Auth'];

  config = function($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider.when('/', {
      title: 'Index',
      templateUrl: pageUrl("index.html"),
      controller: 'mainController',
      resolve: {
        translations: function($q, Requests) {
          return Requests.get('translations');
        }
      }
    }).when('/forbidden', {
      title: 'Access Denied',
      templateUrl: pageUrl("home.html"),
      controller: 'accessDeniedController'
    }).when('/login', {
      title: 'Login',
      templateUrl: pageUrl("auth/login.html"),
      controller: 'loginController',
      resolve: {
        guestOnly: GuestOnlyResolver
      }
    }).when('/reset_password', {
      title: 'Reset password',
      templateUrl: pageUrl("auth/reset_pswd.html"),
      controller: 'resetPasswordController',
      resolve: {
        guestOnly: GuestOnlyResolver
      }
    }).when('/logout', {
      title: 'logout',
      template: '',
      resolve: {
        auth: LogOutResolver
      }
    }).when('/profile', {
      title: 'User Details',
      templateUrl: pageUrl("auth/profile.html"),
      controller: 'profileController',
      resolve: {
        auth: AuthorizedUserResolver,
        currentUser: function(Auth) {
          return Auth.initialized.promise.then(function() {
            return Auth.currentUser();
          });
        }
      }
    }).when('/change_password', {
      title: 'Change Password',
      templateUrl: pageUrl("auth/change_pswd.html"),
      controller: 'changePasswordController',
      resolve: {
        auth: AuthorizedUserResolver
      }
    }).when('/register', {
      title: 'Register',
      templateUrl: pageUrl("auth/register.html"),
      controller: 'registerController',
      resolve: {
        guestOnly: GuestOnlyResolver
      }
    }).when('/about', {
      title: 'About',
      templateUrl: pageUrl("home.html"),
      controller: 'aboutController'
    }).when('/translation/:id', {
      title: 'About',
      templateUrl: pageUrl("translation.html"),
      controller: 'translationController'
    }).when('/new_translation', {
      title: 'Add new translation',
      templateUrl: pageUrl("new_translation.html"),
      controller: 'newTranslationController',
      resolve: {
        locales: function($q, Requests) {
          return Requests.get('locales');
        },
        applications: function($q, Requests) {
          return Requests.get('apps');
        },
        auth: AuthorizedUserResolver
      }
    }).when('/contact', {
      title: 'Contact',
      templateUrl: pageUrl("contact.html"),
      controller: 'contactController',
      resolve: {
        currentUser: function(Auth) {
          return Auth.initialized.promise.then(function() {
            return Auth.currentUser();
          });
        }
      }
    }).otherwise({
      redirectTo: '/'
    });
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    return $httpProvider.interceptors.push('AuthInterceptor');
  };

  angular.module('sxTrApp').config(config);

}).call(this);

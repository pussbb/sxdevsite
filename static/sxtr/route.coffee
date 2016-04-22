PAGE_URL = "#{window.location.origin}/static/sxtr/pages"

pageUrl = (name) ->
  "#{PAGE_URL}/#{name}"

LogOutResolver = ($q, $location, Auth, $route) ->
  Auth.logout().then -> $location.path '/'
  $q.reject()

LogOutResolver.$inject = ['$q', '$location', 'Auth', '$route']

GuestOnlyResolver = ($q, $location, Auth) ->
  Auth.initialized.promise.then ->
    if Auth.isAuthorized()
      $q.reject()
      $location.path 'forbidden', $location
  $q.resolve()
GuestOnlyResolver.$inject = ['$q', '$location', 'Auth']


AuthorizedUserResolver = ($q, $location, Auth, $route) ->
  Auth.initialized.promise.then ->
    if not Auth.isAuthorized()
        $q.reject()
        $location.path 'login'
  $q.resolve()
AuthorizedUserResolver.$inject = ['$q', '$location', 'Auth']

config = ($routeProvider, $locationProvider, $httpProvider, $compileProvider) ->
  $routeProvider
    .when '',
      title: 'Index'
      templateUrl: pageUrl("index.html")
      controller: 'mainController'
      resolve:
        translations: ($q, Requests)->
          return Requests.get 'translations'
    .when '/',
      title: 'Index'
      templateUrl: pageUrl("index.html")
      controller: 'mainController'
      resolve:
        translations: ($q, Requests)->
          return Requests.get 'translations'
    .when '/forbidden',
      title: 'Access Denied'
      templateUrl: pageUrl("home.html")
      controller: 'accessDeniedController'
    .when '/login',
      title: 'Login'
      templateUrl : pageUrl("auth/login.html")
      controller: 'loginController'
      resolve:
        guestOnly: GuestOnlyResolver
    .when '/reset_password',
      title: 'Reset password'
      templateUrl : pageUrl("auth/reset_pswd.html")
      controller: 'resetPasswordController'
      resolve:
        guestOnly: GuestOnlyResolver
    .when '/logout',
      title: 'logout'
      template: ''
      resolve:
        auth: LogOutResolver
    .when '/profile',
      title: 'User Details'
      templateUrl : pageUrl("auth/profile.html")
      controller: 'profileController'
      resolve:
        auth: AuthorizedUserResolver
        currentUser : (Auth)->
          Auth.initialized.promise.then -> Auth.currentUser()
    .when '/change_password',
      title: 'Change Password'
      templateUrl : pageUrl("auth/change_pswd.html")
      controller: 'changePasswordController'
      resolve:
        auth: AuthorizedUserResolver
    .when '/register',
      title: 'Register'
      templateUrl: pageUrl("auth/register.html")
      controller: 'registerController'
      resolve:
        guestOnly: GuestOnlyResolver
    .when '/about',
      title: 'About'
      templateUrl: pageUrl("home.html")
      controller: 'aboutController'
    .when '/translation/:id',
      title: 'Translation'
      templateUrl: pageUrl("translation.html")
      controller: 'translationController'
    .when '/new_translation',
      title: 'Add new translation'
      templateUrl: pageUrl("new_translation.html")
      controller: 'newTranslationController'
      resolve:
        locales: ($q, Requests)->
          return Requests.get 'locales'
        applications: ($q, Requests)->
          return Requests.get 'apps'
        auth: AuthorizedUserResolver
    .when '/contact',
      title: 'Contact'
      templateUrl: pageUrl("contact.html")
      controller: 'contactController'
      resolve:
        currentUser : (Auth)->
          Auth.initialized.promise.then ->
            Auth.currentUser()
    .otherwise
      redirectTo: '/'

    $httpProvider.defaults.xsrfCookieName = 'csrftoken'
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
    $httpProvider.interceptors.push 'AuthInterceptor'
    $compileProvider.debugInfoEnabled(false);

angular
  .module 'sxTrApp'
  .config(config)
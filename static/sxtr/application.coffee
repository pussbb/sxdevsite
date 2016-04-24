

sxTrApp = angular
  .module 'sxTrApp', ['ngRoute', 'ngCookies']
  .constant 'USER_ROLES',
    all : '*',
    admin : 'admin',
    editor : 'editor',
    guest : 'guest'
  .constant 'AUTH_EVENTS',
    loginSuccess : 'auth-login-success',
    loginFailed : 'auth-login-failed',
    logoutSuccess : 'auth-logout-success',
    sessionTimeout : 'auth-session-timeout',
    notAuthenticated : 'auth-not-authenticated',
    notAuthorized : 'auth-not-authorized'


sxTrApp.run ($rootScope, $http, $injector, $route, Auth, AUTH_EVENTS)->

  Auth.init().then -> $rootScope.auth = Auth

  $rootScope.pageLoading = false
  $rootScope.failedChangeRoute = false

  $rootScope.$on '$routeChangeSuccess', (event, current, previous) =>
    $rootScope.pageLoading = false
    $rootScope.pageTitle = current.title

  $rootScope.$on '$routeChangeError', ->
    $rootScope.failedChangeRoute = true
    $rootScope.pageLoading = false

  $rootScope.$on '$routeChangeStart', (event, current, previous, $location)->
    $rootScope.failedChangeRoute = false
    $rootScope.pageLoading = true
    return unless current?.access?.restricted
    if not Auth.loggedIn()
      event.preventDefault()
      $rootScope.$broadcast AUTH_EVENTS.notAuthenticated

  ###
  $rootScope.$on '$routeChangeStart', (event, current, previous, $location)->
    return unless current?.access?.restricted
    if not Auth.loggedIn()
      event.preventDefault()
      $rootScope.$broadcast AUTH_EVENTS.notAuthenticated

  $rootScope.$on AUTH_EVENTS.notAuthenticated, ()->
    console.log arguments

  $rootScope.$on(AUTH_EVENTS.notAuthorized, showNotAuthorized)
  $rootScope.$on(AUTH_EVENTS.notAuthenticated, showLoginDialog)
  $rootScope.$on(AUTH_EVENTS.sessionTimeout, showLoginDialog)
  $rootScope.$on(AUTH_EVENTS.logoutSuccess, showLoginDialog)
  $rootScope.$on(AUTH_EVENTS.loginSuccess, setCurrentUser)

  console.log $route
  $rootScope.$on '$routeChangeStart', (event, current, previous)->
    return unless current?.access?.restricted
    console.log current
    if not Auth.loggedIn()
      $rootScope.$broadcast AUTH_EVENTS.notAuthenticated

    #  and
  ###
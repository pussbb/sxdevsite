
AuthInterceptor = ($rootScope, $q, Session, AUTH_EVENTS)->
  responseError: (response)->
    $rootScope.$broadcast {
      401 : AUTH_EVENTS.notAuthenticated,
      403 : AUTH_EVENTS.notAuthorized,
      419 : AUTH_EVENTS.sessionTimeout,
      440 : AUTH_EVENTS.sessionTimeout
    }[response.status], response
    $q.reject response

AuthInterceptor.$inject = [ '$rootScope', '$q', 'Session', 'AUTH_EVENTS']

angular
  .module 'sxTrApp'
  .factory 'AuthInterceptor', AuthInterceptor
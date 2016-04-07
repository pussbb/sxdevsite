

AccessDeniedController = ($scope)->
  $scope.title = 'Access Denied'
  $scope.message = 'You does not have permissions to this page'

angular
  .module 'sxTrApp'
  .controller 'accessDeniedController', AccessDeniedController
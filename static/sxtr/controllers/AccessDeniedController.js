// Generated by CoffeeScript 1.10.0
(function() {
  var AccessDeniedController;

  AccessDeniedController = function($scope) {
    $scope.title = 'Access Denied';
    return $scope.message = 'You does not have permissions to this page';
  };

  angular.module('sxTrApp').controller('accessDeniedController', AccessDeniedController);

}).call(this);
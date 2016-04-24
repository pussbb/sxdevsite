// Generated by CoffeeScript 1.10.0
(function() {
  var AboutController, AccessDeniedController, ContactController;

  AboutController = function($scope) {
    $scope.title = 'About US';
    return $scope.message = 'Who cares!!!';
  };

  AccessDeniedController = function($scope) {
    $scope.title = 'Access Denied';
    return $scope.message = 'You does not have permissions to this page';
  };

  ContactController = function($scope, Requests, currentUser) {
    $scope.errors = {};
    $scope.success = false;
    $scope.isDisabled = false;
    $scope.contact = {
      name: (currentUser != null ? currentUser.full_name() : void 0) || '',
      email: (currentUser != null ? currentUser.email() : void 0) || ''
    };
    return $scope.submit = function() {
      $scope.isDisabled = true;
      $scope.internalError = false;
      return Requests.post('./contact/', $scope.contact).then(function() {
        return $scope.success = true;
      }, function(errors) {
        return $scope.errors = errors;
      }).then(function() {
        return $scope.isDisabled = false;
      });
    };
  };

  ContactController.$inject = ['$scope', 'Requests', 'currentUser'];

  angular.module('sxTrApp').controller('aboutController', AboutController).controller('accessDeniedController', AccessDeniedController).controller('contactController', ContactController);

}).call(this);
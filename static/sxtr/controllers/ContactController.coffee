

ContactController = ($scope, Requests, currentUser) ->
  $scope.errors = {}
  $scope.success = false
  $scope.isDisabled = false
  $scope.contact =
    name: currentUser?.full_name() || ''
    email: currentUser?.email() || ''
  $scope.submit = ()->
    $scope.isDisabled = true
    $scope.internalError = false
    Requests.post('./contact/', $scope.contact)
      .then -> # success callback
        $scope.success = true
      , (errors)->
        $scope.errors = errors
      .then -> # general request is finished
        $scope.isDisabled = false

ContactController.$inject = ['$scope', 'Requests', 'currentUser']

angular
  .module 'sxTrApp'
  .controller 'contactController', ContactController
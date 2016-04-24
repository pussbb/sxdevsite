
AboutController = ($scope) ->
  # create a message to display in our view
  $scope.title = 'About US'
  $scope.message = 'Nothing here for now. Sorry about that.'


AccessDeniedController = ($scope)->
  $scope.title = 'Access Denied'
  $scope.message = 'You does not have permissions to this page'


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
  .controller 'aboutController', AboutController
  .controller 'accessDeniedController', AccessDeniedController
  .controller 'contactController', ContactController
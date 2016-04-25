
LoginController = ($scope, Auth, $location)->
  $scope.errors = {}
  $scope.user = {}
  $scope.submit = ->
    $scope.errors = {}
    Auth.login $scope.user
     .then ->
       $location.path '/'
     , (data)->
       $scope.errors = data

LoginController.$inject = ['$scope', 'Auth', '$location']

ResetPasswordController = ($scope, Requests, $location) ->
  $scope.errors = {}
  $scope.user = {}
  $scope.submit = ->
    $scope.errors = {}
    Requests.post '/account/reset', $scope.user
      .then ->
        $location.path 'login'
      , (errors)->
        $scope.errors = errors

ResetPasswordController.$inject = ['$scope', 'Requests', '$location']

ChangePasswordController = ($scope, Requests, $location) ->
  $scope.errors = {}
  $scope.isDisabled = false
  $scope.user = {}
  $scope.submit = ->
    $scope.isDisabled = true
    $scope.errors = {}
    Requests.post '/account/change_password', $scope.user
      .then -> # success callback
        $location.path 'profile'
      , (errors)-> # on fail callback
        $scope.errors = errors
      .then -> # general request is finished
        $scope.isDisabled = false
ChangePasswordController.$inject = ['$scope', 'Requests', '$location']


RegisterController = ($scope, Requests, $location) ->
  $scope.errors = {}
  $scope.isDisabled = false
  $scope.user = {}
  $scope.submit = ->
    $scope.isDisabled = true
    $scope.errors = {}
    Requests.post '/account/register', $scope.user
      .then -> # success callback
        $location.path 'login'
      , (errors)-> # on fail callback
        $scope.errors = errors
      .then -> # general request is finished
        $scope.isDisabled = false

RegisterController.$inject = ['$scope', 'Requests', '$location']

ProfileController = ($scope, currentUser, Auth) ->
  $scope.errors = {}
  $scope.success = false
  $scope.isDisabled = false
  $scope.user = currentUser.data
  $scope.submit = ->
    $scope.errors = {}
    $scope.isDisabled = true
    Auth.updateUser $scope.user
      .then -> $scope.success = true
      .then -> $scope.isDisabled = false

ProfileController.$inject = ['$scope', 'currentUser', 'Auth']

angular
  .module 'sxTrApp'
  .controller 'loginController', LoginController
  .controller 'resetPasswordController', ResetPasswordController
  .controller 'registerController', RegisterController
  .controller 'profileController', ProfileController
  .controller 'changePasswordController', ChangePasswordController
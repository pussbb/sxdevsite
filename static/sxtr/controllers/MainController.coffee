
MainController = ($scope, translations) ->

  $scope.translations = translations

MainController.$inject = ['$scope', 'translations']


NewTranslationController = ($scope, locales, applications, $location, Requests) ->
  $scope.locales = locales
  $scope.model = {}
  $scope.errors = {}
  $scope.applications = applications
  $scope.submit = ->
    Requests.post 'translations/', $scope.model
     .then (data)->
        $location.path "/translation/#{data.id}"
      , (errors)->
        $scope.errors = errors


NewTranslationController.$inject = [
    '$scope', 'locales', 'applications', '$location', 'Requests'
]

TranslationController = ($scope, tr_model, $location, $routeParams, Requests) ->
  if not $routeParams?.id
    return $location.path '/'
  $scope.model = {}
  $scope.saving = false
  $scope.errors = {}
  $scope.canEdit = tr_model?.canEdit
  $scope.trUrl = "translations/#{$routeParams.id}"
  $scope.translation = tr_model
  $scope.onSubmit = ->
    $scope.saving = true
    Requests.post $scope.trUrl, $scope.model
     .then ->
        $scope.saving = false
      , (errors)->
        $scope.errors = errors

TranslationController.$inject = [
    '$scope', 'tr_model', '$location', '$routeParams', 'Requests'
]

angular
  .module 'sxTrApp'
  .controller 'mainController', MainController
  .controller 'newTranslationController', NewTranslationController
  .controller 'translationController', TranslationController

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

TranslationController = ($scope, $location, $routeParams, Requests, $interval) ->
  if not $routeParams?.id
    return $location.path '/'
  $scope.loading = true
  $scope.model = {}
  $scope.errors = {}
  Requests.get "translations/#{$routeParams.id}"
    .then (translation)->
      $scope.translation = translation
      $interval ->
        console.log($scope.model)
      , 600
      $scope
    , (errors)->
      $scope.errors = errors
    .then -> $scope.loading = false

TranslationController.$inject = [
    '$scope', '$location', '$routeParams', 'Requests', '$interval'
]

angular
  .module 'sxTrApp'
  .controller 'mainController', MainController
  .controller 'newTranslationController', NewTranslationController
  .controller 'translationController', TranslationController
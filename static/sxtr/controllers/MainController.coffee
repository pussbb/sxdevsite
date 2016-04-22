
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

TranslationController = ($scope, $location, $routeParams, Requests, $interval, $window) ->
  if not $routeParams?.id
    return $location.path '/'
  $scope.loading = true
  $scope.model = {}
  $scope.saving = false
  $scope.errors = {}
  $scope.trUrl = "translations/#{$routeParams.id}"
  Requests.get $scope.trUrl
    .then (translation)->
      $scope.translation = translation
      #$interval ->
      #
      #, 600
    , (errors)->
      $scope.errors = errors
    .then -> $scope.loading = false
  $scope.onSubmit = ->
    Requests.post $scope.trUrl, $scope.model
     .then ->
        $scope.saving = false
      , (errors)->
        $scope.errors = errors

TranslationController.$inject = [
    '$scope', '$location', '$routeParams', 'Requests', '$interval', '$window'
]

angular
  .module 'sxTrApp'
  .controller 'mainController', MainController
  .controller 'newTranslationController', NewTranslationController
  .controller 'translationController', TranslationController
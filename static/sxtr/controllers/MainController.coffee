
MainController = ($scope, translations) ->

  $scope.translations = translations

MainController.$inject = ['$scope', 'translations']


NewTranslationController = ($scope, locales, applications, $location, Requests) ->
  $scope.locales = locales
  $scope.model = {}
  $scope.errors = {}
  $scope.applications = applications
  console.log $scope
  $scope.submit = ->
    Requests.post 'translations/', $scope.model
     .then (data)->
        $location.path "/translation/#{data.id}"
      , (errors)->
        $scope.errors = errors


NewTranslationController.$inject = [
    '$scope', 'locales', 'applications', '$location', 'Requests'
]

TranslationController = ($scope, $location, $routeParams) ->
  if not $routeParams?.id
    return $location.path '/'


TranslationController.$inject = ['$scope', '$location', '$routeParams']

angular
  .module 'sxTrApp'
  .controller 'mainController', MainController
  .controller 'newTranslationController', NewTranslationController
  .controller 'translationController', TranslationController
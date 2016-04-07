
MainController = ($scope) ->
  $scope.title = 'Start page'
  $scope.message = 'Everyone come and see how good I look!'

angular
  .module 'sxTrApp'
  .controller 'mainController', MainController
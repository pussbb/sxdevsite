

AboutController = ($scope) ->
  # create a message to display in our view
  $scope.title = 'About US'
  $scope.message = 'Who cares!!!'


angular
  .module 'sxTrApp'
  .controller 'aboutController', AboutController
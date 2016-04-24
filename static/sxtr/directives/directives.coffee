
NavBarDirective = ($location) ->
  restrict: 'A'
  replace: false
  link: (scope, elem)->
    scope.$on "$routeChangeSuccess", ->
      elem.find('li.active').removeClass('active')
      curr = elem.find "li:has(a[href*='#{$location.$$url.replace('/', '', 1)}'])"
      if curr.length is 0
        if not elem.is('ul')
          curr = elem.find('ul:first li:first')
        else
          curr = elem.children().first()
      curr.addClass 'active'
    scope.$on '$routeChangeStart', ->
      if elem.attr 'aria-expanded'
        elem.collapse('hide')


FormGroup = ->
  restrict: 'E',
  transclude:
    'label': '?formGroupLabel',
    'body': 'formGroupBody',
    'footer': '?formGroupFooter'
  scope:
    'fieldErrors': '='
    'showLabel': '=?'
  controller: ($scope) ->
    if  angular.isUndefined $scope.showLabel
      $scope.showLabel = true
  template: '
        <div class="form-group" ng-class="{ \'has-error\' : fieldErrors }">
          <span ng-show="showLabel" class="col-md-1 col-md-offset-2 text-center" ng-transclude="label"></span>
          <div ng-class="showLabel ? \'col-md-8\' : \'\' ">
              <div ng-transclude="body"></div>
              <span class="help-block " ng-show="fieldErrors">
                  <ul>
                      <li ng-repeat="error in fieldErrors">{{ error }}</li>
                  </ul>
              </span>
          </div >
          <div ng-transclude="footer"></div>
        </div>
  '

angular
  .module 'sxTrApp'
  .directive 'navBarNav', ['$location', NavBarDirective]
  .directive 'formGroup', FormGroup
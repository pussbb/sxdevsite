
Requests = ($http, $q)->
    submitFn = (httpObj, args) ->
      deffered = $q.defer()
      httpObj.apply(httpObj, args).then (response)->
        deffered.resolve response?.data
      , (response) ->
        errors = '__all__': [
          'Something terrible happened at server side.
           Could not proceed with your request. Please try again later!!!'
        ]
        if response?.data?.errors
          errors = response.data.errors
        deffered.reject errors
      deffered.promise

    get: ->
      submitFn $http.get, arguments

    post: ->
      submitFn $http.post, arguments

    patch: ->
      submitFn $http.patch, arguments

    delete: ->
      submitFn $http.delete, arguments

    put: ->
      submitFn $http.put, arguments
    #


Requests.$inject = ['$http', '$q']


angular
  .module 'sxTrApp'
  .factory 'Requests', Requests
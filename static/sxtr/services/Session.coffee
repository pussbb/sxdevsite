

Auth = (Requests, $q, Session)->
  auth =
  initialized: $q.defer()
  init: ->
    deferred = $q.defer()
    Requests.get '/account/profile/'
      .then (data)->
        Session.setUser data
      , (errors)->
        errors
      .then ->
        auth.initialized.resolve()
        deferred.resolve(auth)
    deferred.promise
  login: (userData)->
    deferred = $q.defer()
    Requests.post '/account/login', userData
      .then (data)->
        deferred.resolve(Session.setUser data )
      , (errors)->
        deferred.reject(errors)
    deferred.promise
  logout: ->
    deferred = $q.defer()
    Requests.get '/account/logout'
      .then (data)->
        deferred.resolve(Session.destroy())
      , (errors)->
        deferred.reject(errors)
    deferred.promise
  updateUser: (userData)->
    deferred = $q.defer()
    Requests.post '/account/profile', userData
      .then (data)->
        deferred.resolve(Session.setUser data)
      , (errors)->
        deferred.reject(errors)
    deferred.promise
  isAuthorized: -> Session.isLoggedIn()
  currentUser: -> return Session.getUser()

  #

Auth.$inject = ['Requests', '$q', 'Session']

class User

  constructor: (data)->
    @data = data

  full_name: ->
    if @data?.first_name and @data?.last_name
      return "#{@data.first_name} #{@data.last_name}"
    @data?.username.toString()

  email: ->
    @data?.email.toString()


class Session
  @$inject = []

  constructor: ()->
    @user = null

  setUser: (data) ->
    if data
      data = new User(data)
    @user = data

  getUser: ->
    @user

  destroy: ->
    @setUser null

  isLoggedIn: ->
    @getUser() != null


angular
  .module 'sxTrApp'
  .factory 'Auth', Auth
  .service 'Session', Session
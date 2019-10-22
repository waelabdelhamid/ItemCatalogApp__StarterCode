# !/usr/bin/env python3
#
# "Server code" for the Catalog App Web Application.


import json
import os
import random
import string

import httplib2
import requests
from flask import (Flask, abort, flash, g, jsonify, make_response, redirect,
                   render_template, request)
from flask import session as login_session
from flask import url_for
from flask_httpauth import HTTPBasicAuth
from models import Base, Catalog, CatalogItem, User
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets
from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


auth = HTTPBasicAuth()


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)


@app.teardown_request
def remove_session(ex=None):
    session.remove()


# ADD @auth.verify_password decorator here
@auth.verify_password
def verify_password(username_or_token, password):
    # Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(
            username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# Create a state token to prevent request forgery.
# Store it in the session for later validation.
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" %login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange client token for long-lived server-side token with GET /oauth/
    # access_token?grant_type=fb_exchange_token&client_id={app-id}&
    # client_secret=
    # {app-secret}&fb_exchange_token={short-lived-token}
    app_id = json.\
        loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.\
        loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret='
           '%s&fb_exchange_token=%s') % (
        app_id, app_secret, access_token)
    #print 'the exchange url:%s'%url
    h = httplib2.Http()
    # result = h.request(url, 'GET')[1]  #after try i found it returns json, i
    # found another solution in github project
    #result = json.loads(h.request(url, 'GET')[1])
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    # nb:This API call has been officially deprecated by Facebook
    # as of March 25th, 2017. Requests made to that version will no longer work.
    # Please use the most current version of the Facebook API which shown below
    # in the next code block.
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token.
    # nb:This token includes an expires field that indicates how long this token
    # is valid. Long term tokens can last up to two months. I'm going to strip
    # the expires tag from my token since i don't need it to make API calls.
    # token = result.split("&")[0]  #after try i found it returns json, i
    # found another solution in github project
    #token = result['access_token']
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v2.8/me?access_token=%s&fields='
           'name,id,email') % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    #print "url sent for API access:%s"% url
    #print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['access_token'] = token

    # Get user picture
    # nb:Facebook uses a separate API call to retrieve a profile picture.
    # url =
    # 'https:
    # //graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200'
    # % token  #after try i found it used user_id not token
    url = ('https://graph.facebook.com/v2.2/%s/picture?&'
           'redirect=0&height=200&width=200') % login_session['facebook_id']
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    #print "url sent for API access for picture:%s"% url
    #print "API JSON for picture result: %s" % result
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (' " style = "width: 300px; height: 300px;border-radius: '
               '150px;-webkit-border-radius: 150px;-moz-border-radius: '
               '150px;"> ')
    flash("you are now logged in as %s" % login_session['username'])
    #print "done!"
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    # url = 'https://graph.facebook.com/%s/permissions' % facebook_id  #after
    # try i found its not work, the below one from github project
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    #print 'url of API call for fb log out result %s' % url
    #print 'The API call for fb log out result %s' % result
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    #print "call gconnect ok: %s" %request.args.get['state']
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # if there was an error in the access token info, abort,
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID dosen't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's Client ID does not match app's"), 401)
        #print "Token's Client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check to see if the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use., --this assuming
    #  none of the previous check is true , so let store it
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (' " style = "width: 300px; height: 300px;border-radius: '
               '150px;-webkit-border-radius: 150px;-moz-border-radius: '
               '150px;"> ')
    flash("you are now logged in as %s" % login_session['username'])
    #print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(
        username=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# add /token route here to get a token for the login user # I will use
# login_session instead of @auth.login_required because no local user
# creation till now only oauth provider user
@app.route('/catalog/token')
def get_auth_token():
    if 'username' not in login_session:
        return redirect('/login')
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    g.user = user
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


# JSON APIs to view Catalog Information


# List of all catalogs
@app.route('/catalog/JSON')
@auth.login_required
def catalogsJSON():
    memory = []

    catalogs = session.query(Catalog).order_by(asc(Catalog.name)).all()
    # return jsonify(Categories=[c.serialize.update(dict(Item=[i.serialize for
    # i in session.query(CatalogItem).filter_by(catalog_id=c.id).all()])) for
    # c in catalogs]) # it is same as below but the problem is c.serialize not
    # stores data, everytime bring the same serialize from the catalog class
    for c in catalogs:
        temp = c.serialize
        # memory.append(temp.update(dict(Item= [i.serialize for i in
        # session.query(CatalogItem).filter_by(catalog_id=c.id).all()]))) # it
        # is same as below but the problem is temp.update returns None
        items = [i.serialize for i in session.query(
            CatalogItem).filter_by(catalog_id=c.id).all()]
        # item=dict({'Item': items}) # it is same as below
        # item={'Item': items} # it is same as below
        item = dict(Item=items)
        temp.update(item)
        memory.append(temp)
    return jsonify(Category=memory)


# List the catalog items of a specific catalog
@app.route('/catalog/<int:catalog_id>/items/JSON')
@auth.login_required
def catalogItemsJSON(catalog_id):
    items = session.query(CatalogItem).filter_by(catalog_id=catalog_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


# And a specific catalog item
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/JSON')
@auth.login_required
def catalogItemJSON(catalog_id, item_id):
    Catalog_Item = session.query(CatalogItem).filter_by(id=item_id).first()
    if Catalog_Item:
        return jsonify(Category_Item=Catalog_Item.serialize)
    else:
        return jsonify(Category_Item={})


# Show all catalogs
@app.route('/')
@app.route('/catalog')
def showCatalogs():
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    lastItems = session.query(CatalogItem).order_by(
        desc(CatalogItem.created_at))
    # for i in lastItems:
    #    i.user=session.query(User).filter_by(id=i.user_id).one()
    # Change the None value for catalog_id to 0 because giving runtime err in url_for
    catalog = catalogs.first()
    if catalog:
        catalog_id = catalog.id
    else:
        catalog_id = 0
    # Get the first item of the first catalog if found to use with sample APIs
    item = session.query(CatalogItem).filter_by(catalog_id=catalog_id).first()
    if item:
        item_id = item.id
    else:
        item_id = 0
    return render_template(
        'catalogs.html',
        catalogs=catalogs,
        items=lastItems,
        catalog_id=catalog_id,
        item_id=item_id)


# Show a catalog items
@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items')
def showCatalogItems(catalog_id):
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(catalog_id=catalog_id).all()
    count_items = len(items)
    # Get the first item of the current catalog if found to use with sample APIs
    item = session.query(CatalogItem).filter_by(catalog_id=catalog_id).first()
    if item:
        item_id = item.id
    else:
        item_id = 0
    return render_template(
        'catalogItems.html',
        catalogs=catalogs,
        items=items,
        catalog=catalog,
        count_items=count_items,
        item_id=item_id)


# Create a new catalog item
@app.route('/catalog/<int:catalog_id>/items/new', methods=['GET', 'POST'])
def newCatalogItem(catalog_id):
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['category']:
            catalog_id = request.form['category']
        newItem = CatalogItem(
            name=request.form['name'],
            description=request.form['description'],
            catalog_id=catalog_id,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Catalog %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showCatalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'newCatalogItem.html',
            catalog_id=catalog_id,
            catalogs=catalogs)

# Edit a catalog item


@app.route(
    '/catalog/<int:catalog_id>/items/<int:item_id>/edit',
    methods=[
        'GET',
        'POST'])
def editCatalogItem(catalog_id, item_id):
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    editedItem = session.query(CatalogItem).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        # remove set time out and redirect to prevent navigation problem
        # return ("<script>function myFunction() {alert("
        #  "'You are not authorized to edit this Catalog Item. "
        #  "Please create your own Catalog Item in order to edit.'); "
        #  "setTimeout(function() {"
        #  "window.location.href = '"+url_for('showCatalogItem', catalog_id="
        #  "catalog_id, item_id=item_id)+"';"
        #  "}, 1000);}"
        #  "</script><body onload= 'myFunction()''>")
        return ("<script>function myFunction() {alert('You are not authorized "
                "to edit this Catalog Item. "
                "Please create your own Catalog Item "
                "in order to edit.');}</script><body onload= 'myFunction()''>"
                "Unauthorized Access</body>")
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.catalog_id = request.form['category']
            catalog_id = request.form['category']
        session.add(editedItem)
        session.commit()
        flash('Catalog Item Successfully Edited')
        return redirect(
            url_for(
                'showCatalogItem',
                catalog_id=catalog_id,
                item_id=item_id))
    else:
        return render_template(
            'editCatalogItem.html',
            catalog_id=catalog_id,
            item=editedItem,
            catalogs=catalogs)

# Delete a catalog item


@app.route(
    '/catalog/<int:catalog_id>/items/<int:item_id>/delete',
    methods=[
        'GET',
        'POST'])
def deleteCatalogItem(catalog_id, item_id):
    itemToDelete = session.query(CatalogItem).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['user_id']:
        # remove set time out and redirect to prevent navigation problem
        # return ("<script>function myFunction() {alert("
        #"'You are not authorized to delete this Catalog Item. "
        #"Please create your own Catalog Item in order to delete.'); "
        #  "setTimeout(function() {"
        #  "window.location.href = '"+url_for('showCatalogItem', catalog_id"
        #  "=catalog_id, item_id=item_id)+"';"
        # "}, 1000);}"
        # "</script><body onload= 'myFunction()''>")
        return ("<script>function myFunction() {alert('You are not authorized "
                "to delete this Catalog Item. "
                "Please create your own Catalog Item "
                "in order to delete.');}</script><body onload= 'myFunction()''>"
                "Unauthorized Access</body>")
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Catalog Item Successfully Deleted')
        return redirect(url_for('showCatalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'deleteCatalogItem.html',
            catalog_id=catalog_id,
            item=itemToDelete)


# Show a catalog item
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def showCatalogItem(catalog_id, item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()
    return render_template(
        'catalogItem.html',
        item=item,
        catalog_id=catalog_id)


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['access_token']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalogs'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalogs'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    #app.debug = True
    app.run(host='0.0.0.0', port=port)

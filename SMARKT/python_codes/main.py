# -*- coding: utf-8 -*-
import cherrypy
import json
from firebase import firebase
from firebase import jsonutil
import time
import datetime
import paho.mqtt.client as mqtt
ipBroker = "iot.eclipse.org"
portBroker = 1883
firebase = firebase.FirebaseApplication('https://smarkt-bac7b.firebaseio.com/', None)

class Generator(object):

		
	def index (self, *uri, ** params):
		outuput = '''
		WELCOME TO SMARKT:<br />
		<form id='login' action='login' method='post' accept-charset='UTF-8'>
		<fieldset >
		<legend>Login</legend>
		<label for='username' >UserName*:</label>
		<input type='text' name="username" id="username" maxlength="50" />
		<label for='password' >Password*:</label>
		<input type='password' name='password' id='password' maxlength="50" />
		<input type='submit'  value='Submit' />
		</form>
		</fieldset>

		<form id='register' action='register' method='post'
		accept-charset='UTF-8'>
		<fieldset >
		<legend>Register</legend>
		<label for='name' >Your Full Name*: </label>
		<input type='text' name='name' id='name' maxlength="50" />
		<label for='email' >Email Address*:</label>
		<input type='text' name='email' id='email' maxlength="50" />
		<label for='username' >UserName*:</label>
		<input type='text' name='username' id='username' maxlength="50" />
		<label for='password' >Password*:</label>
		<input type='password' name='password' id='password' maxlength="50" />
		<input type='submit' value='Submit' />
		</fieldset>
		</form>
				
        '''
		return output
		
	index.exposed = True
				
	def login (self,username=None,password=None):
		attempt = '/users/' + username
		auth = firebase.get(attempt, None)
		if auth['password'] == password:
			print("Logged in!")
			currentUser = username
			client.publish("$SMARKT/BROKER/LOGIN/",'currentUser');
			output = self.shoping(currentUser);
			
		else:
			output = "INCORRECT PASSWORD return and try to log again!"
		return output
	login.exposed = True

	def register (self, name,email,username,password):
		createUser = firebase.patch('/users', { username : { "username" : username , "password" : password, "email": email, "name":name}})
		currentUser = username
		print("Username not taken, creating user!")
		client.publish("$SMARKT/BROKER/NEWCLIENT/",currentUser);
		return ("Welcome, @" + currentUser)
	register.exposed = True
	
	def shoping(self,*uri, **params):
			
		out = '''
		<h3>WELCOME TO SMARKT :<h3>
		<h4>customer_name currentUser custumer_ID chart_ID:</h4>
		<form id='scan_product' action='scan_product' method='post' accept-charset='UTF-8'>
		<fieldset >
		<legend>ADD YOUR PRODUCT </legend>
		<input type='text' name='scan_input' id='scan_input' placeholder="Enter shopping item..." autofocus>
		<input type='submit'  value='Submit' />
		</fieldset>
		<fieldset >
		<legend>SHOP LIST </legend>
		<form id='shoplist' action='shoplist' method='post' accept-charset='UTF-8'>
		<input type="text" name="item" id="item" placeholder="item#"  autofocus>
		<input type="text" name="description" id="description" placeholder="description"  autofocus>
		<input type="text" name="quantity" id="quantity" placeholder="quantity"  autofocus>
		<input type="text" name="unityprice" id="unityprice" placeholder="unity price"  autofocus>
		<input type="text" name="totalprice" id="totalprice" placeholder="total price "  autofocus>
		<button type="submit" class="btn">DELETE</button><button type="submit" class="btn">ADD</button>
		<br/>
		<label for="TOTAL" >TOTAL:</label>
		<form id='TOTAL' action='TOTAL' method='post' accept-charset='UTF-8'>
		<input type="text" name="TOTAL" id="TOTAL"  maxlength="50" />
		<fieldset >
		<br/>
		<fieldset >
		<legend>PROMOTION MESSAGE </legend>
		<form id='promotion_func' action='promotion_func' method='post' accept-charset='UTF-8'>
		<input type="text" name="accept_promotion" id="accept_promotion" placeholder="promotion..." size="70">
		<button type="submit" class="btn">ACCEPT</button>
		</fieldset>
		<br/>
		<button type="submit" class="btn">SUBMIT YOUR SHOP LIST</button>
		<button type="submit" class="btn">CANCEL YOUR SHOP LIST</button>
		</fieldset>

		'''
		return out
	shoping.exposed = True
	
	def scan_product (self,scan_input=None,currentUser=None):
		produto = scan_input
		print produto
		client.publish("$SMARKT/BROKER/",'currentUser/can_input');
		
		return "welcome"
	scan_product.exposed = True

	
	
if __name__	== '__main__':
	client = mqtt.Client()
	client.connect("iot.eclipse.org",1883,60)
	#cherrypy.quickstart(Generator(), '/')
	cherrypy.tree.mount (Generator(),	'/')
	cherrypy.engine.start()
	cherrypy.engine.block()
from django.shortcuts import render_to_response
from django.template import RequestContext,Context
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
import urllib2
from django.http import HttpResponse
from django.shortcuts import render
import json
from models import customers
from models import streams,aspects
import os
import sqlite3
from random import shuffle
import logging
from django.conf.global_settings import AUTH_USER_MODEL
from admin import Streamlist
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
import socket
# Get an instance of a logger
logger = logging.getLogger(__name__)
import octo_configs
from django.db.models import F
from django.core.mail import send_mail

import math
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
dbfilename = os.path.join(BASE_DIR, 'db.sqlite3')
holgerhostname = 'opsqa.octoshape.org'
holgerusername = 'ispp-readonly'
holgerpassword = '1234'
cpcodes = {}
global aspectslist
# Create your views here.

	
def index(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password) 
	if user is not None:
			if user.is_active:
				auth_login(request, user)
				x=request.POST.get('login-check', None)
				if request.POST.get('login-check', None):
					request.session.set_expiry(3600*24*30*6)
				customerlist=customers.objects.all().order_by('name')
				aspectslist=aspects.objects.all().order_by('name')
				Context = {'customerlist' : customerlist,'aspectslist' : aspectslist}
				print Context
				return render_to_response('signin.html',Context,context_instance=RequestContext(request))
	if request.user.is_authenticated():
		if request.POST.get('login-check', None):
			request.session.set_expiry(3600*24*30)
			print request.POST.get('login-check', None)
		customerlist=customers.objects.all().order_by('name')
		aspectslist=aspects.objects.all().order_by('name')
		Context = {'customerlist' : customerlist,'aspectslist' : aspectslist}
		return render_to_response('signin.html',Context, context_instance=RequestContext(request))  
	return render_to_response('index.html',context_instance=RequestContext(request))
	
	user = authenticate(username=username, password=password)
		
	if user is not None:
			if user.is_active:
				login(request,user)
				
				HttpResponseRedirect('/signin/')

	return render_to_response('index.html',context_instance=RequestContext(request))

def signin(request):
	if request.user.is_authenticated():
		request.user.get_username()
		global customerlist
		customerlist=customers.objects.all().order_by('name')
		aspectslist=aspects.objects.all().order_by('name')
		Context = {'customerlist' : customerlist,'aspectslist' : aspectslist}
		return render_to_response('signin.html',Context,context_instance=RequestContext(request))
		#return render_to_response('signin.html', context_instance=RequestContext(request))  
	return render_to_response('signout.html',context_instance=RequestContext(request))
	
def signout(request):
	logout(request)
	return render_to_response('signout.html', context_instance=RequestContext(request))  

class HolgerClient:
	def __init__(self, dirserver, namespace, username, password):
		self.dirserver = dirserver
		self.holgerservers = []
		self.namespace = namespace
		self.username = username
		self.password = password
		self._get_holger_servers()

	def _get_holger_servers(self):
		reply = urllib2.urlopen('http://%s/octodir/v2/waldo' % self.dirserver).read()
		self.holgerservers = []
		for line in reply.split():
			if line.startswith('http://'):
				self.holgerservers.append(line)
		shuffle(self.holgerservers)

	'''
	def _get_holger_server(self):
		if len(self.holgerservers) == 0:
			self._get_holger_servers()

		if not len(self.holgerservers) > 0:
			raise Exception('All holger servers are down')

		return self.holgerservers[0]

	
	def _prepare_request(self, method, url, aspects, data=None, subdirs=None):
		if subdirs:
			subdirs = '&subdirs=%s' % subdirs
		else:
			subdirs = ''

		request = urllib2.Request('%s%s/%s?aspects=%s&format=json%s' % (self._get_holger_server(), self.namespace, url, aspects, subdirs), data=data)
		request.get_method = lambda: method
		if data:
			request.add_header('Content-Type', 'application/json')

		return request

	def _send_request(self, request):
		auth_handler = HTTPDigestAuthIntAuthHandler()
		auth_handler.add_password('octowebapi', self._get_holger_server(), self.username, self.password)
		opener = urllib2.build_opener(auth_handler)
		return opener.open(request)
	'''

	def _holger_open(self, method, url, aspects, data=None, subdirs=None):
		"""Make request to holger server, failing over to other servers in case of an error"""
		if subdirs:
			subdirs = '&subdirs=%s' % subdirs
		else:
			subdirs = ''

		for server in self.holgerservers:
			request = urllib2.Request('%s%s/%s?aspects=%s&format=json%s' % (server, self.namespace, url, aspects, subdirs), data=data)
			request.get_method = lambda: method
			if data:
				request.add_header('Content-Type', 'application/json')

			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi', server, self.username, self.password)
			opener = urllib2.build_opener(auth_handler)
			try:
				response = opener.open(request)
				return response
			except urllib2.HTTPError as e:
				if e.code >= 500 and e.code < 600:
					pass
				else:
					raise


	def _get_real_stream(self, stream):
		if stream.startswith(self.namespace):
			return stream[len(self.namespace)+1:]
		return stream

	def get_aspects(self, stream, aspects):
		"""Get aspects for the specified stream (or prefix)"""
		stream = self._get_real_stream(stream)
		aspects = '+'.join(aspects)
		return json.loads(self._holger_open('GET', stream, aspects).read(), strict=False)

	def get_aspects_omit(self, stream, aspects):
		"""Get aspects for the specified stream (or prefix)"""
		stream = self._get_real_stream(stream)
		aspects = '+'.join(aspects)
		return json.loads(self._holger_open('GET', stream, aspects, subdirs='omit').read(), strict=False)

	def get_aspects_fine(self, stream, aspects):
		"""Get aspects for the specified stream (or prefix)"""
		stream = self._get_real_stream(stream)
		aspects = '+'.join(aspects)
		return json.loads(self._holger_open('GET', stream, aspects, subdirs='fine').read())

	def get_aspects_coarse(self, stream, aspects):
		"""Get aspects for the specified stream (or prefix)"""
		stream = self._get_real_stream(stream)
		aspects = '+'.join(aspects)
		return json.loads(self._holger_open('GET', stream, aspects, subdirs='coarse').read())

	def put_aspect(self, stream, aspect, data):
		"""Put an aspect for the specified stream (or prefix)"""
		stream = self._get_real_stream(stream)
		return self._holger_open('PUT', stream, aspect, data).read()

	def patch_aspect(self, stream, aspect, data):
		"""Put an aspect for the specified stream (or prefix)"""
		stream = self._get_real_stream(stream)
		return self._holger_open('PATCH', stream, aspect, data).read()



def dbview(request):
	streamlist=streams.objects.all().order_by('name')
	Context = {'streamlist' : streamlist,}
	return render_to_response('dbview.html',Context,context_instance=RequestContext(request))


def get_cpcodes(name):
	global cpcodes
	
	if name not in cpcodes:
		cpcodes[name] = 'Not Found'
		for customer in customerlist:
			if customer.name == name:
				cpcodes[name] = customer.cpcode

	return cpcodes[name]

def Holgerstreams(request, tag=None):
	if request.user.is_authenticated():
		streamcontext=octo_configs.CONTEXT	
		global customerlist
		streamviewname=request.POST.get('Holgerinp','')
		print streamviewname
		streamlist=streams.objects.all().filter(name__contains=request.POST.get('Holgerinp',False))
		customerlist=customers.objects.all().order_by('name')
		aspectslist=aspects.objects.all().order_by('name')
		slist = []
		for stream in streamlist:
			name = "{}/".format(stream.name.split('/')[0])
			stream.cpcode = get_cpcodes(name)
			slist.append(stream)
		#print "i am "		
		Context = {'streamcontext' : streamcontext,'streamlist' : slist,'aspectslist' : aspectslist,'customerlist' : customerlist,'streamviewname' : streamviewname }
		print streamlist
		return render_to_response('signin.html',Context,context_instance=RequestContext(request))
		#Context = {'streamcontext' : streamcontext,'streamlist' : slist,'aspectslist' : aspectslist,'customerlist' : customerlist,'streamviewname' : streamviewname }
		#return render_to_response('signin.html',Context,context_instance=RequestContext(request))
	return render_to_response('signout.html',context_instance=RequestContext(request))
	

class HTTPDigestAuthIntAuthHandler(urllib2.HTTPDigestAuthHandler):
	def get_authorization(self, req, chal):
		try:
			realm = chal['realm']
			nonce = chal['nonce']
			qop = chal.get('qop')
			algorithm = chal.get('algorithm', 'MD5')
			opaque = chal.get('opaque', None)
		except KeyError:
			return None

			if qop != 'auth-int':
				return super(HTTPDigestAuthIntAuthHandler, self).get_authorization(req, chal)

		H, KD = self.get_algorithm_impls(algorithm)
		if H is None:
			return None

		user, pw = self.passwd.find_user_password(realm, req.get_full_url())
		if user is None:
			return None

		if req.has_data():
			entdig = H(req.get_data())
		else:
			entdig = H('')

		A1 = "%s:%s:%s" % (user, realm, pw)
		A2 = "%s:%s:%s" % (req.get_method(), req.get_selector(), entdig)

		if nonce == self.last_nonce:
			self.nonce_count += 1
		else:
			self.nonce_count = 1
			self.last_nonce = nonce

			ncvalue = '%08x' % self.nonce_count
			cnonce = self.get_cnonce(nonce)
			noncebit = "%s:%s:%s:%s:%s" % (nonce, ncvalue, cnonce, qop, H(A2))
			respdig = KD(H(A1), noncebit)

		base = 'username="%s", realm="%s", nonce="%s", uri="%s", ' \
			'response="%s"' % (user, realm, nonce, req.get_selector(),
								respdig)
		if opaque:
			base += ', opaque="%s"' % opaque
		if entdig:
			base += ', digest="%s"' % entdig
		base += ', algorithm="%s"' % algorithm
		if qop:
			base += ', qop=auth-int, nc=%s, cnonce="%s"' % (ncvalue, cnonce)
		return base




def search(request, tag=None):
	if request.user.is_authenticated():
		searchstr = request.POST.get('searchstring', False)
		auth_handler = HTTPDigestAuthIntAuthHandler()
		auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user,octo_configs.octo_pass)
		opener = urllib2.build_opener(auth_handler)

		first_name = str(octo_configs.octo_server+'/holger/32900/-/')
		last_name = str(searchstr)
		n=first_name+last_name
		request1 = urllib2.Request(n)
		request1.get_method = lambda: 'GET'
		request1.add_header('Content-Type', 'application/json')
		response = opener.open(request1).read()
		return render(response, 'admintable.html', context_instance=RequestContext( request, { 'json_response' : response }))
	return render_to_response('signout.html',context_instance=RequestContext(request))


def getbroadcastpw(getsignificantpass):
	prefix=getsignificantpass
	if prefix.endswith("/"):
		prefix=prefix
	prefix=prefix+'/'
	
	print prefix.count('/')
	for i in range(prefix.count('/')+1):
			print getsignificantpass
			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user,octo_configs.octo_pass)		
			opener = urllib2.build_opener(auth_handler)
			request1 = urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+getsignificantpass+'/')
			request1.get_method = lambda: 'GET'
			request1.add_header('Content-Type', 'application/json')
			responsepw = opener.open(request1).read()
			responsepwd=json.loads(responsepw)
			if 'live-srcpassword' in responsepwd:
				if 'password' in responsepwd['live-srcpassword']:
					bpwd=responsepwd['live-srcpassword']['password']
					#print bpwd
					return bpwd
			print getsignificantpass
			getsignificantpass=getsignificantpass.rsplit('/', 1)[0]

def checkpass(preexistpass):
	auth_handler = HTTPDigestAuthIntAuthHandler()
	auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user,octo_configs.octo_pass)		
	opener = urllib2.build_opener(auth_handler)
	request1 = urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+preexistpass)
	request1.get_method = lambda: 'GET'
	request1.add_header('Content-Type', 'application/json')
	responsepw = opener.open(request1).read()
	responsepwd=json.loads(responsepw)
	if 'live-srcpassword' in responsepwd:
		if 'password' in responsepwd['live-srcpassword']:
			bpwd=responsepwd['live-srcpassword']['password']
			print bpwd
			return 'set at prefix '+preexistpass+' is '+bpwd
		return ""
	return ""

def Putaspect():
	pass

def NewStream(request):
	global customerlist
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:
			if not request.user.is_superuser:
				if request.user.user_quota<1:
					erroredit= "**** Abort. 10 streams per day only . Please try tomorrow or escalate CC_Octo_Queue ****"
					global customerlist
					customerlist=customers.objects.all().order_by('name')
					aspectslist=aspects.objects.all().order_by('name')
					Context={ 'erroredit' : erroredit ,'customerlist' : customerlist,'aspectslist' : aspectslist}
					return render_to_response('signin.html',Context,context_instance=RequestContext(request))
					#return HttpResponse(' Abort. 10 streams per day only . Please try tommorrow <meta http-equiv="refresh" content="3;url=/" />') 
			request.user.user_quota=request.user.user_quota-1
			request.user.save()
			streamcreation=[]
			passoverwriteerr=""
			streamexisterr=""
			finalstr=[]
			checkbox=request.POST.get('multilive', False)
			custname=str(request.POST.get('custname', False))
			broadpw=""
			streamname = custname+request.POST.get('streamname', False)
			
			if streamname.endswith("/"):
				streamname=streamname[:-1]
			
			customerlist=customers.objects.all().order_by('name')
			aspectslist=aspects.objects.all().order_by('name')
			Context = {'customerlist' : customerlist}
			passwd=request.POST.get('streampwdopt', False)
			#custname=custname+'/'
			
			##print request.user.username
			searchstr = streamname+'/*'
			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user,octo_configs.octo_pass)
			opener = urllib2.build_opener(auth_handler)
		
			first_name = octo_configs.octo_server+'/holger/32900/-/'
			last_name = searchstr
			n=first_name+last_name
			
			requestget = urllib2.Request(n)
			requestget.get_method = lambda: 'GET'
			requestget.add_header('Content-Type', 'application/json')
			responseget = opener.open(requestget).read()

			maxbr='"bitrate": '
			maxbr+=  request.POST.get('maxbr', False)
			testvar = request.POST.get('maxbr', False)
			typeofstream=request.POST.get('streamtype')
			extratext=str(request.POST.get('comments' ,False))
			brvalues=testvar.split(',')	
			multisource = request.POST.get('redundant',False)
			streamnamesnewabr='{"streams": {'
			if request.user.is_superuser:
				for i in brvalues:
					if int(i)<octo_configs.MINBRrate:
						return HttpResponse(" Abort. Minimum 64 bitrate required . Please try again with correct values") 
			   	#check if stream already exists 
			if not request.user.is_superuser:
				if len(brvalues)>8:
					return HttpResponse(" Abort. Please add less than 8 bitrate") 
				for i in brvalues:
					if int(i)<octo_configs.MINBRrate or int(i)>octo_configs.MAXBRrate:
						return HttpResponse(" Abort. Minimum 64 bitrate required and Maximum 5000. Please try again with correct values") 
			   	#check if stream already exists 
			for i in brvalues:
				streamcheck=""	
				streamcheck=streamname+'/'+str(i)+'k'
				print streamcheck
				strc=""
				strc= streams.objects.all().filter(name=streamcheck)
				for x in strc:
					print x.name
					if (streamcheck==x.name):
						streamexisterr=streamcheck+' already exists.'
						Context= { 'streamexisterr' : streamexisterr,'passoverwriteerr' :passoverwriteerr, 'streamcreation' : streamcreation,'customerlist' : customerlist ,'aspectslist' : aspectslist}
						return render_to_response('signin.html',Context,context_instance=RequestContext(request))
						#return HttpResponse(streamcheck+" already exists")
			if passwd:
				if streamname.endswith("/"):
					searchpassword=streamname
				searchpassword=streamname+'/'
				checkpasswd=checkpass(searchpassword)
				print checkpasswd
				if checkpasswd:
					streamcreation.append('*****We cannot overwrite a password '+checkpasswd )
					passoverwriteerr='password cannot be overwritten'
				else:
					requestpwd =urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+searchpassword+'?aspect=live-srcpassword&format=json' ,data='{"password": "'+passwd+'"}')					
					requestpwd.get_method = lambda: 'PUT'
					requestpwd.add_header('Content-Type', 'application/json')
					try:
						responsepwd = opener.open(requestpwd).read()
						streamcreation.append('The stream password is '+passwd )
					except urllib2.HTTPError, e:
						#print(e.read())
						return render(e,'signin.html',  { 'flag1' : 0 })
			broadpw=""
			broadpw=getbroadcastpw(streamname)
			if broadpw:
				streamcreation.append('****  Broadcast Password for stream is '+broadpw)

			for i in brvalues:		
					streamnamesnewabr+='"' 		
					streamnamesnewabr+=streamname+'/'+str(i)+'k'
					streamnamesnewabr+='" : { },' 	
			streamnamesnewabr = streamnamesnewabr[:-1]
			finalstreamabr=streamnamesnewabr+'},"smooth": false}'
		
		
			for i in brvalues:		
				streamnamesnew="" 		
				streamnamesnew=streamname+'/'+str(i)+'k'
				##print streamnamesnew
			
				maxbr=""
				
				maxbr='"bitrate": '+str(int(i)*1000+0.3*(int(i)*1000))
				streamtype= '"streamtype": "'+typeofstream+'"'
				publish ='"publish": true'
				note=""
				note='"extra-text": { "note":" '+extratext+'"}'
				dat = '{' +maxbr+','+streamtype+','+publish+','+note+ '}'	
				if multisource:
					publish ='"publish": false'
					dat=""
					dat = '{' +maxbr+','+streamtype+','+publish+','+note+ '}'	
		
				if multisource:
					auth_handler = HTTPDigestAuthIntAuthHandler()
					auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user,octo_configs.octo_pass)
					opener = urllib2.build_opener(auth_handler)
					requestmultia =urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+streamnamesnew+'/a?aspect=livebase-pushed&format=json' ,data=dat)
					requestmultia.get_method = lambda: 'PUT'
					requestmultia.add_header('Content-Type', 'application/json')
					try:
						responsemultia = opener.open(requestmultia).read()
						streamcreation.append('PRIMARY Ingest Stream Name  octoshape://streams.octoshape.net/'+streamnamesnew+'/a  and the bitrate is  '+str(int(int(i)+0.3*(int(i))))+'k')
						updateDB(streamnamesnew+'/a','livebase-pushed')
						logger.info("User "+request.user.username+" created stream "+streamnamesnew+'/a')
					except urllib2.HTTPError, e:
						print e
						return render(e,'signin.html',  { 'flag1' : 0 })
					requestmultib =urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+streamnamesnew+'/b?aspect=livebase-pushed&format=json' ,data=dat)
					requestmultib.get_method = lambda: 'PUT'
					requestmultib.add_header('Content-Type', 'application/json')
					try:
						responsemultib = opener.open(requestmultib).read()
						updateDB(streamnamesnew+'/b','livebase-pushed')
						streamcreation.append('BACKUP Ingest Stream Name  octoshape://streams.octoshape.net/'+streamnamesnew+'/b  and the bitrate is  '+str(int(int(i)+0.3*(int(i))))+'k')
						logger.info("User "+request.user.username+" created stream "+streamnamesnew+'/b')

					except urllib2.HTTPError, e:
						print e
						return render(e,'signin.html',  { 'flag1' : 0 })
					msource='{"publish": true,"sources": {"'+streamnamesnew+'/a":{},"'+streamnamesnew+'/b":{}}}'
					#print msource
					requestmultip =urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+streamnamesnew+'?aspect=livebase-best&format=json' ,data=msource)
					requestmultip.get_method = lambda: 'PUT'
					requestmultip.add_header('Content-Type', 'application/json')
					try:
						responsemultip = opener.open(requestmultip).read()
						updateDB(streamnamesnew,'livebase-pushed')
						streamcreation.append('PLAYBACK Stream Name is octoshape://streams.octoshape.net/'+streamnamesnew+' and the bitrate is  '+str(int(int(i)+0.3*(int(i))))+'k')
						logger.info("User "+request.user.username+" created stream "+streamnamesnew)

					except urllib2.HTTPError, e:
						return render(e,'signin.html',  { 'flag1' : 0 ,'customerlist' : customerlist,'aspectslist' : aspectslist})
						print e
				else:
					requeststr =urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+streamnamesnew+'?aspect=livebase-pushed&format=json' ,data=dat)
					requeststr.get_method = lambda: 'PUT'
					requeststr.add_header('Content-Type', 'application/json')
					responsestr = opener.open(requeststr).read()
	
					updateDB(streamnamesnew,'livebase-pushed')
					logger.info("User "+request.user.username+" created stream "+streamnamesnew)
					 
					streamcreation.append('Stream Name is octoshape://streams.octoshape.net/'+streamnamesnew+' and the bitrate is  '+str(int(int(i)+0.3*(int(i))))+'k')

					
			if len(brvalues)>1:
				#print finalstreamabr	
				requestabr = urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+streamname+'/abr?aspect=multi-live&format=json' ,data=finalstreamabr)
				requestabr.get_method = lambda: 'PUT'
				requestabr.add_header('Content-Type', 'application/json')
				try:
					responseabr = opener.open(requestabr).read()
					#print(response)
					updateDB(streamname+'/abr', 'multi-live')
					streamcreation.append('****  The ABR PLAYBACK Stream Name is  octoshape://streams.octoshape.net/'+streamname+'/abr')
					logger.info("User "+request.user.username+" created stream "+streamnamesnew+'/abr')
					print streamcreation
					Context= { 'passoverwriteerr' :passoverwriteerr,'flag1' : 1 , 'streamcreation' : streamcreation,'customerlist' : customerlist,'aspectslist' : aspectslist }
					return render_to_response('signin.html',Context,context_instance=RequestContext(request))

				except urllib2.HTTPError, e:
				
					return HttpResponse(e, content_type="text/plain")
			
			logger.info("User "+request.user.username+" created streams "+str(streamcreation))
			Context={ 'passoverwriteerr' :passoverwriteerr,'flag1' : 1 , 'streamcreation' : streamcreation , 'customerlist' : customerlist,'aspectslist' : aspectslist}
			return render_to_response('signin.html',Context,context_instance=RequestContext(request))

		return HttpResponse("You are not allowed to create new streams. Please contact the SA team")
	return render_to_response('signout.html',context_instance=RequestContext(request))


def find_password(streamname, passwords):
	if streamname in passwords:
		# if the exact stream name has its own password, return it right away
		return passwords[streamname]
	
	password = None
	sorted_names = sorted(passwords, key=lambda x: len(x), reverse=True)
	for name in sorted_names:
		if name.endswith('/') and streamname.startswith(name):
			# stream names are sorted by length descending. the longest name will be the correct password so return it once it is found
			return passwords[name]
	
def updateDB(streamnametodb, aspect):	
	client = HolgerClient(holgerhostname, '-', holgerusername, holgerpassword)
	try:
		stream_aspects = client.get_aspects(streamnametodb, ['livebase-pushed', 'livebase-best', 'multi-live'])
		conn = sqlite3.connect(dbfilename)
		c = conn.cursor()
		password= getbroadcastpw(streamnametodb)
		for streamname in stream_aspects:
			values = stream_aspects[streamname] # much complicate
			bitrate = values['bitrate'] if 'bitrate' in values else None
			print bitrate
			streamtype = values['streamtype'] if 'streamtype' in values else None
			publish = values['publish'] if 'publish' in values else None
			print password
			readonly = values['read-only'] if 'read-only' in values else None
			c.execute('INSERT OR REPLACE INTO "login_streams" ("name", "aspect", "bitrate", "streamtype", "publish" , "password" ,"readonly") VALUES (?, ?, ?, ?, ?,?,?)', (streamnametodb, aspect, bitrate, streamtype, publish,password,readonly))

		conn.commit()
	
	except Exception as e:
		print('Something went wrong: %s' % e)
		HttpResponse("Unable to update local DB")
		
		
def delDB(streamnametodb):
	valuestrm=streamnametodb
	print valuestrm
	try:
		delinst= streams.objects.all().filter(name=valuestrm)
		delinst.delete()
	except Exception as e:
		print('Something went wrong: %s' % e)
		HttpResponse("Unable to update local DB")

def updateDBcust(custnametodb, aspect ):
	valuestrm=custnametodb
	try:
		conn = sqlite3.connect(dbfilename)
		c = conn.cursor()
		c.execute('INSERT INTO "login_customers" ("name", "cpcode") VALUES (?, ?)', (valuestrm,aspect ))
		conn.commit()
	
	except Exception as e:
		print('Something went wrong: %s' % e)
		HttpResponse("Unable to update local DB")

def allstream(request):
	if request.user.is_authenticated():
		request.user.get_username()
		#print request.user.username
		searchstr = '*'
		auth_handler = HTTPDigestAuthIntAuthHandler()
		auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user, octo_configs.octo_pass)
		opener = urllib2.build_opener(auth_handler)
		
		first_name = octo_configs.octo_server+'/holger/32900/-/'
		last_name = searchstr
		n=first_name+last_name
	
		request1 = urllib2.Request(n)
		request1.get_method = lambda: 'GET'
		request1.add_header('Content-Type', 'application/json')
		response = opener.open(request1).read()
		return render_to_response('test2.html',context_instance=RequestContext( request, { 'json_response' : response }))
	return render_to_response('signout.html',context_instance=RequestContext(request))

def deletestream(request,tag=None,tagasp=None):
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:
			print tag
			print tagasp
			Context = {'tag' : tag, 'tagasp' : tagasp}
			return render_to_response('StreamDelete.html',Context,context_instance=RequestContext(request))
		return render_to_response('signout.html',context_instance=RequestContext(request))
	return render_to_response('signout.html',context_instance=RequestContext(request))


def deletestreamconfirm(request):
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:
			global customerlist
			customerlist=customers.objects.all().order_by('name')
			aspectslist=aspects.objects.all().order_by('name')
			delstream=request.POST.get('delstream',False)
			delstreamasp=request.POST.get('delstreamaspect',False)
			print delstream
			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi',  octo_configs.octo_server, octo_configs.octo_user, octo_configs.octo_pass)
			opener = urllib2.build_opener(auth_handler)
			first_name = octo_configs.octo_server+'/holger/32900/-/'

			n=first_name+delstream+'?aspect='+delstreamasp
			requestdel = urllib2.Request(n)
 			try:
			 	requestdel.get_method = lambda: 'DELETE'
			 	requestdel.add_header('Content-Type', 'application/json')
				responsedel = opener.open(requestdel).read()
				print responsedel
				#print(response)
				delDB(delstream)
				logger.info("User "+request.user.username+" deleted stream "+delstream)
				delstream+=' has been deleted successfully'
				Context = {'deletstream' : delstream,'customerlist' : customerlist,'aspectslist' : aspectslist }
			except urllib2.HTTPError, e:
				print e
				logger.info("User "+request.user.username+" had error deleting stream "+delstream+" "+str(e))
				Context = {'deletstream' : 'Please contact Octoshape Operations as the item is read-only or part of abr','flag1' : 0 ,'customerlist' : customerlist }
				return render_to_response('signin.html',Context,context_instance=RequestContext(request))
			return render_to_response('signin.html',Context,context_instance=RequestContext(request))
		return render_to_response('signout.html',context_instance=RequestContext(request))
	return render_to_response('signout.html',context_instance=RequestContext(request))

	
def listtream(request,tag=None):
	logger.info("User "+request.user.username+" searched for "+tag)
	streamcontext=octo_configs.CONTEXT
	print 'is'+streamcontext
	if request.user.is_authenticated():
		global customerlist
		streamlist=streams.objects.all().filter(name=tag)
		customerlist=customers.objects.all().order_by('name')
		aspectslist=aspects.objects.all().order_by('name')

		slist = []
		for stream in streamlist:
			name = "{}/".format(stream.name.split('/')[0])
			stream.cpcode = get_cpcodes(name)
			slist.append(stream)
		auth_handler = HTTPDigestAuthIntAuthHandler()
		auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user, octo_configs.octo_pass)
		opener = urllib2.build_opener(auth_handler)
			
		first_name = octo_configs.octo_server+'/holger/32900/-/'+tag
	
		request1 = urllib2.Request(first_name)
		request1.get_method = lambda: 'GET'
		request1.add_header('Content-Type', 'application/json')
		response = opener.open(request1).read()
		responsenew=json.loads(response)
		streamabr=""
		slistabr=""
		streamtype=""
		bitrate=""
		actualbr=""
		publish=""
		streamlistabr=""
		slistbest = []	
		streamlistnonabr=""
		streamlistnoabrrecord=""
		erroredit=""
		streamabrexisting=""
		streambest=""
		streampassword =""
		if 'livebase-pushed' in responsenew:
			if 'live-srcpassword' in responsenew:
				if 'password' in responsenew['live-srcpassword']:
					streampassword=responsenew['live-srcpassword']['password']
			if 'read-only' in responsenew['livebase-pushed']:
				erroredit= "**** Uneditable stream in ISPP, Can be edited by OctoAdmins via OSMT ****"
				
				
			streamtype= responsenew['livebase-pushed']['streamtype']
			bitrate =responsenew['livebase-pushed']['bitrate']
			actualbr=int(bitrate/1000)
			bitrate=int(((bitrate)/1.3)/1000)
			publish =responsenew['livebase-pushed']['publish']
						
		else:
			if 'multi-live' in responsenew:
				streamabrexisting=responsenew['multi-live']['streams']
				streamlistnonabr=streams.objects.filter(name__contains=tag.rsplit('/', 1)[0]).filter(aspect__contains='livebase').filter(name__endswith='k')
				streamlistnoabrrecord=streamlistnonabr
				streamabr=responsenew['multi-live']['streams']
				slistabr = []	
				for l in streamabr:	
					streamlistabr=streams.objects.all().filter(name=l)
					
					for stream in streamlistabr:
						name = "{}/".format(stream.name.split('/')[0])
						stream.cpcode = get_cpcodes(name)
						slistabr.append(stream)
			else:
				if 'livebase-best' in responsenew:
					if 'sources' in responsenew['livebase-best']:
						streambest=responsenew['livebase-best']['sources']
			
		print([p.name for p in streamlistnoabrrecord])
		Context = {'streamcontext' : streamcontext,'streambest' : streambest,'streampassword' :streampassword,'streamabrexisting': streamabrexisting,'erroredit'	: erroredit,'streamlistnonabr':streamlistnonabr, 'abr':tag,'slistbest': slistbest,'streamlist' : slist,'streamlistabr': slistabr, 'streamabr': streamabr,'aspectslist' : aspectslist,'customerlist' : customerlist,'liss' : response, 'streamviewname' : tag, 'streamtype' : streamtype,'actualbr' : actualbr ,'bitrate' :bitrate,'publish' : publish}
		return render_to_response('EditStream.html',Context,context_instance=RequestContext(request))
	return render_to_response('signout.html',context_instance=RequestContext(request))
		
	
def NewCust(request):
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:
			newcust = request.POST.get('newcustname',False)
			newcust =newcust.lower()
			passwd = request.POST.get('row_password',False)
			#print newcust
			if not newcust.endswith("/"):
				newcust+='/'
			newcpcode=str(request.POST.get('newcustcpcode',False))
			newcpcode=str(newcpcode)
			Newcustcreated=[]
			Newcustcreated.append('New Customer name '+newcust)
			Newcustcreated.append('New password '+passwd)
			Newcustcreated.append('CPcode '+newcpcode)
			#client = HolgerClient(holgerhostname, '-', holgerusername, holgerpassword)
			#client._holger_open('PUT', stream, aspects)
			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi', octo_configs.octo_server , octo_configs.octo_user, octo_configs.octo_pass)
			dat= '{ "context": "'+octo_configs.CONTEXT+'","debtor-id" : "'+newcpcode+'" }'
			opener = urllib2.build_opener(auth_handler)
			requestcust =urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+newcust+'?aspect=customer&format=json' ,data=dat)
			requestcust.get_method = lambda: 'PUT'
			requestcust.add_header('Content-Type', 'application/json')
			requestpwd =urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+newcust+'?aspect=live-srcpassword&format=json' ,data='{"password": "'+passwd+'"}')
			requestpwd.get_method = lambda: 'PUT'
			requestpwd.add_header('Content-Type', 'application/json')
			requestmbr =urllib2.Request(octo_configs.octo_server+'/holger/32900/-/'+newcust+'?aspect=x-live-mbr&format=json' ,data='{"live": 311}')
			requestmbr.get_method = lambda: 'PUT'
			requestmbr.add_header('Content-Type', 'application/json')
			customerlist=customers.objects.all().order_by('name')
			aspectslist=aspects.objects.all().order_by('name')

		
			try:	
				responsecust = opener.open(requestcust).read()
				responsembr = opener.open(requestmbr).read()
				responsepwd = opener.open(requestpwd).read()
				updateDBcust(newcust, newcpcode)
				
				Context = {'customerlist' : customerlist,'Newcustcreated'	: Newcustcreated,'aspectslist' : aspectslist}
				logger.info("User "+request.user.username+" created new Customer "+str(Newcustcreated))
				return render_to_response('signin.html',Context,context_instance=RequestContext(request))
			except urllib2.HTTPError, e:
				print e
				return render(e,'signin.html',  { 'flag1' : 0 })
			return render_to_response('signin.html',Context,context_instance=RequestContext(request))
		return HttpResponse("Permission Error")
	return render_to_response('signout.html',context_instance=RequestContext(request))


def EditStream(request,tag=None):
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:
			streamupdate=[]	
			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user, octo_configs.octo_pass)
			opener = urllib2.build_opener(auth_handler)
			editstreamname=request.POST.get('streaminview',False)
			newstreamname=request.POST.get('editinview',False)
			editpublish=request.POST.get('editpublish',False)
			dattype=request.POST.get('editstreamtype',False)
			datbr=request.POST.get('editmaxbr',False)
			datbr=int(datbr)
			datbr=int((datbr+(0.3*datbr))*1000)
			datbr=str(datbr)
			leditpublish= editpublish.lower()
			streamprefix='{"publish": '+leditpublish+', "streamtype": "'+dattype+'" ,"bitrate": '+datbr+' }'
			streamupdate.append(editstreamname)
			path= octo_configs.octo_server+'/holger/32900/-/'+editstreamname+'?aspect=livebase-pushed&format=json'
			request1 =urllib2.Request(path ,data=streamprefix)
			request1.get_method = lambda: 'PUT'
			request1.add_header('Content-Type', 'application/json')
			#path2= 'http://173.193.194.70:28242/holger/32900/-/'+editstreamname+'?aspect=streamname&format=json'
			#request2 =urllib2.Request(path2 ,data='{ "name": "'+newstreamname+'"}')
			#request2.get_method = lambda: 'PUT'
			#request2.add_header('Content-Type', 'application/json')
			try:
				response = opener.open(request1).read()
				#response2 = opener.open(request2).read()
				global customerlist
				updateDB(editstreamname, 'livebase-pushed')
				customerlist=customers.objects.all().order_by('name')
				aspectslist=aspects.objects.all().order_by('name')

				Context = {'customerlist' : customerlist,'streamupdate'	: streamupdate ,'aspectslist' : aspectslist}
				return render_to_response('signin.html',Context,context_instance=RequestContext(request))
				#return HttpResponse('Done. STREAM UPDATED RELOADING PAGE<meta http-equiv="refresh" content="3;url=/" />')
			except urllib2.HTTPError, e:
				print e
				return render(e,'signin.html',  { 'flag1' : 0 })
			return render_to_response('EditStream.html',Context,context_instance=RequestContext(request))
		return HttpResponse("Permission Error")
	return render_to_response('signout.html',context_instance=RequestContext(request))
		
	

def Editabr(request,tag=None):
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:	
			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user, octo_configs.octo_pass)
			opener = urllib2.build_opener(auth_handler)
			
			first_name = octo_configs.octo_server+'/holger/32900/-/'+tag
			requestabr = urllib2.Request(first_name)
			requestabr.get_method = lambda: 'GET'
			requestabr.add_header('Content-Type', 'application/json')
			slistabr=[]
	
			try:
				responseabr = opener.open(requestabr).read()
				responsenew=json.loads(responseabr)
				if 'multi-live' in responsenew:
					streamlistnonabr=streams.objects.all().filter(name__contains=tag.rsplit('/', 1)[0]).filter(aspect__contains='livebase').filter(name__endswith='k')
					slistabr = []
					streamabr=responsenew['multi-live']['streams']
					for l in streamabr:	
						slistabr.append(l)
						
				Context = {'streamlistabr': slistabr ,'streamlistnonabr':streamlistnonabr, 'abr':tag}
				#response2 = opener.open(request2).read()
			except urllib2.HTTPError, e:
				print e
				return render(e,'signin.html',  { 'flag1' : 0 })
			return render_to_response('Editabr.html',Context,context_instance=RequestContext(request))
		return HttpResponse("Permission Error")
	return render_to_response('signout.html',context_instance=RequestContext(request))


def Updateabr(request,tag=None):
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:
			abrupdatestatus=""
			newabr=request.POST.get('valp', False)
			abr=request.POST.get('valabr', False)
			newabr=newabr[:-1]
			newabr=' {"streams": {'+newabr+'}}'
			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user, octo_configs.octo_pass)
			opener = urllib2.build_opener(auth_handler)
			path= octo_configs.octo_server+'/holger/32900/-/'+abr+'?aspect=multi-live&format=json'
			requestabrupdate =urllib2.Request(path ,data=newabr)
			requestabrupdate.get_method = lambda: 'PUT'
			requestabrupdate.add_header('Content-Type', 'application/json')
			try:
				responseabrupdate = opener.open(requestabrupdate).read()
				updateDB(abr, 'multi-live')
			except urllib2.HTTPError, e:
				print e
				erroredit=str(e)
				aspectslist=aspects.objects.all().order_by('name')
				Context = { 'erroredit'	: erroredit,'customerlist' : customerlist,'abrupdatestatus'	: abrupdatestatus ,'aspectslist' : aspectslist}
				return render_to_response('signin.html',Context,context_instance=RequestContext(request))
				#return render(e,'signin.html', )
			logger.info("User "+request.user.username+" updated abr stream "+abr)
			abrupdatestatus=abr+' has been updated '
			aspectslist=aspects.objects.all().order_by('name')
			Context = {'customerlist' : customerlist,'abrupdatestatus'	: abrupdatestatus ,'aspectslist' : aspectslist}
			return render_to_response('signin.html',Context,context_instance=RequestContext(request))
			#return HttpResponse('abr has been updated, RELOADING PAGE <meta http-equiv="refresh" content="3;url=/" />')
		return HttpResponse("Permission Error")
	return render_to_response('signout.html',context_instance=RequestContext(request))


def advconfig(request,tag=None):
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:
			print tag
			aspectslist=aspects.objects.all().order_by('name')
			Context = {'tag' : tag , 'aspectslist' : aspectslist}
			return render_to_response('Advanced.html',Context,context_instance=RequestContext(request))
		return render_to_response('signout.html',context_instance=RequestContext(request))
	return render_to_response('signout.html',context_instance=RequestContext(request))




def advconfigpage(request):
	if request.user.is_authenticated():
		if request.user.is_superuser or request.user.is_staff:
			streamname=	request.POST.get('streamidedit', False)
			streamaspect=request.POST.get('aspectnamenew', False)
			streamfilter=request.POST.get('aspectvalue', False)
			print streamfilter
			streammethod=request.POST.get('aspectmethod', False)
			customerlist=customers.objects.all().order_by('name')
			aspectslist=aspects.objects.all().order_by('name')
			print streamname,streamaspect,streamfilter,streammethod
			#return HttpResponse("Permission Error")
			#abr=request.POST.get('valabr', False)
			auth_handler = HTTPDigestAuthIntAuthHandler()
			auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user, octo_configs.octo_pass)
			opener = urllib2.build_opener(auth_handler)
			path= octo_configs.octo_server+'/holger/32900/-/'+streamname+'?aspect='+streamaspect+'&format=json'
			requestadvconfig =urllib2.Request(path ,data=streamfilter)
			requestadvconfig.get_method = lambda: streammethod
			requestadvconfig.add_header('Content-Type', 'application/json')
			reponse_data={}
			try:
				responseabrupdate = opener.open(requestadvconfig).read()
				abrupdatestatus=streamname+' has been updated '
				reponse_data['message']=streamaspect+'  Aspect Updated'
				return HttpResponse( json.dumps(reponse_data),content_type="application/json")
			except urllib2.HTTPError, e:
				print e
				error=str(e)
				reponse_data['message']=error
				delstream=streamname+' failed to update '
				Context = {'customerlist' : customerlist,'aspectslist' : aspectslist,'deletstream' : delstream}
				return HttpResponse( json.dumps(reponse_data),content_type="application/json")
				#return render_to_response('signin.html',Context,context_instance=RequestContext(request))
				#return render(e,'signin.html',  { 'flag1' : 0 })
			logger.info("User "+request.user.username+" updated advconfig stream "+streamname+" with values " +streamaspect,streamfilter,streammethod+".")
			Context = {'customerlist' : customerlist,'aspectslist' : aspectslist,'abrupdatestatus'	: abrupdatestatus}
			print "asdas"
			return HttpResponse( json.dumps(reponse_data),content_type="application/json")
			return render_to_response('signin.html',Context,context_instance=RequestContext(request))
			#return HttpResponse('abr has been updated, RELOADING PAGE <meta http-equiv="refresh" content="3;url=/" />')
		return HttpResponse("Permission Error")
	return render_to_response('signout.html',context_instance=RequestContext(request))
def ajax(request):
	reponse_data={}  
	print "hi" 	                          
	try:
 		reponse_data['message']=request.POST.get('formv', False)
  		return HttpResponse( json.dumps(reponse_data),content_type="application/json")
 	except:
  		reponse_data['message']='nothing'
  	 	return HttpResponse( json.dumps(reponse_data),content_type="application/json")
  	return HttpResponse( json.dumps(reponse_data),content_type="application/json")

def ajaxemail(request):
	reponse_data={}  
	print "hi" 	                          
	try:
 		y=request.POST.get('output', False)
 		print y
 		print reponse_data
 		send_mail('Details here', y , 'from@example.com',['chirag@chirags.in'], fail_silently=False)
  		return HttpResponse( json.dumps(reponse_data),content_type="application/json")
 	except:
  		reponse_data['message']='nothing'
  	 	return HttpResponse( json.dumps(reponse_data),content_type="application/json")
  	return HttpResponse( json.dumps(reponse_data),content_type="application/json")


def master(request,tag=None):
	logger.info("User "+request.user.username+" searched for "+tag)
	if request.user.is_authenticated():
		searchstr = tag
		auth_handler = HTTPDigestAuthIntAuthHandler()
		auth_handler.add_password('octowebapi', octo_configs.octo_server, octo_configs.octo_user,octo_configs.octo_pass)
		opener = urllib2.build_opener(auth_handler)

		first_name = str(octo_configs.octo_server+'/holger/32900/-/')
		last_name = str(searchstr)
		n=first_name+last_name
		request1 = urllib2.Request(n)
		request1.get_method = lambda: 'GET'
		request1.add_header('Content-Type', 'application/json')
		response = opener.open(request1).read()
		return render(response, 'masterdetail.html', context_instance=RequestContext( request, { 'json_response' : response }))
	return render_to_response('signout.html',context_instance=RequestContext(request))

	
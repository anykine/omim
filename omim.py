import os
import sys
import urllib
import urllib2

# download gene symbols from OMIM

# OMIM has different handlers for different type of data return
# http://www.omim.org/help/api
# I only want genemap here
class OMIM(object):

	def __init__(self, handler="entry", action="search1"):
		self.apiKey='WaSdXwt5R3evXruxxg-49g'
		self.api = 'http://api.omim.org/api'
		if handler in ['entry', 'geneMap', 'search', 'apiKey', 'dump']:
			self.handler = handler
#		self.values = values #dict of values
		self.action = action

	def makeHandlerURL(self):
		url = self.api + "/" + self.handler
		if self.action:
			url = url + "/" + self.action
		return(url)

	def getXMLData(self):
		url = self.makeHandlerURL()
		#print(url)
		data = urllib.urlencode(self.values)
		#print(data)
		
		# if you pass data, urllib uses POST
		req = urllib2.Request(url, data)
		# workaround
		req=url + "/?" + data
		#print req
		response = urllib2.urlopen(req)
        # return a string
		return(response.read())

	def setArgs(self, **kwargs):	
		"""pass dict of query parameters"""
		self.values = kwargs



#values={
#	'format' : 'json',
#	'mimNumber' : 100100,
#	'apiKey' : apiKey,
#
#}

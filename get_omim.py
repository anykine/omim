import os
import sys
import urllib
import urllib2
import omim
import xml.etree.ElementTree as etree

# Access the OMIM API
# download gene symbols from OMIM based on search string (eg muscle weakness)
# we are using XML data returned from OMIM

# We need to register apiKey through OMIM
apiKey='WaSdXwt5R3evXruxxg-49g'

# OMIM has different handlers for different type of data return
# http://www.omim.org/help/api
# I only want genemap here

# parameters to pass to OMIM API
values={
	'format' : 'xml',
	#'mimNumber' : 100100,
	'apiKey' : 'WaSdXwt5R3evXruxxg-49g',
	'search' : 'muscle weakness muscular dystrophy',
    #'limit' : 7000
    'limit' : 100
	#'include': 'geneMap'
}

#### Step1: grab ALL Entry MIM numbers! (large)

# create our OMIM object and pass in query parameters
# and grab list of Entries
a = omim.OMIM(handler="entry", action="search")
a.setArgs(**values)
xmlstring = a.getXMLData()

tree = etree.fromstring(xmlstring)
mimlst = tree.findall('.//mimNumber')
# list of mimNumbers
mimlst2 = [ i.text for i in mimlst]
print "size of mimlst2="
print len(mimlst2)
sys.exit(1)

#### Step2: query the OMIM API again passing 20 MIM entries at a time
### (they limit N=20 per GET) to get the Gene Symbols

# reuse values dict, remove search param
del values['search']
 
# tmp list
tmplst = []
# store results
allsymbols = []

for j in range(350):
    # read 20 MIM entries at a time
    for i in range(20):
        tmplst.append(mimlst2.pop(i))

    mims = ",".join(str(e) for e in tmplst)

    values['mimNumber'] = mims
    values['include'] = 'geneMap' # genesymbols are here

    # call OMIM 20 at a time, grab Genesymbols and put in allsymbols
    obj = omim.OMIM(handler="entry", action="")
    obj.setArgs(**values)
    xmlstring = obj.getXMLData()
    tree = etree.fromstring(xmlstring)
    genelst = tree.findall('.//geneSymbols')
    # some OMIM entries list multiple genesymbols per entry (SYM1, SYM2), so I
    # need to split them
    for sublist in genelst:
        for i in sublist.text.split(","):
            allsymbols.append(i)

    # clean up loop
    tmplst[:] 

# remove spaces from all symbols
allsymbols1 = [ str(i).replace(' ', '') for i in allsymbols ]

# find unique gene symbols
unique = set(allsymbols1)
print "len=" + str(len(unique))
fout = open("omim_gene_symbols.txt", "w")
for item in unique:
    fout.write(item)
fout.close()


## from list of mimNumbers, download 20 at a time
## to get gene symbol
#lst = tree.findall('.//geneSymbols')

#for l in lst:
#    print l.tag
#    print l.text
#



#data = urllib.urlencode(values)
#print data
#
#req = urllib2.Request(url, data)
#response = urllib2.urlopen(req)
#the_page = response.read()
#print the_page
#

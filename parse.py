#!/usr/bin/python

import datetime
import xml.etree.ElementTree


def getElementsFor(filename):
    tree = xml.etree.ElementTree.parse(filename)
    root = tree.getroot()

    atomns='http://www.w3.org/2005/Atom'
    espins='http://naesb.org/espi'
    entry = '{%s}entry' % (atomns,)
    link = '{%s}link' % (atomns,)
    content = '{%s}content' % (atomns,)
    block = '{%s}IntervalBlock' % (espins,)
    reading = '{%s}IntervalReading' % (espins,)
    value = '{%s}value' % (espins,)

    linkXPath = "%s/%s" % (entry, link)
    linkElements = root.findall(linkXPath)

    valueXPath = "%s/%s/%s/%s/%s" % (entry, content, block, reading, value)
    valueElements = root.findall(valueXPath)

    timePeriod = '{%s}timePeriod' % (espins,)
    start = '{%s}start' % (espins,)
    startsXPath = "%s/%s/%s/%s/%s/%s" % (entry, content, block, reading, timePeriod, start)
    startElements = root.findall(startsXPath)
    return (linkElements, valueElements, startElements)

def getText(x):
    return x.text

def getHref(x):
    return x.get('href')

def hasUsagePoint(x):
    i = x.find("UsagePoint")
    return (i>0)

def getUsagePointFor(s):
    tokens = s.split("/")
    usagePointIndex = tokens.index("UsagePoint")
    if(usagePointIndex < 0):
        raise Exception('could not find UsagePoint')
    return tokens[1+usagePointIndex]

def getUsagePoint(linkElements):
    retval = set()
    linkTextList = map(getHref, linkElements)
    usagePointLinks = filter(hasUsagePoint, linkTextList)
    for link in usagePointLinks:
        retval.add(getUsagePointFor(link))
    if(1 == len(retval)):
        return retval.pop()
    raise Exception('UsagePoint is not unique')

def isoize(x):
    naked = datetime.datetime.utcfromtimestamp(long(x)).isoformat()
    explicit = naked + "Z"
    return explicit
                   
def mayne():
    (linkElements, valueElements, startElements) = getElementsFor('pge_electric_interval_data.xml')
    usagePoint = getUsagePoint(linkElements)
    values = map(getText, valueElements)
    s_epoch = map(getText, startElements)
    s_iso8601 = map(isoize, s_epoch)

    for occurred, value in zip(s_iso8601, values):
        print "%s,%s,%s" % (usagePoint, occurred, value)

if __name__ == "__main__":
    mayne()

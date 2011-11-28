#!/usr/bin/python

##自动生产diff文件

import os
import re
import sys

####svn######
svnlog = r'svn log --stop-on-copy %s'
svndiff = r'svn diff -r %s:%s %s > %s-%s.diff'

def getVersion(line):
	v = re.split('\|', line)
	p = re.compile('^\s*r(\d*)\s*.*$')
	m = p.match(v[0])
	n = m.group(1)
	return int(n);

def main():
	svnurl = raw_input("svn url? ")
	cmd = (svnlog % svnurl)
	pipe = os.popen(cmd)

	logSeparator = '------------------------------------------------------------------------'	
	isVerLine = False
	versions = []

	for line in pipe:
		line = line[0:-1]

		if line == logSeparator :
			isVerLine = True
		elif isVerLine : 
			isVerLine = False
			versions.append( getVersion(line) )

	pipe.close()
	ev = versions[0]
	sv = versions[len(versions)-1]

	cmd = (svndiff % (ev, sv, svnurl, ev, sv) )
	os.system(cmd)
	print "OK, the diff file created successfully."

main()


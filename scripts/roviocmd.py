#!usr/bin/python

import os,sys,httplib
import base64,time
import string,re

import rovioapi

if len(sys.argv) <= 4:
  print "Usage: roviocmd.py <ip> <login> <passwd> <command>"
  print " get_revision reboot"
  raise SystemExit

g_command=sys.argv[4]
if len(sys.argv)>5:
  g_args=sys.argv[5:]
else:
  g_args=[]
	

g_Debug=False;

(g_strRovioIP,g_strLogin,g_strPwd)=sys.argv[1:4]

if g_Debug: 
    print "Using IP:%s with login:%s/%s"%(g_strRovioIP,g_strLogin,g_strPwd)


print "Doing Rovio access"

done=False
rovio=rovioapi.CRovioApiClient(g_strRovioIP,g_strLogin,g_strPwd)
rovio.RefreshStatusInfo()
    
if g_command=="get_version":
    print "Rovio version:",rovio.GetVersion()    

  
# do we have a read mem etc command
if g_command=="read_mem":
  if g_args[2]=="text":
    bytes = rovio.ReadMem(g_args[0],g_args[1])
    count=0
    for i in bytes:
      print "0x%02x"%i,
      count+=1
      if count%8==0: print ""
  elif g_testArgs[2]=="binary":
    bytes = rovio.ReadMem(g_args[0],g_args[1],g_args[3])
    print "Saved in:",g_args[3]  
print "Done"

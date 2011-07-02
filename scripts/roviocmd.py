#!/usr/bin/python

import os,sys,httplib
import base64,time
import string,re

import rovioapi

if len(sys.argv) < 4:
  print "Usage: roviocmd.py <ip> <login> <passwd> <command>"
  print """ cmd:
     get_version                             # Returns version of Rovio firmware should be 5.03
     reboot                                  # Warm reboot now
     read_mem <addr> <len> text              # Reads len bytes at address addr from Rovio memory and print as hex
     read_mem <addr> <len> file <file-name>  # Reads len bytes at address addr from Rovio memory and save in file
"""
  raise SystemExit

# Get information about Rovio IP / Port / user/pwd 
(g_strRovioIP,g_strLogin,g_strPwd)=sys.argv[1:4]

# Get command info 
g_command=sys.argv[4]
if(len(sys.argv)>4):
    g_params=sys.argv[5:]
else:
    g_params=[]

print "Trying Rovio access"

done=False
rovio=rovioapi.CRovioApiClient(g_strRovioIP,g_strLogin,g_strPwd)
rovio.RefreshStatusInfo()

print "Connected"
    
# Execute command
if g_command=="get_version":
    print "Rovio version:",rovio.GetVersion()    

    # do we have a read mem etc command
elif g_command=="read_mem":
    dumpfile=None
    if (len(g_params)>2):
      dumpfile=g_params[2]  
    bytes = rovio.ReadMem(g_params[0],g_params[1],dumpfile)
    count=0
    if dumpfile:
        print "Saved in:",dumpfile  
    else:
        for i in bytes:
          print "0x%02x"%i,
          count+=1
          if count%8==0: print ""
        print
elif g_command=="write_mem":
	bytes = rovio.WriteMem(g_params[0],g_params[1])
elif g_command=="reboot":
    bytes = rovio.Reboot()
  
print "Done"

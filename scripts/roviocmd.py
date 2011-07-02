#!/usr/bin/python

import os,sys,httplib
import base64,time
import string,re

import rovioapi

if len(sys.argv) < 4:
  print "Usage: roviocmd.py <ip> <login> <passwd> <command>"
  print """ cmd:
     get_version                          # Returns version of Rovio firmware should be 5.03
     reboot                               # Warm reboot now
     read_mem <addr> <len> [<file-name>]  # Reads len bytes at address addr from Rovio memory and eventually save in file
     write_mem <addr> hex  <hexstring>    # write to Rovio memory at <addr>, hex string like 0x01,0x02,.....
     write_mem <addr> file <filename>     # write to Rovio memory at <addr> content of <filename> 
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
        print "\nSaved in:",dumpfile  
elif g_command=="write_mem":
    filein=None
    if g_params[1] =='hex':
        bytes = rovio.WriteMem(g_params[0],g_params[2])
    elif g_params[1] =='file':
        bytes = rovio.WriteMem(g_params[0],"",g_params[2])
    else:
        print "unknown data format",g_params[1]
        
elif g_command=="reboot":
    bytes = rovio.Reboot()
  
print "Done"

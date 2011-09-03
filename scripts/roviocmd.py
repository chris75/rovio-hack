#!/usr/bin/python

import os,sys,httplib
import base64,time
import string,re

import rovioapi


def print_usage():
  print "Usage: roviocmd.py <ip> <login> <passwd> <command>"
  print """ cmd:
     get_version                          # Returns version of Rovio firmware should be 5.03
     reboot                               # Warm reboot now
     malloc  <len>                        # Allocate len bytes of memory in Rovio RAM 
     read_mem <addr> <len> [<file-name>]  # Reads len bytes at address addr from Rovio memory and eventually save in file
     write_mem <addr> hex  <hexstring>    # write to Rovio memory at <addr>, hex string like 0x01,0x02,.....
     write_mem <addr> file <filename>     # write to Rovio memory at <addr> content of <filename> 
     patch_fw  <hook.bin> <addr_hook> <code.bin> <addr_code> # hook.bin/addr_hook: file with hook code (currently hooking GetVer.cgi at 0x000709D8)
                                                             # code.bin/addr_code: file with code to load in RAM at 0x70e020
"""
if len(sys.argv) < 4:
  print_usage()
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
elif g_command=="malloc":
    (pointer,total) = rovio.Malloc(g_params[0])
    print "Allocated %s bytes at address: %s (%s allocated via malloc)"%(g_params[0],pointer,total)
elif g_command=="patch_fw":
    if(len(g_params)< 4):
      print " Error: missing parameters"
      print_usage()
      raise SystemExit
    print "Allocate 128K RAM"
    code_file=g_params[2]
    code_addr=eval(g_params[3])
    (pointer,total) = rovio.Malloc(0x20000)
    pointer=eval(pointer)
    print "Got 128K RAM at %08X : "%pointer
    if pointer >= code_addr:
       print " Cannot patch. Got a buffer at 0x%08X and you want to load your code at 0x%08X  which is not in allocated buffer. Try a Rovio reboot Reboot to allocate from clean state"%(pointer,code_addr)
       raise SystemExit
    hook_file=g_params[0]
    hook_addr=g_params[1]
    print "Uploading hook code from '%s' at address '%s'"%(hook_file,hook_addr)
    bytes = rovio.WriteMem(hook_addr,"",hook_file)
    print "Uploading fw patch from '%s' at address '%s'"%(code_file,code_addr)
    bytes = rovio.WriteMem("0x%08X"%code_addr,"",code_file)
    patch_addr=code_addr-0x20
    print "Write PATC marker at address '%s'"%(patch_addr)
    bytes = rovio.WriteMem("0x%08X"%patch_addr,"0x50,0x41,0x54,0x43")
  
print "Done"

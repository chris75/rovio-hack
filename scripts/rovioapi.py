import os,sys,httplib
import base64,time
import string,re


g_iColCount=0

class CRovioApiClient:
    def __init__(self, ip,login,password):
      port="80"
      # If ip has port info ie: 192.168.1:8080
      if ':' in ip:
        (ip,port)=ip.split(':')

      self.password = password
      self.login    = login
      print "Connect to Rovio at '%s' port '%s'"%(ip,port)
      self.hConRovio = httplib.HTTPConnection(ip,port)
      base64string = base64.encodestring('%s:%s' % (login, password))[:-1]
      self.extraHeaders ={"Authorization":"Basic %s" % base64string}
      
      # For status variable
      self.dictStatus ={}
      # Try to read version to see if things are ok 
      self.version = self.GetVersion()
      print "Connected to Rovio version:", self.version 
      
    def CGIGet(self,url):
       self.hConRovio.request("GET", url,None,self.extraHeaders)
       response = self.hConRovio.getresponse()
       # print "Result:%s %s"%(response.status, response.reason)
       data = response.read()
       return data 

    def GetRawRevision(self):
      return self.CGIGet("/rev.cgi?Cmd=nav&action=1")
    
    def GetVersion(self):
      return self.CGIGet("/GetVer.cgi")
    
    def RefreshStatusInfo(self):
      data = self.GetRawRevision()
      lstLines = string.split(data, "\n")
      for i in lstLines:
        lstPairs = string.split(i,"|")
        for p in lstPairs:
          p = string.replace(p,"\r","")
          if(p.find("=")>0):
            (varName,varValue) = string.split(p,"=")
            self.dictStatus[varName]=varValue
            
    def GetStatus(self,name):
        return self.dictStatus[name]
      
    def RovioDoMove(self,direction,speed):
      self.CGIGet("/rev.cgi?Cmd=nav&action=18&drive=%d&speed=%d"%(direction,speed))

    def GoHome(self):
      result = self.CGIGet("/rev.cgi?Cmd=nav&action=12")
      print "GO Home:",result
      
    def GoForward(self,speed=2):
      self.RovioDoMove(1, speed)
    def GoBackward(self,speed=1):
      self.RovioDoMove(2, speed)
    def Stop(self):
      self.RovioDoMove(0, 2)
      
    def ReadMem(self,start,length,toFile=None,append=True):
      bytes=[]
      toRead = eval(length)
      address=eval(start)
      bytes_read=0
      while toRead>0:
        if toRead>0x200:
          size=0x200
        else:
          size = toRead
          
        if not toFile:print
        print "  Reading from %08X - %04X bytes ..."%(address,size),  
        output=self.CGIGet("/debug.cgi?action=read_mem&address=0x%08x&size=0x%08x"%(address,size))
        print "OK"
        lstLines=output.split("\n")[1:]
        if toFile:
          fileOut=open(toFile,"a")
        for i in lstLines:
          s = i[len("read_mem = "):].replace("\n","")
          cur_address=address
          for b in s.split(" "):
            if len(b)==2:
              b=eval("0x"+b)
              if toFile :
                fileOut.write(chr(b))
              else:
                if bytes_read%8==0:
                    print "\n0x%08X:"%(cur_address),
                print "0x%02X"%(b),
                cur_address+=1
                bytes_read+=1  
                bytes.append(b)
        if not toFile: print
                
        toRead -= size
        address+=size
      if toFile:
        fileOut.close()
      else:
        print                
      return bytes          

    def WriteMem(self,start,values,fromFile=None):
      """ For ex : start= '0x1234' values: '0x01,0x02....' """
      address=eval(start)
      if fromFile:
          lstValues=open(fromFile,"r").read()
      else:
        lstValues=values.split(",")
      written=0
      print "Writing to %08X %d bytes:"%(address,len(lstValues))
      for i in lstValues:
        if fromFile:
            val="0x%02X"%ord(i)
        else:
            val=i
        output=self.CGIGet("/debug.cgi?action=write_mem&address=0x%08x&size=0x01&value=%s"%(address,val))
        if written%8==0:
            print "\n0x%08X: "%(address),
        print val,
        address+=1
        written+=1
      print
      return bytes          

    def Reboot(self):
      """ Do warm reboot"""
      self.CGIGet("/Reboot.cgi")
      return           

    def Malloc(self,size):
      """ Allocate memory in bytes """
      res=self.CGIGet("/debug.cgi?action=malloc&size=%s"%size)
      return res

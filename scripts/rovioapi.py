import os,sys,httplib
import base64,time
import string,re


g_iColCount=0

class CRovioApiClient:
    def __init__(self, ip,login,password):
      port=80
      # If ip has port info ie: 192.168.1:8080
      if ':' in ip:
        (ip,port)=ip.split(':')

      self.password = password
      self.login    = login
      print "Connect with",ip,port
      self.hConRovio = httplib.HTTPConnection(ip,port)
      base64string = base64.encodestring('%s:%s' % (login, password))[:-1]
      self.extraHeaders ={"Authorization":"Basic %s" % base64string}
      
      # For status variable
      self.dictStatus ={}
      
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
      while toRead>0:
        if toRead>0x200:
          size=0x200
        else:
          size = toRead
        print "Reading from %08X - %04X bytes ..."%(address,size),  
        output=self.CGIGet("/debug.cgi?action=read_mem&address=0x%08x&size=0x%08x"%(address,size))
        print "OK"
        toRead -= size
        address+=size
        lstLines=output.split("\n")[1:]
        if toFile:
          fileOut=open(toFile,"a")
        for i in lstLines:
          s = i[len("read_mem = "):].replace("\n","")
          for b in s.split(" "):
            if len(b)==2:
              b=eval("0x"+b)
              if toFile :
                fileOut.write(chr(b))
              else:
                bytes.append(b)
      if toFile:
        fileOut.close()                
      return bytes          

    def WriteMem(self,start,values,fromFile=None):
      """ For ex : start= '0x1234' values: '0x01,0x02....' """
      address=eval(start)
      if fromFile:
          lstValues=open(fromFile,"r").read()
      else:
        lstValues=values.split(",")
      for i in lstValues:
        output=self.CGIGet("/debug.cgi?action=write_mem&address=0x%08x&size=0x01&value=%s"%(address,i))
        address+=1
        print "Write =>",i
      return bytes          


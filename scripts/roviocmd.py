import os,sys,httplib
import base64,time
import string,re

if len(sys.argv) < 4:
  print "Usage: RovioControl <ip> <login> <passwd> <testXX>"
  print " testXX: testBackward testForward"
  raise SystemExit

g_testXX=""
if len(sys.argv)==5:
  g_testXX=sys.argv[4]
  
g_testCommand=None
if len(sys.argv)>5:
  g_testCommand=sys.argv[4]
  g_testArgs=sys.argv[5:]

g_Debug=False;

(g_strRovioIP,g_strLogin,g_strPwd)=sys.argv[1:4]

if g_Debug: 
    print "Using IP:%s with login:%s/%s"%(g_strRovioIP,g_strLogin,g_strPwd)

g_iColCount=0

class CRovioApiClient:
    def __init__(self, ip,login,password):
      self.ip=ip
      self.password = password
      self.hConRovio = httplib.HTTPConnection(g_strRovioIP,80)
      base64string = base64.encodestring('%s:%s' % (g_strLogin, g_strPwd))[:-1]
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

print "Doing Rovio access"
done=False
try :
    rovio=CRovioApiClient(g_strRovioIP,g_strLogin,g_strPwd)
    rovio.RefreshStatusInfo()
    done = True
except:
    print "Rovio not up waiting 5 sec"
    time.sleep(5)

# Do we have a simple test command 
if len(g_testXX)>0:
  print "Doing test:",g_testXX
  if g_testXX=="testBackward":
    for i in range(10):
      rovio.GoBackward()
      time.sleep(0.1)
    time.sleep(2)
    rovio.Stop()
    raise SystemExit
  elif g_testXX=="testGoHome":
    rovio.GoHome()
  
# do we have a read mem etc command
if g_testCommand:
  if g_testCommand=="read_mem":
    if g_testArgs[2]=="text":
      bytes = rovio.ReadMem(g_testArgs[0],g_testArgs[1])
      count=0
      for i in bytes:
        print "0x%02x"%i,
        count+=1
        if count%8==0: print ""
    elif g_testArgs[2]=="binary":
      bytes = rovio.ReadMem(g_testArgs[0],g_testArgs[1],g_testArgs[3])
      print "Saved in:",g_testArgs[3]  
  print "Done"

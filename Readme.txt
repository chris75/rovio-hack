
Current code is a proof of concept for hacking directly Rovio code in RAM to implement local bahavior 
ie: not relying on a computer 'driving' the Web API to do automatic things.

Demo code currently installs a timer procedure sending commands to blink Rovio blue leds left-right.

To recompile and test the code: 

1 - Prerequisite: 

 I'm doing this on Linux and using a gcc ARM cross compiler plus python scripts, this could probably be transposed to Windows with cygwin etc...
 So you need:
  * A rovio with Firmware 5.03. This is critical as code invokes Firmware functions at specific addresses, so other
    version will probably have different addresses.
  * An ARM Compiler, you can get a good one from : http://www.codesourcery.com/
  * Set your path so arm-XXX tools are available ie: something like : 
    export PATH=/opt/arm-2010.09/bin:$PATH

 Note: I've added precompiled binaries in bin so you can eventually used this to do a quick .

2 - Set variables for Rovio IPs/Crendentials

 Copy rovio.local.sample to rovio.local and edit for your particular rovio settings ie: ip / login / password.

3 - Compile & upload code 
  
 From main folder (where Makefile is) run command:  
   make

 Code will be recompiled then  a python script will be invoked to push code to Rovio memory.

4 - trigger new code 

 With a browser got Rovio URL : 
   http://<myrovio>/GetVer.cgi 

 Page should say some cryptic stuff about a patch and MCU response

 Then if you Rovio is not on Dock you should see blue leds blinking righ to left 


Principle of Operation:

 Since WoWwee posted in bulk on http://www.robocommunity.com/ some of the sources and precompiled 
 objs with debug info, we were able to have an inside look at what Rovio firmware really does.
 Unfortunately everything was compiled with proprietary compiler / libs so we can't build alternative 
 firmware at this point. 

 Knowing this,  a simpler option was to patch Rovio memory via APIs (write_mem). 

 So the trick is to first compile some ARM code to replace a well-known API here the code is patch-getver.c 
 and is poked at the location of the code behind the URL:
   http://X.X.X.X/GetVer.cgi 

 When invoked this code will look at some specific address in RAM (0x70e000) for a firwmare patch.  
 If a signature for the patch ('PATC') is found code at 0x70e020 is invoked. 
 
 At this location a demo code is poked (demo-leds.c), currently this code will register a timer rountine to send commands 
 to mcu to turn on/off blue leds in sequence.

 The demo-leds code is poked in a memory region that is first allocated via the malloc API, so in theory this code is 
 in a safe area that won't be overwritten during rovio operations. 
 It is recommended to patch rovio shortly after startup and before you control it via browser, otherwise malloc will get 
 a free area that is too high for current values used to compile code. 
 The python script will complain about this if it happens.


 I disassembled a bit the Rovio code to locate some APIs, so far the code uses: 
   * ictlCtrlMCU @0x000B8098: Sends a command string to MCU. this is used to turn on/off blue leds. MCU 
     also controls motors/arm/sensors/etc....
   * prdAddTask @0x000C9E70: Schedule a function to be run every XX hundreds of seconds.
   * AddHttpValue @0x0006C34C: Add key / value strings to be printed as output of current HTTP request result. 
   
 You can find more untested functions in rovio-fw/apis503.h
 
License:
  Do whatever you want, i'm doing this for fun. So let says it's GPL so improvements are at least shared.
   



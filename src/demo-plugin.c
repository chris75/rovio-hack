#include "rovio-fw/apis503.h"

/* Entry point for patch in RAM */


// Hook GetVersion API to do new stuff 
int MyGetVersion(void *R0, void *R1, void *R2, void *R3 );

// To put some debug info and read via GetVersio.cgi 
static char s_szDebugBuffer[256];
void InitPatch(void *R0, void *R1, void *R2, void *R3 )
{
  int i;
  unsigned long *pCode = (unsigned long *) FW503_GET_VERSION;
  // Init buffer 
  for (i =0 ; i < sizeof(s_szDebugBuffer) ; i++) 
    s_szDebugBuffer[i]=0;
 
  // patch GetVersion.cgi entry with a jump to my stuff  ldr pc,[pc+4]
  pCode[0] = 0xe51ff004; // ldr pc,[pc, #-4]
  pCode[1] = (unsigned long *) MyGetVersion; 
  
  /* Report everything ok  */
  
  AddHttpValue(R3,"Patch demo led installed","."); 
}

int MyGetVersion(void *R0, void *R1, void *R2, void *R3 )
{
   snprintf(s_szDebugBuffer,sizeof(s_szDebugBuffer),"Test %d,%d",12,34);
   AddHttpValue(R3,"Hook installed ",s_szDebugBuffer);  
   return 0;
}

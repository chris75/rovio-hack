#include "rovio-fw/apis503.h"


/* Entry point for patch in RAM */
void InitPatch( )

{
  
  /* Do some stuff */ 
}

int MyConfig_GetVer(void *R0, void *R1, void *R2, void *R3 ) 
{
  /* Call a firmware function */
  fw_AddHttpValue(R3,"Patch demo led installed","."); 

  return 0;
}


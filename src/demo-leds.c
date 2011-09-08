#include "rovio-fw/apis503.h"


/* Entry point for patch in RAM */
void InitPatch(void *R0, void *R1, void *R2, void *R3 )

{
  /* Do some stuff */ 
  /* Call a firmware function */
  fw_AddHttpValue(R3,"Patch demo led installed","."); 
  return 0;
}


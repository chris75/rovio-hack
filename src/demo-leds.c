#include "rovio-fw/apis503.h"

void mcuSimpleTestCommand(void *R3 );

/* Entry point for patch in RAM */
void InitPatch(void *R0, void *R1, void *R2, void *R3 )

{
  /* Do some stuff */ 
  /* Call a firmware function */
  fw_AddHttpValue(R3,"Patch demo led installed","."); 
  mcuSimpleTestCommand(R3);
}

void mcuSimpleTestCommand(void *R3 )
{
  char szCommand[] = "114D4D00010053485254000100011A150000";
  char szResponse[256];
  int rc;
  ICTL_HANDLE_T ictl;
  ictl.Privilege=AUTH_SYSTEM;
  
  rc = fw_ictlCtrlMCU(&ictl,szCommand,szResponse,sizeof(szResponse));
  if (rc != ICTL_OK) 
  {
    fw_AddHttpValue(R3,"MCU Send failed",".");
  }
  else
  {
    fw_AddHttpValue(R3,"MCU Send OK",".");
  }
}



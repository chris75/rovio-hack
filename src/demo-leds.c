#include "rovio-fw/apis503.h"

/* Some background function */
void MyTickFunc();
void mcuSimpleTestCommand(void *R3 );

/* Entry point for patch in RAM */

static PRD_TASK_T g_hTask ;
static long g_args=0;
void InitPatch(void *R0, void *R1, void *R2, void *R3 )

{
  /* Call a firmware function */
  fw_prdAddTask(&g_hTask,MyTickFunc,1000 ,0);
  /* Report everything ok  */
  
  fw_AddHttpValue(R3,"Patch demo led installed","."); 
  mcuSimpleTestCommand();
//  MyTickFunc(); 
}

void mcuSimpleTestCommand(void *R3 )
{
  char szCommand[] = "114D4D00010053485254000100011A150000"; 
  // 114D4D00010053485254000100011A120000 // 2 Front leds off only 
  char szResponse[256];
  int rc;
  ICTL_HANDLE_T ictl;
  ictl.Privilege=AUTH_SYSTEM;
  
  rc = fw_ictlCtrlMCU(&ictl,szCommand,szResponse,sizeof(szResponse));
  if (rc == ICTL_OK) 
  {
    fw_AddHttpValue(R3,"MCU Send OK",".");
  }
  else
  {
    fw_AddHttpValue(R3,"MCU Send failed",".");
  }
}

/* Increment ascii code of a char in GetVer message */
void MyTickFunc(void *pArg)
{
  char *pStr=0x70e003;
  *pStr+=1;
}


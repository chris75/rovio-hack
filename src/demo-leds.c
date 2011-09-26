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
  fw_prdAddTask(&g_hTask,MyTickFunc,100 ,0);
  /* Report everything ok  */
  
  fw_AddHttpValue(R3,"Patch demo led installed","."); 
  mcuSimpleTestCommand(R3);
}

void mcuSimpleTestCommand(void *R3 )
{
  char szCommand[] = "4D4D00010053485254000100011A150000"; 
  // 114D4D00010053485254000100011A120000 // 2 Front leds off only 
  char szResponse[256];
  int rc;
  ICTL_HANDLE_T ictl;
  ictl.Privilege=AUTH_SYSTEM;
  
  szResponse[0]=0;
  
  rc = fw_ictlCtrlMCU(&ictl,szCommand,szResponse,sizeof(szResponse));
  if (rc == ICTL_OK) 
  {
    if(szResponse[0]==0) 
    { 
      fw_AddHttpValue(R3,"Response unchanged",".");
    }
    fw_AddHttpValue(R3,"MCU Send OK",szResponse);
  }
  else
  {
    fw_AddHttpValue(R3,"MCU Send failed",".");
  }
}

static char *s_szCommands[]=
{ 
 "4D4D00010053485254000100011A080000",
 "4D4D00010053485254000100011A100000",
 "4D4D00010053485254000100011A200000",
 "4D4D00010053485254000100011A010000",
 "4D4D00010053485254000100011A020000",
 "4D4D00010053485254000100011A040000"
};

static int  s_iCount=0;
static int  s_iDir=1;

/* Increment ascii code of a char in GetVer message */
void MyTickFunc(void *pArg)
{

  char szResponse[256];
  int rc;
  ICTL_HANDLE_T ictl;
  ictl.Privilege=AUTH_SYSTEM;
  szResponse[0]=0;
  fw_ictlCtrlMCU(&ictl,s_szCommands[s_iCount],szResponse,sizeof(szResponse));
  if ( s_iCount <= 0)
  {
    s_iDir=1;
  }
  else
  {
    if (s_iCount>=5) 
      s_iDir=-1;
  }
  s_iCount += s_iDir;
}


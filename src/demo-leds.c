#include "rovio-fw/apis503.h"

/* Some background function */

void MyTickFunc();
/* Entry point for patch in RAM */

static PRD_TASK_T g_hTask ;
static long g_args=0;
void InitPatch(void *R0, void *R1, void *R2, void *R3 )

{
  /* Call a firmware function */
  fw_prdAddTask(&g_hTask,MyTickFunc,500 ,0);
  /* Report everything ok  */
  
  fw_AddHttpValue(R3,"Patch demo led installed","."); 
//  MyTickFunc(); 
}

/* Increment ascii code of a char in GetVer message */
void MyTickFunc()
{
  char *pStr=0x70e003;
  *pStr++;
}


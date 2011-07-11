#include "rovio-fw/apis503.h"

/* Patch Config_GetVer at 0x000709D8 */
/* int Config_GetVer(HTTPCONNECTION hConnection, LIST *pParamList, int iAction, XML *pReturnXML)*/
int Config_GetVer(void *R0, void *R1, void *R2, void *R3 ) 
{

  /* Call a firmware function */
  fw_AddHttpValue(R3,"MyGetVer","12345-12"); 

  return 0;
}

/* Patch Config_GetVer at 0x000709D8 */

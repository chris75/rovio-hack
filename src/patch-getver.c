#include "rovio-fw/apis503.h"

/* Patch Config_GetVer at 0x000709D8 */
/* int Config_GetVer(HTTPCONNECTION hConnection, LIST *pParamList, int iAction, XML *pReturnXML)*/
int Config_GetVer(void *R0, void *R1, void *R2, void *R3 ) 
{
  /* Check if PATCH was loaded in RAM if so call it */
  if(    ((char *)(ROVIO_RAM_MALLOC_BASE_ADDR))[0] == 'P' 
      && ((char *)(ROVIO_RAM_MALLOC_BASE_ADDR))[1] == 'A'
      && ((char *)(ROVIO_RAM_MALLOC_BASE_ADDR))[2] == 'T'
      && ((char *)(ROVIO_RAM_MALLOC_BASE_ADDR))[3] == 'C'
    )
  {
    /* Call a firmware function */
    fw_RovioPatch(R0,R1,R2,R3);
    fw_AddHttpValue(R3,"Patch called","."); 
  }
  else
  {
    /* Call a firmware function */
    fw_AddHttpValue(R3,"Patch not found","!"); 
  }

  return 0;
}

/* Patch Config_GetVer at 0x000709D8 */

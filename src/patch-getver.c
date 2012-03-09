#include "rovio-fw/apis503.h"

/* Patch Config_GetVer at 0x000709D8 */
/* int Config_GetVer(HTTPCONNECTION hConnection, LIST *pParamList, int iAction, XML *pReturnXML)*/
int Config_GetVer(void *R0, void *R1, void *R2, void *R3 ) 
{
  /* Check if PATCH was loaded in RAM if so call it */
  char *ptrMarker = (char *)(ROVIO_RAM_MALLOC_BASE_ADDR);
  if(    ptrMarker[0] == 'P' 
      && ptrMarker[1] == 'A'
      && ptrMarker[2] == 'T'
      && ptrMarker[3] == 'C'+1 /* Trigger init on 2nd GetVer call using brower => called twice for some reason */
    )
  {
      /* Call a firmware function */
      fw_RovioPatch(R0,R1,R2,R3);
      AddHttpValue(R3,"Inited","."); 
  }
  else
  {
    /* Call a firmware function */
    AddHttpValue(R3,"Plugin Not found","!"); 
  }
  /* Change last char of marker to avoid multiple invocation */
  ptrMarker[3]++;
  return 0;
}

/* Patch Config_GetVer at 0x000709D8 */

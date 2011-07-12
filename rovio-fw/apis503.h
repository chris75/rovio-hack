
/* Used ugly defs to inline call address */

//void AddHttpValue(XML *pReturnXML, const char *pcString, const char *pcValue)
#define fw_AddHttpValue ((void (*)( void *pReturnXML, const char *pcString, const char *pcValue )) 0x0006C34C)

//void prdAddTask(PRD_TASK_T *pHandle, void (*fnTask)(void *pArg), cyg_tick_count_t tTimeout, void *pArg);
#define fw_prdAddTask (((void (*)( void *pHandle, void *pFunc, unsigned long timeout, void *pArg )) 0x000C9E70)  //## TO CHECK

// void ledShowState_Ready() 
#define fw_letShowStateready (((void (*)( )) 0x0001234) //## NOT FOUND YET

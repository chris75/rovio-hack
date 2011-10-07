/* Constants  */

    /* System Address Map */

#define    GPIO_BA   0x7FF00300 /* GPIO Control */

    /* GPIOs */

/* GPIO-B Pins */
#define REG_GPIOB_OE		(GPIO_BA+0x30)   /* GPIO-B Pins Output Enable Control Register */
#define REG_GPIOB_DAT		(GPIO_BA+0x34)   /* GPIO-B Pins Data Register */
#define REG_GPIOB_STS		(GPIO_BA+0x38)   /* GPIO-B Pins Status Register */
#define REG_GPIOB_PE		(GPIO_BA+0x3c)   /* GPIO-B Pull-Up/Down Enable Control Register */


    /* LEDs  */ 

#define LED_GPIO_RED	 0x01000000
#define	LED_GPIO_GREEN	 0x02000000

/* Rovio patch constants */

#define ROVIO_RAM_MALLOC_BASE_ADDR      0x70e000 /* Where 'PATC" marker is store to indicate patch was loaded */
#define ROVIO_RAM_PATCH_BASE_ADDR       0x20     /* Entry point for patch */

/* Some function addresses for Firwmare 5.03 */

#define FW503_GET_VERSION 0x000709D8

/* Prototype for patch entry func */

#define fw_RovioPatch ((void (*) (void *R0,void *R1,void *R2, void *R3)) ROVIO_RAM_MALLOC_BASE_ADDR+ROVIO_RAM_PATCH_BASE_ADDR)

/* Rovio FW defines / types */
#include "rovio-types.h"

/* Prototypes for libc stuff */
int  snprintf(char *buf, size_t len, const char *fmt, ...);
void *malloc( size_t /* size */ );


/* Rovio functions in Firmware 5.03 : (Used ugly defs to inline call address ) */

//void AddHttpValue(XML *pReturnXML, const char *pcString, const char *pcValue)
void AddHttpValue( void *pReturnXML, const char *pcString, const char *pcValue );

//void prdAddTask(PRD_TASK_T *pHandle, void (*fnTask)(void *pArg), cyg_tick_count_t tTimeout, void *pArg);
void prdAddTask( void *pHandle, void *pFunc, unsigned long timeout, void *pArg );

// void ledShowState_Ready() 
void ledShowStateReady();

// void ledShowState_PoweredOn() 
void ledShowStatePoweredOn();

// void ledShowState_Error() 
void ledShowStateError();

// int mcuSendCommand(const void *pCmd, size_t szCmdLen, void *pResponse, size_t szResponseLen);
void mcuSendCommand() ;

//int ictlCtrlMCU(ICTL_HANDLE_T *pHandle, const char *pcCommand, char *pcResponse, size_t szMaxResponse);
int ictlCtrlMCU(ICTL_HANDLE_T *pHandle,const char * pcCommand, char *pcResponse,unsigned long );



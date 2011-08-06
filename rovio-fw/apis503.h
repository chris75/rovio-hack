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

/* Used ugly defs to inline call address */

//void AddHttpValue(XML *pReturnXML, const char *pcString, const char *pcValue)
#define fw_AddHttpValue ((void (*)( void *pReturnXML, const char *pcString, const char *pcValue )) 0x0006C34C)

//void prdAddTask(PRD_TASK_T *pHandle, void (*fnTask)(void *pArg), cyg_tick_count_t tTimeout, void *pArg);
#define fw_prdAddTask (((void (*)( void *pHandle, void *pFunc, unsigned long timeout, void *pArg )) 0x000C9E70)  

// void ledShowState_Ready() 
#define fw_ledShowStateReady (((void (*)( )) 0x0001234) //## TO FIX

// void ledShowState_PoweredOn() 
#define fw_ledShowStatePoweredOn (((void (*)( )) 0x000BDBD4) 

// void ledShowState_Error() 
#define fw_ledShowStateError     (((void (*)( )) 0x000BDAEC) 

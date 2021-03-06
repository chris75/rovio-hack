// Types and constants for Rovio firmware 


typedef long size_t;

typedef struct

{
	unsigned char ucLeading;	/* leading byte */
	unsigned char ucLength;		/* length byte, not include itself. */
	/*
	"II" = Little-endian, Intel mode
	"MM" = Big-endian, Motorola mode
	*/
	unsigned char aucEndian[2];	/* endian */
	unsigned char aucVersion[3];/* version */
	unsigned char aucCmd[4];	/* "SHRT" = ioCmd, indicate this packet is SHORT command. prefer in this version */
	unsigned char aucPackets[2];/* packets, always 0x0001 in this version */
	unsigned char aucDrive[2];	/* nDrive, should be 0x0001 in "SHRT" command */
	unsigned char ucDirection;	/* Direction Code, 0x02 = BACKWORD, defined in draft 0.2 */
	unsigned char ucSpeed;		/* Speed = level 4 */
	unsigned char aucPadding[2];/* padding bytes. */
	unsigned char aucChecksum[2];	/* checksum */
	unsigned char ucSuffix;			/* suffix byte. */

} MPU_CMD_T;

typedef unsigned long long cyg_tick_count_t;

typedef struct tagList
{
	struct tagList *pPrev;
	struct tagList *pNext;
} LIST_T;

typedef struct tagPRD_TASK
{
	void (*fnTask)(void *pArg);
	void *pArg;
	cyg_tick_count_t tTimeout;
	cyg_tick_count_t tRemain;
	LIST_T list;

} PRD_TASK_T;

typedef void *HTTPCONNECTION;

typedef struct tagLISTNODE

{
	void *pValue;
	struct tagLISTNODE *pPreNode;
	struct tagLISTNODE *pNextNode;
	struct tagLIST *pList;
} LISTNODE;

typedef struct tagLIST
{
	LISTNODE *pFirstNode;
	LISTNODE *pLastNode;
} LIST;


/* Define XML structure */
typedef struct tagXML
{
	struct tagXML *pParXML;
	LISTNODE *pParXMLNode;
	char *pcName;
	LIST *plAttrib;
	LIST *plSubXML;
} XML;

// 
#define ICTL_OK			0
#define ICTL_ERROR		(-1)
#define ICTL_UNAUTHORIZED	(-2)
#define ICTL_INVALID_PARAMETERS	(-3)

#define AUTH_ANY -1
#define AUTH_USER 0
#define AUTH_ADMIN 1
#define AUTH_SYSTEM 2

typedef struct {
    char Username[24];
    char Passwd[24];
    int Privilege;
}ICTL_HANDLE_T;





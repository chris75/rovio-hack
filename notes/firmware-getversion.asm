
GetVer.cgi => Addr: 0x0709D8

000709D8 Config_GetVer                           ; DATA XREF: off_86420o
000709D8                 STMFD   SP!, {R4,LR}
000709DC                 MOV     R4, R3
000709E0                 CMP     R2, #0
000709E4                 BEQ     l709FC
000709E8                 CMP     R2, #1
000709EC                 MOVLNE  R0, 0xFFFFFFFF
000709F0                 LDMNEFD SP!, {R4,PC}
000709F4
000709F4 l709F4                                  ; CODE XREF: Config_GetVer+38j
000709F4                 MOV     R0, #0
000709F8                 LDMFD   SP!, {R4,PC}
000709FC 709FC                                   ; CODE XREF: Config_GetVer+Cj
000709FC                 BL      WRGetProductVersion
00070A00                 MOV     R2, R0
00070A04                 MOV     R0, R4
00070A08                 LDR     R1, =aVersion
00070A0C                 BL      AddHttpValue
00070A10                 B       loc_709F4
00070A14 off_70A14       DCD aVersion            ; DATA XREF: Config_GetVer+30r
00070A14                                         ; "Version"

0008D9C8 WRGetProductVersion                     ; CODE XREF: Config_GetVer:loc_709FCp
0008D9C8                                         ; sub_F5AB4+10op ...
0008D9C8
0008D9C8 var_18          = -0x18
0008D9C8 var_14          = -0x14
0008D9C8 var_10          = -0x10
0008D9C8 var_C           = -0xC
0008D9C8
0008D9C8                 STMFD   SP!, {R4,LR}
0008D9CC                 LDR     R4, =unk_11A11C
0008D9D0                 SUB     SP, SP, #0x20
0008D9D4                 LDRB    R0, [R4]
0008D9D8                 CMP     R0, #0
0008D9DC                 BNE     loc_8DA1C
0008D9E0                 ADD     R3, SP, #0x28+var_18
0008D9E4                 ADD     R2, SP, #0x28+var_14
0008D9E8                 ADD     R1, SP, #0x28+var_10
0008D9EC                 ADD     R0, SP, #0x28+var_C
0008D9F0                 BL      WRGetProductVersionNum
0008D9F4                 LDR     R0, [SP,#0x28+var_18]
0008D9F8                 LDR     R1, =aRevision_0
0008D9FC                 LDR     R2, [SP,#0x28+var_C]
0008DA00                 LDR     R3, [SP,#0x28+var_10]
0008DA04                 STMEA   SP, {R0-R3}
0008DA08                 LDR     R3, [SP,#0x28+var_14]
0008DA0C                 LDR     R2, =aSSSD_D
0008DA10                 MOV     R1, #0x80 ; 'Ç'
0008DA14                 MOV     R0, R4
0008DA18                 BL      snprintf
0008DA1C
0008DA1C loc_8DA1C                               ; CODE XREF: WRGetProductVersion+14j
0008DA1C                 MOV     R0, R4
0008DA20                 ADD     SP, SP, #0x20
0008DA24                 LDMFD   SP!, {R4,PC}
0008DA24 ; End of function WRGetProductVersion
0008DA24
0008DA24 ; ---------------------------------------------------------------------------
0008DA28 off_8DA28       DCD unk_11A11C          ; DATA XREF: WRGetProductVersion+4r
0008DA2C off_8DA2C       DCD aRevision_0         ; DATA XREF: WRGetProductVersion+30r
0008DA2C                                         ; "$Revision: "
0008DA30 off_8DA30       DCD aSSSD_D             ; DATA XREF: WRGetProductVersion+44r
0008DA30                                         ; "%s %s %s%d.%d$"



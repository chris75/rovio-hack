SECTIONS {
  .text 0x70e020 : {
                         *(.text)
                         *(.rodata)
                         *(.rodata.*)
                         *(.glue_7)
                         *(.glue_7t)
                         *(.got)
                         *(.got.*)
                         }
  .data ALIGN(4): { *(.data)
                    *(.data.rel)
                    *(.data.rel.local)
                    __params_begin = .;
                     *(.data.param)
                            __params_end = .;
                    __commands_begin = .;
                    *(.data.commands)
                    __commands_end = .;
                  }
  .bss ALIGN(4):  { *(.bss)  *(COMMON) }
}


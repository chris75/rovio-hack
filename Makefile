CROSS_COMPILE=arm-none-eabi
AS=$(CROSS_COMPILE)-as
GCC=$(CROSS_COMPILE)-gcc
LD=$(CROSS_COMPILE)-ld
OBJCOPY=$(CROSS_COMPILE)-objcopy
OBJDUMP=$(CROSS_COMPILE)-objdump

CFLAGS=-O2 -g -I. -mcpu=xscale 

#LDFLAGS=-g --just-symbols=./minilib/fw503-symbols.ld
LDFLAGS=-g --just-symbols=./minilib/current-fw-symbols.ld

OBJS=objs/init.o 

all: rovio.local bin/patch-getver.bin bin/demo-leds.bin bin/demo-plugin.bin
	@echo " Compiled OK!"
	@echo " Now do a make on one of: demo-patch-firmware  demo-plugin"

include rovio.local

config-test: rovio.local
	@echo 
	@echo "Checking Rovio settings ..."
	@echo "  IP is  : "$(ROVIOIP)
	@echo "  User is: "$(ROVIOUSER)
	@echo "  Pwd  is: xxx"
	@echo 
	@echo "  Testing connection to Rovio"
	./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) get_version


rovio.local:
	@echo "You should copy rovio.local.sample to rovio.local and edit for your rovio settings"
	ls -l rovio.local


demo-patch-firmware:bin/patch-getver.bin bin/demo-leds.bin
	echo "Uploading fw patch with command: ./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) patch_fw bin/patch-getver.bin 0x000709D8 bin/blink-leds.bin 0x70e020"
	./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) patch_fw bin/patch-getver.bin 0x000709D8 bin/demo-leds.bin 0x70e020
	@echo "Done"

demo-plugin:bin/patch-getver.bin bin/demo-plugin.bin
	echo "Uploading fw patch with command: ./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) patch_fw bin/patch-getver.bin 0x000709D8 bin/demo-plugin.bin 0x70e020"
	./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) patch_fw bin/patch-getver.bin 0x000709D8 bin/demo-plugin.bin 0x70e020
	@echo "Done"

demo-patch-getver: bin/patch-getver upload_patch-getver
	@echo "Done"
	
minilib/stubs.o: minilib/stubs.asm
	$(AS) -o minilib/stubs.o minilib/stubs.asm 

bin/patch-getver.bin: src/patch-getver.c
	@echo
	@echo "Compiling patch-getver arm program to patch Rovio with"
	@echo "----------------------------------------------"
	@echo 
	$(GCC) $(CFLAGS) -c -o objs/patch-getver.o src/patch-getver.c
	$(LD) $(LDFLAGS) -Tminilib/rovio-getver.ld -Bstatic -o bin/patch-getver.elf objs/patch-getver.o
	$(OBJCOPY) -O binary -S bin/patch-getver.elf bin/patch-getver.bin 
	@echo
	@echo "Done."

bin/demo-leds.bin: objs/start.o objs/demo-leds.o 
	@echo "Linking demo-leds patch for Rovio"
	@echo "-----------------------------------"
	$(LD) $(LDFLAGS) -Tminilib/rovio-ram.ld -Bstatic -o bin/demo-leds.elf objs/start.o objs/demo-leds.o
	$(OBJCOPY) -O binary -S bin/demo-leds.elf bin/demo-leds.bin 
	@echo
	@echo "Done."

objs/demo-leds.o: src/demo-leds.c 
	@echo
	@echo "Compiling demo-leds patch for Rovio"
	@echo "-----------------------------------"
	$(GCC) $(CFLAGS) -c -o objs/demo-leds.o src/demo-leds.c


bin/demo-plugin.bin: objs/start.o objs/demo-plugin.o 
	@echo "Linking demo-plugin patch for Rovio"
	@echo "-----------------------------------"
	$(LD) $(LDFLAGS) -Tminilib/rovio-ram.ld -Bstatic -o bin/demo-plugin.elf objs/start.o objs/demo-plugin.o
	$(OBJCOPY) -O binary -S bin/demo-plugin.elf bin/demo-plugin.bin 
	@echo
	@echo "Done."

objs/demo-plugin.o: src/demo-plugin.c 
	@echo
	@echo "Compiling demo-plugin patch for Rovio"
	@echo "-----------------------------------"
	$(GCC) $(CFLAGS) -c -o objs/demo-plugin.o src/demo-plugin.c



objs/start.o: minilib/start.asm
	@echo
	@echo "Assemble startup code"
	@echo "---------------------"
	$(AS) -o objs/start.o minilib/start.asm

clean:
	rm objs/*
	rm bin/*

upload_patch-getver:
	@echo "Uploading with command:" ./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) write_mem 0x00070b24 file bin/patch-getver.bin
	./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) write_mem 0x00070b24 file bin/patch-getver.bin

showdump:
	$(OBJDUMP) -b elf32-littlearm -g -d bin/patch-getver.elf
	$(OBJDUMP) -b elf32-littlearm -g -d bin/demo-leds.elf
	$(OBJDUMP) -b elf32-littlearm -g -d bin/demo-plugin.elf

# Regenerate linker script from currently compiled firmware
generate-ld-script: 
	./scripts/lst2ldsym.py $(FIRMWARE_SYMBOL_FILE) minilib/current-fw-symbols.ld
	

CROSS_COMPILE=arm-none-eabi
AS=$(CROSS_COMPILE)-as
GCC=$(CROSS_COMPILE)-gcc
LD=$(CROSS_COMPILE)-ld
OBJCOPY=$(CROSS_COMPILE)-objcopy
OBJDUMP=$(CROSS_COMPILE)-objdump

CFLAGS=-O2 -I. -mcpu=xscale

OBJS=objs/init.o 

all: rovio.local bin/patch-getver demo-patch-firmware

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


demo-patch-firmware:bin/patch-getver bin/demo-leds.bin
	echo "Uploading fw patch with command: ./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) patch_fw bin/patch-getver.bin 0x000709D8 bin/blink-leds.bin 0x70e020"
	./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) patch_fw bin/patch-getver.bin 0x000709D8 bin/demo-leds.bin 0x70e020
	@echo "Done"

demo-patch-getver: bin/patch-getver upload_patch-getver
	@echo "Done"
	
minilib/stubs.o: minilib/stubs.asm
	$(AS) -o minilib/stubs.o minilib/stubs.asm 

bin/patch-getver:
	@echo
	@echo "Compiling patch-getver arm program to patch Rovio with"
	@echo "----------------------------------------------"
	@echo 
	$(GCC) $(CFLAGS) -c -o objs/patch-getver.o src/patch-getver.c
	$(LD) -Tminilib/rovio-getver.ld -Bstatic -o bin/patch-getver.elf objs/patch-getver.o
	$(OBJCOPY) -O binary -S bin/patch-getver.elf bin/patch-getver.bin 
	@echo
	@echo "Done."

bin/demo-leds.bin: src/demo-leds.c
	@echo
	@echo "Compiling demo-leds patch for Rovio"
	@echo "-----------------------------------"
	@echo 
	$(GCC) $(CFLAGS) -c -o objs/demo-leds.o src/demo-leds.c
	$(LD) -Tminilib/rovio-ram.ld -Bstatic -o bin/demo-leds.elf objs/demo-leds.o
	$(OBJCOPY) -O binary -S bin/demo-leds.elf bin/demo-leds.bin 
	@echo
	@echo "Done."

clean:
	rm objs/*
	rm bin/*

upload_patch-getver:
	@echo "Uploading with command:" ./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) write_mem 0x000709D8 file bin/patch-getver.bin
	./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) write_mem 0x000709D8 file bin/patch-getver.bin

showdump:
	$(OBJDUMP) -b elf32-littlearm -d bin/patch-getver.elf
	

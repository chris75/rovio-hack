CROSS_COMPILE=arm-none-eabi
AS=$(CROSS_COMPILE)-as
GCC=$(CROSS_COMPILE)-gcc
LD=$(CROSS_COMPILE)-ld
OBJCOPY=$(CROSS_COMPILE)-objcopy
OBJDUMP=$(CROSS_COMPILE)-objdump

CFLAGS=-O2 -I. -mcpu=xscale

OBJS=objs/init.o 

all: bin/patch-getver


demo-patch-firmware:bin/patch-getver bin/blink-leds.bin
	echo "Uploading fw patch with command: ./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) patch_fw bin/patch-getver.bin 0x000709D8 bin/blink-leds 0x70e020"
	./scripts/roviocmd.py $(ROVIOIP) $(ROVIOUSER) $(ROVIOPWD) patch_fw bin/patch-getver.bin 0x000709D8 bin/blink-leds 0x70e020
	@echo "Done"

demo-patch-getver: bin/patch-getver upload_patch-getver
	@echo "Done"
	
minilib/stubs.o: minilib/stubs.asm
	$(AS) -o minilib/stubs.o minilib/stubs.asm 

bin/patch-getver:
	@echo
	@echo "Compile patch-getver arm program to patch Rovio with"
	@echo "----------------------------------------------"
	@echo 
	$(GCC) $(CFLAGS) -c -o objs/patch-getver.o src/patch-getver.c
	$(LD) -Tminilib/rovio-getver.ld -Bstatic -o bin/patch-getver.elf objs/patch-getver.o
	$(OBJCOPY) -O binary -S bin/patch-getver.elf bin/patch-getver.bin 
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
	

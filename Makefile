CROSS_COMPILE=arm-none-eabi
AS=$(CROSS_COMPILE)-as
GCC=$(CROSS_COMPILE)-gcc
LD=$(CROSS_COMPILE)-ld
OBJCOPY=$(CROSS_COMPILE)-objcopy
OBJDUMP=$(CROSS_COMPILE)-objdump

CFLAGS=-O2 -I. -mcpu=xscale

OBJS=objs/init.o 

all: bin/sample
	
minilib/stubs.o: minilib/stubs.asm
	$(AS) -o minilib/stubs.o minilib/stubs.asm 

bin/sample:
	@echo
	@echo "Compile sample arm program to patch Rovio with"
	@echo "----------------------------------------------"
	@echo 
	$(GCC) $(CFLAGS) -c -o objs/sample.o src/sample.c
	$(LD) -Tminilib/rovio-getver.ld -Bstatic -o bin/sample.elf objs/sample.o
	$(OBJCOPY) -O binary -S bin/sample.elf bin/sample.bin 
	@echo
	@echo "Done."
clean:
	rm objs/*
	rm bin/*

upload_sample:
	./scripts/roviocmd.py $ROVIOIP $ROVIOUSER $ROVIOPWD write_mem 0x000709D8 file bin/sample.bin


showdump:
	$(OBJDUMP) -b elf32-littlearm -d bin/sample.elf
	

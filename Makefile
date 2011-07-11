CROSS_COMPILE=arm-none-eabi
AS=$(CROSS_COMPILE)-as
GCC=$(CROSS_COMPILE)-gcc
LD=$(CROSS_COMPILE)-ld
OBJCOPY=$(CROSS_COMPILE)-objcopy
OBJDUMP=$(CROSS_COMPILE)-objdump

CFLAGS=-I. -mcpu=xscale

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
	#$(GCC) -c -o objs/init.o minilib/init.c
	#$(AS) -o objs/stubs.o minilib/stubs.asm
	$(LD) -Tminilib/rovio.ld -Bstatic -o bin/sample.elf objs/sample.o
	$(OBJCOPY) -O binary -S bin/sample.elf bin/sample.bin 
	@echo
	@echo "Done."
clean:
	rm objs/*
	rm bin/*


showdump:
	$(OBJDUMP) -b elf32-littlearm -d bin/sample.elf
	

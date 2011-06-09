CROSS_COMPILE=arm-none-eabi
AS=$(CROSS_COMPILE)-as
GCC=$(CROSS_COMPILE)-gcc
LD=$(CROSS_COMPILE)-ld
OBJCOPY=$(CROSS_COMPILE)-objcopy
OBJDUMP=$(CROSS_COMPILE)-objdump


CFLAGS=-mcpu=xscale
OBJS=objs/init.o

all: bin/sample.bin

bin/sample.bin: src/sample.c rovio-fw/apis503.h
	-mkdir objs
	-mkdir bin
	$(GCC) -I . -c -o objs/sample.o src/sample.c
	$(LD) -Trovio.ld -Bstatic -o bin/sample.elf objs/sample.o
	$(OBJCOPY) -O binary -S bin/sample.elf bin/sample.bin
clean:
	rm objs/*
	rm bin/*

showdump:
	$(OBJDUMP) -b elf32-littlearm -d bin/sample.elf



CROSS_COMPILE=arm-none-eabi
AS=$(CROSS_COMPILE)-as

CFLAGS=-mcpu=xscale

minilib/stubs.o: minilib/stubs.asm
	$(AS) -o minilib/stubs.o minilib/stubs.asm 
all:
	@echo "Todo"

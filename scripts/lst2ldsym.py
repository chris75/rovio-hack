#!/usr/bin/python
import sys,os,re

""" Extract symbols address from ADS 1.2 lst file """
if len(sys.argv) != 3:
    print "Usage: lst2ldsym <lstfile.lst> <ldscript.ld>"
    raise SystemExit


re_symbol=re.compile("([^ ]+) +(0x[^ ]+) +(.*) +(.*)")


lst_file=open(sys.argv[1],"r")

lst_lines=lst_file.readlines()

print "Read %d lines \n"%len(lst_lines)


lds_out=open(sys.argv[2],"w")


lds_out.write("""
SECTIONS
{
""")

b_syms=False

for i in lst_lines:
    i = i.lstrip(" \n")
    if len(i)<2:
      continue
    if b_syms:
        res =re_symbol.match(i)
        if res:
            (sym,addr,sym_type)=res.groups()[0:3]
            if 'ARM' in sym_type and len(sym) < 30:
                lds_out.write("  %40s = %s;\n"%(sym,addr))
        elif i.startswith("==========="):
            break
    else:
      # Check if we have reach the symbol vs address section
      if i.find("Global Symbols")>=0:
          b_syms=True 

lds_out.write("}\n")     
lds_out.close() 

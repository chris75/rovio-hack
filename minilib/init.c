
int func(int i )
{
  ((void (*)()) 0x12345678)();
  return i+1;
}

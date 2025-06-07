// Generated MSIL code
.assembly extern mscorlib {}
.assembly generated_code {}

.method static int32 processValues(int32 x, char c, bool b) cil managed
{
  .locals init (int32 V_0)
  ldloc V_0
  ldc.i4 65
  add
  stloc V_0
  .locals init (char V_1)
  ldloc V_1
  ldc.i4 1
  add
  stloc V_1
  .locals init (bool V_2)
  ldloc V_2
  ldc.i4 5
  add
  stloc V_2
  .locals init (int32 V_3)
  ldc.i4 65
  stloc V_3
  .locals init (char V_4)
  ldc.i4 65
  stloc V_4
  .locals init (bool V_5)
  ldc.i4 5
  stloc V_5
  ldloc V_0
  ret
}

.method static void checkConditions(int32 x, char c) cil managed
{
  ldloc V_0
  ldc.i4 65
  cgt
  brfalse IL_0002
  .locals init (int32 V_0)
  ldloc V_0
  stloc V_0
IL_0002:
IL_0003:
  ldloc V_0
  ldc.i4 1
  cgt
  brfalse IL_0004
  ldloc V_0
  ldc.i4 1
  sub
  stloc V_0
  br IL_0003
IL_0004:
  .locals init (int32 V_1)
  ldc.i4 0
  stloc V_1
IL_0005:
  ldloc V_1
  ldc.i4 65
  clt
  brfalse IL_0006
  .locals init (int32 V_2)
  ldloc V_1
  ldc.i4 97
  add
  stloc V_2
  ldloc V_1
  br IL_0005
IL_0006:
  ret
}

.method static int32 check_count_of_params(int32 x, char c, bool b) cil managed
{
  ldloc V_0
  ldloc V_1
  add
  ldloc V_2
  add
  ret
}

.method static int32 main() cil managed
{
  .locals init (int32 V_0)
  ldc.i4 65
  stloc V_0
  .locals init (char V_1)
  ldc.i4 65
  stloc V_1
  .locals init (bool V_2)
  ldc.i4 5
  stloc V_2
  .locals init (bool V_3)
  ldc.i4 1
  stloc V_3
  ldc.i4 1
  ldc.i4 2
  ldc.i4 3
  ldc.i4 4
  ldc.i4 5
  ldc.i4 8
  ldc.i4 97
  ldc.i4 98
  ldc.i4 1
  .locals init (int32 V_4)
  call int32 generated_code::unexisting_function()
  stloc V_4
  .locals init (bool V_5)
  ldc.i4 1
  ldc.i4 2
  call int32 generated_code::check_count_of_params()
  stloc V_5
  .locals init (int32 V_6)
  ldc.i4 65
  ldc.i4 65
  ldc.i4 5
  call int32 generated_code::processValues()
  stloc V_6
  ldc.i4 1
  ldc.i4 65
  call int32 generated_code::checkConditions()
  ldc.i4 0
  ret
}

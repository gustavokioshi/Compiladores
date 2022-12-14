; ModuleID = "modulo.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

@"n" = common global i32 0, align 4
@"soma" = common global i32 0, align 4
define i32 @"main"()
{
"principal:entry":
  %".2" = alloca i32
  store i32 0, i32* %".2"
  store i32 10, i32* @"n"
  store i32 0, i32* @"soma"
  br label %"loop"
loop:
  %".7" = load i32, i32* @"soma"
  %".8" = load i32, i32* @"n"
  %".9" = add i32 %".7", %".8"
  store i32 %".9", i32* @"soma"
  %".11" = load i32, i32* @"n"
  %".12" = sub i32 %".11", 1
  store i32 %".12", i32* @"n"
  br label %"loop_val"
loop_val:
  %"a_cmp" = load i32, i32* @"n", align 4
  %".15" = icmp eq i32 %"a_cmp", 0
  br i1 %".15", label %"loop_end", label %"loop"
loop_end:
  %".17" = load i32, i32* @"soma"
  call void @"escrevaInteiro"(i32 %".17")
  br label %"exit"
exit:
  ret i32 0
}

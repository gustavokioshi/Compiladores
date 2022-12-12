; ModuleID = "modulo.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

@"n" = common global i32 0, align 4
@"soma" = common global i32 0, align 4
define i32 @"principal"()
{
entry:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  store i32 10, i32* @"n"
  store i32 0, i32* @"soma"
  br label %"loop"
loop:
  br label %"loop_val"
loop_val:
  %"a_cmp" = load i32, i32* @"n", align 4
  %".7" = icmp eq i32 %"a_cmp", 0
  br i1 %".7", label %"loop_end", label %"loop"
loop_end:
  br label %"exit"
exit:
  ret i32 0
}

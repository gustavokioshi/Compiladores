; ModuleID = "modulo.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

@"a" = common global i32 0, align 4
define i32 @"principal"()
{
entry:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"b" = alloca i32, align 4
  store i32 0, i32* %"b"
  store i32 10, i32* @"a"
  %".5" = load i32, i32* %"b"
  store i32 %".5", i32* %"b"
  br label %"exit"
exit:
  %".8" = load i32, i32* %"b"
  ret i32 %".8"
}

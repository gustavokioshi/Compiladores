; ModuleID = "modulo.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

define i32 @"main"()
{
"principal:entry":
  %".2" = alloca i32
  store i32 0, i32* %".2"
  %"x" = alloca i32, align 4
  store i32 0, i32* %"x"
  %"y" = alloca i32, align 4
  store i32 0, i32* %"y"
  store i32 0, i32* %"x"
  store i32 0, i32* %"y"
  %".8" = load i32, i32* %"x", align 4
  %".9" = call i32 @"leiaInteiro"()
  store i32 %".9", i32* %"x", align 4
  %".11" = load i32, i32* %"y", align 4
  %".12" = call i32 @"leiaInteiro"()
  store i32 %".12", i32* %"y", align 4
  %".14" = load i32, i32* %"x"
  call void @"escrevaInteiro"(i32 %".14")
  %".16" = load i32, i32* %"y"
  call void @"escrevaInteiro"(i32 %".16")
  br label %"exit"
exit:
  ret i32 0
}

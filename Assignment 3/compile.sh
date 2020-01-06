#!/bin/bash

echo ' Assembling with nasm'
nasm -f elf32 -o $1.o $1.asm

echo 'Success, Now Linking'
ld -o $1 $1.o

echo 'Go Ahead, may the force be with you'

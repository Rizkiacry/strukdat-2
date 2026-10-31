#!/bin/bash
# usage: build.sh file.cpp out  -> compile with shim (Turbo C++ -> g++), ASan/LSan on
f=$1; o=$2
sed 's/^void main()/int main()/; s/system(CLS)/putchar(12)/' "$f" > /home/claude/build/tmp.cpp
g++ -fpermissive -w -g -fsanitize=address -I/home/claude/shim /home/claude/build/tmp.cpp -o "$o"

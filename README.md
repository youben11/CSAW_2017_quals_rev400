# Sudo_root
-----------------------
# Reversing400 realism:

Did you know that x86 is really old? I found a really old Master Boot Record that I thought was quite interesting! At least, I think it's really old...

qemu-system-i386 -drive format=raw,file=main.bin
------------------------

We were provided with a [main.bin](https://github.com/youben11/CSAW_2017_quals_rev400/blob/master/main.bin) which seems to be a DOS/MBR boot sector, so we have to disassamble it as 16-bit assembly.

I first started it in qemu to have an idea of what going on, It prints some byte to the screen and wait for the user to type a flag of 20char length and check if the flag is correct (it prints wrong :p).

Then I started IDA to do some static analysis, the code was small since the MBR is limited to the size of 512bytes, the execution also start at the begining of the file wich is loaded at adr 0x7c00 (MBR stuff). After few readings, I realised that the important part of the code is in the range adr [0x066-0x0d3] the rest is some code for reading from the keyboard and printing the result and stuff like that, we will only focus on the important part (the entire assembly code is [there](https://github.com/youben11/CSAW_2017_quals_rev400/blob/master/main.ida) )

0066 cmp     byte ptr ds:7DC8h, 13h ; check if the flag_length is < 19 and read more if yes, otherwise start checking the flag

006B jle     loc_10D

006F cmp     dword ptr ds:1234h, 67616C66h ; compare the first char of the flag with "flag"

0078 jnz     loc_14D

008B mov     si, 8 ; prepare si for a loop

007C movaps  xmm0, xmmword ptr ds:1238h ; this load the 16 byte that follows "flag" into xmm0

0081 movaps  xmm5, xmmword ptr ds:7C00h ; this load the 16 first byte of the binary ( remember that MBR is loaded at adr 0x7c00 )

0086 pshufd  xmm0, xmm0, 1Eh ; this just change the position of the in xmm0

I didn't focused on how pshufd really work because I know that I can reorder the flag using my eyes and because I was very tired x)

after that is a loop of 8 iteration, if a check is not correct it will break and display wrong, if it can finish the 8 iteration, it will print correct, so what was this check ?

this is the begining of the loop:

008E movaps  xmm2, xmm0 ; move the changed flag to xmm2

0091 andps   xmm2, xmmword ptr [si+7D90h] ; this just switch two byte of xmm2 to 0x00 depending on the si

0096 psadbw  xmm5, xmm2 ; It will take me a lot to explain this intruction, please read the doc

from psadbw the computation of the 16byte flag will be devided (go read the doc), the result of each part must be equal to some bytes stored at 0x7da8-0x7dc8 at each iteration, this lead us to some equation : 

b8 + b7 + b6 + b5 + b4 + b3  +      abs(b1-cst1) = res1

b8 + b7 + b6 + b5 + b4 +      b2  + abs(b1-cst2) = res2

b8 + b7 + b6 + b5 +      b3 + b2  + abs(b1-cst3) = res3

b8 + b7 + b6 +      b4 + b3 + b2  + abs(b1-cst4) = res4

b8 + b7 +      b5 + b4 + b3 + b2  + abs(b1-cst5) = res5

b8 +      b6 + b5 + b4 + b3 + b2  + abs(b1-cst6) = res6

   b7 + b6 + b5 + b4 + b3 + b2  + abs(b1-cst7) = res7

with some linear algebra and some brute_force we can solve it, I used numpy to get this done [keygen.py](https://github.com/youben11/CSAW_2017_quals_rev400/blob/master/keygen.py)
there is two value for cst and dec, each one of them give 8byte independently, so just comment one of them

the first value of cst and dec give 10 possibilites but the first one seems to be the good one, after reorder of them it gives "{4r3alz_"

the second then give 9 possibilites, reading carefully, the 8th seems to be the good one, after reoredr of them it gives "m0d3_y0}"

the flag was "flag{4r3alz_m0d3_y0}"

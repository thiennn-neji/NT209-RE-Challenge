# CRACK_NASM
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `CrackMe_ASM`
```zsh
└─$ file CrackMe_ASM
CrackMe_ASM: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, not stripped
```
Đây là file thực thi trên linux `32-bit` và lưu trữ theo `Little endian (LSB)`
### Disassembly
Vì là file 32-bit nên mình dùng `IDA Pro` để disassembly. Sau đây là assembly của hàm `_start`
```asm
.text:08048080                 mov     eax, 4
.text:08048085                 mov     ebx, 1          ; fd
.text:0804808A                 mov     ecx, offset prom ; addr
.text:0804808F                 mov     edx, 7          ; len
.text:08048094                 int     80h             ; LINUX - sys_write
.text:08048096                 mov     eax, 3
.text:0804809B                 mov     ebx, 0          ; fd
.text:080480A0                 mov     ecx, offset var ; addr
.text:080480A5                 mov     edx, 0Bh        ; len
.text:080480AA                 int     80h             ; LINUX - sys_read
.text:080480AC                 mov     eax, offset flag
.text:080480B1                 mov     byte ptr [eax], 53h ; 'S'
.text:080480B4                 add     eax, 1
.text:080480B7                 mov     byte ptr [eax], 33h ; '3'
.text:080480BA                 add     eax, 1
.text:080480BD                 mov     byte ptr [eax], 43h ; 'C'
.text:080480C0                 add     eax, 1
.text:080480C3                 mov     byte ptr [eax], 72h ; 'r'
.text:080480C6                 add     eax, 1
.text:080480C9                 mov     byte ptr [eax], 45h ; 'E'
.text:080480CC                 add     eax, 1
.text:080480CF                 mov     byte ptr [eax], 2Bh ; '+'
.text:080480D2                 add     eax, 1
.text:080480D5                 mov     byte ptr [eax], 46h ; 'F'
.text:080480D8                 add     eax, 1
.text:080480DB                 mov     byte ptr [eax], 6Ch ; 'l'
.text:080480DE                 add     eax, 1
.text:080480E1                 mov     byte ptr [eax], 34h ; '4'
.text:080480E4                 add     eax, 1
.text:080480E7                 mov     byte ptr [eax], 47h ; 'G'
.text:080480EA                 add     eax, 1
.text:080480ED                 mov     byte ptr [eax], 21h ; '!'
```
Bài này cũng tương tự như [**nasm**](https://github.com/neji-uit/NT209-RE-Challenge/tree/main/nasm). So sánh chuỗi nhập vào (được lưu ở vùng nhớ có label **var**) với password có sẵn trong chương trình (vùng nhớ label **flag**)
```asm
.text:080480F0                 xor     ebx, ebx
.text:080480F2                 xor     ecx, ecx
.text:080480F4                 mov     ecx, ds:flag
.text:080480FA                 mov     ebx, ds:var
.text:08048100                 cmp     ecx, ebx
.text:08048102                 jnz     short failure
.text:08048104                 jmp     short success
```
Nhưng khi vào vùng nhớ `flag` thì vùng nhớ này hoàn toàn trống rỗng, không có gì. Vậy `flag` chỉ lưu dữ liệu khi chương trình khởi chạy.
### Answer
Nhìn lệnh đoạn assembly của `_start` thì có một đoạn nhập dữ liệu vào `flag`
Chuỗi password cần tìm chính là đoạn nhập vào `flag`, là `S3CrE+Fl4G!`
```asm
.text:080480AC                 mov     eax, offset flag
.text:080480B1                 mov     byte ptr [eax], 53h ; 'S'
.text:080480B4                 add     eax, 1
.text:080480B7                 mov     byte ptr [eax], 33h ; '3'
.text:080480BA                 add     eax, 1
.text:080480BD                 mov     byte ptr [eax], 43h ; 'C'
.text:080480C0                 add     eax, 1
.text:080480C3                 mov     byte ptr [eax], 72h ; 'r'
.text:080480C6                 add     eax, 1
.text:080480C9                 mov     byte ptr [eax], 45h ; 'E'
.text:080480CC                 add     eax, 1
.text:080480CF                 mov     byte ptr [eax], 2Bh ; '+'
.text:080480D2                 add     eax, 1
.text:080480D5                 mov     byte ptr [eax], 46h ; 'F'
.text:080480D8                 add     eax, 1
.text:080480DB                 mov     byte ptr [eax], 6Ch ; 'l'
.text:080480DE                 add     eax, 1
.text:080480E1                 mov     byte ptr [eax], 34h ; '4'
.text:080480E4                 add     eax, 1
.text:080480E7                 mov     byte ptr [eax], 47h ; 'G'
.text:080480EA                 add     eax, 1
.text:080480ED                 mov     byte ptr [eax], 21h ; '!'
```
## Execute
```zsh
└─$ ./CrackMe_ASM
Flag : S3CrE+Fl4G!
you are correct !
```

# ES CRACK
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `run.exe`
```zsh
└─$ file run.exe
run.exe: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, with debug_info, not stripped
```
Đây là file thực thi trên linux `32-bit` và lưu trữ theo `Little endian (LSB)`
Dù là đuôi `.exe` nhưng file thực thi trên linux :) 
### Disassembly
Mình dùng `IDA Pro` để disassembly
```asm
.text:08049000 ; void __48_1_()
.text:08049000                 public $_48_1_
.text:08049000 $_48_1_         proc near               ; DATA XREF: LOAD:08048018↑o
.text:08049000                                         ; LOAD:0804805C↑o
.text:08049000                 pop     ebx
.text:08049001                 pop     ebx
.text:08049002                 pop     ebx
.text:08049003                 mov     eax, dword ptr password ; "P455w0rd"
.text:08049008                 cmp     eax, [ebx]
.text:0804900A                 jz      short _start_goodjob
.text:0804900C                 jmp     short _start_wrong
.text:0804900E ; ---------------------------------------------------------------------------
.text:0804900E
.text:0804900E _start_goodjob:                         ; CODE XREF: $_48_1_+A↑j
.text:0804900E                 mov     eax, 4
.text:08049013                 mov     ebx, 1          ; fd
.text:08049018                 mov     ecx, offset goodjobText ; addr
.text:0804901D                 mov     edx, 0Eh        ; len
.text:08049022                 int     80h             ; LINUX - sys_write
.text:08049024                 jmp     short _start_end
.text:08049026 ; ---------------------------------------------------------------------------
.text:08049026
.text:08049026 _start_wrong:                           ; CODE XREF: $_48_1_+C↑j
.text:08049026                 mov     eax, 4
.text:0804902B                 mov     ebx, 1          ; fd
.text:08049030                 mov     ecx, offset nope ; addr
.text:08049035                 mov     edx, 7          ; len
.text:0804903A                 int     80h             ; LINUX - sys_write
.text:0804903C
.text:0804903C _start_end:                             ; CODE XREF: $_48_1_+24↑j
.text:0804903C                 mov     eax, 1
.text:08049041                 xor     ebx, ebx        ; status
.text:08049043                 int     80h             ; LINUX - sys_exit
.text:08049043 $_48_1_         endp ; sp-analysis failed
.text:08049043
.text:08049043 _text           ends
.text:08049043
```
Ở hàm `$_48_1_`, chương trình lấy ra từ stack 3 lần và lưu vào thanh ghi `EBX`, hay `EBX = (EBP - 2)`
Mà 
> `(EBP)     = old EBP`
> `(EBP - 1) = return Address`
> `(EBP - 2) = argv[1]`
Vậy nên chương trình nhận chuỗi vào từ tham số thứ nhất khi gõ lệnh thực thi chương trình (không phải sau khi gõ lệnh thực thi)
Chương trình so sánh chuỗi vào với chuỗi `P455w0rd`.
### Answer
Chuỗi password là `P455w0rd`
## Execute
```zsh
└─$ ./run.exe P455w0rd
You Got This!
```

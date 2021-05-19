# NASM
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `nasm`
```sh
└─$ file nasm
nasm: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
```
Đây là file thực thi trên linux `64-bit` và lưu trữ theo `Little endian (LSB)`
### Disassembly
Vì là file 64-bit nên mình dùng `IDA Pro 64-bit` để disassembly
```asm
.text:0000000000401028                 public _start
.text:0000000000401028 _start          proc near               ; DATA XREF: LOAD:0000000000400018↑o
.text:0000000000401028
.text:0000000000401028 ; FUNCTION CHUNK AT .text:0000000000401000 SIZE 00000028 BYTES
.text:0000000000401028
.text:0000000000401028                 mov     eax, 1
.text:000000000040102D                 mov     edi, 1          ; fd
.text:0000000000401032                 mov     rsi, offset msg1 ; "Enter your password: "
.text:000000000040103C                 mov     edx, 16h        ; count
.text:0000000000401041                 syscall                 ; LINUX - sys_write
.text:0000000000401043                 mov     eax, 0
.text:0000000000401048                 mov     edi, 0          ; fd
.text:000000000040104D                 mov     rsi, 402031h    ; buf
.text:0000000000401057                 mov     edx, 10h        ; count
.text:000000000040105C                 syscall                 ; LINUX - sys_read
.text:000000000040105E                 mov     rdi, offset passwd
.text:0000000000401068                 mov     rsi, 402031h
.text:0000000000401072                 mov     ecx, 0Bh
.text:0000000000401077                 repe cmpsb
.text:0000000000401079                 jz      short correct_func
.text:000000000040107B                 mov     eax, 1
.text:0000000000401080                 mov     edi, 1          ; fd
.text:0000000000401085                 mov     rsi, offset wrong ; buf
.text:000000000040108F                 mov     edx, 7          ; count
.text:0000000000401094                 syscall                 ; LINUX - sys_write
.text:0000000000401096                 mov     eax, 3Ch ; '<'
.text:000000000040109B                 mov     edi, 0          ; error_code
.text:00000000004010A0                 syscall                 ; LINUX - sys_exit
.text:00000000004010A0 _start          endp
```
Chương trình bắt đầu từ hàm `_start` nên mình sẽ tập trung vào phần assembly của hàm `_start`.
Tại câu lệnh `.text:000000000040104D`, chương trình gọi hàm nhận vào một chuỗi (có độ dài tối đa 16 kí tự kể cả endline) và lưu vào vùng nhớ ` (0x0000000000402031)`
### Compare
Phần mình tìm được **password** nằm tại đây
```asm
.text:000000000040105E                 mov     rdi, offset passwd
.text:0000000000401068                 mov     rsi, 402031h
.text:0000000000401072                 mov     ecx, 0Bh
.text:0000000000401077                 repe cmpsb
.text:0000000000401079                 jz      short correct_func
```
Hàm **repe cmpsb** được mô tả trong [Instruction Set Reference (4-558 Vol. 2B)](https://github.com/neji-uit/NT209-RE-Challenge/blob/main/Intel%C2%AE%2064%20and%20IA-32%20Architectures%20Software%20Developer%E2%80%99s%20Manual%20Combined%20Volumes%201,%202A,%202B,%202C,%202D,%203A,%203B,%203C,%203D,%20and%204.pdf) dùng để `Find non-matching bytes in [RDI] and [RSI]`
Vậy là đoạn chương trình sẽ so sánh từng byte tại địa chỉ lưu trong thanh ghi RDI (vùng nhớ lưu **chuỗi passwd** của chương trình) và thanh ghi RSI (**input**). Trả về 0 nếu không có kí tự nào khác nhau.
### Answer
Chuỗi password cần nhập chính là chuỗi được lưu tại vùng nhớ có label `passwd`, là `supersecret`
```asm
.data:0000000000402000 ; ===========================================================================
.data:0000000000402000
.data:0000000000402000 ; Segment type: Pure data
.data:0000000000402000 ; Segment permissions: Read/Write
.data:0000000000402000 _data           segment dword public 'DATA' use64
.data:0000000000402000                 assume cs:_data
.data:0000000000402000                 ;org 402000h
.data:0000000000402000 ; char msg1[]
.data:0000000000402000 msg1            db 'Enter your password: ',0
.data:0000000000402000                                         ; DATA XREF: LOAD:00000000004000C0↑o
.data:0000000000402000                                         ; _start+A↑o
.data:0000000000402016 ; char correct
.data:0000000000402016 correct         db 'Correct!',0Ah       ; DATA XREF: _start-1E↑o
.data:000000000040201F ; char wrong
.data:000000000040201F wrong           db 'Wrong!',0Ah         ; DATA XREF: _start+5D↑o
.data:0000000000402026 passwd          db 'supersecret'        ; DATA XREF: _start+36↑o
.data:0000000000402026 _data           ends
.data:0000000000402026
```
## Execute
```zsh
└─$ ./nasm
Enter your password: supersecret
Correct!
```

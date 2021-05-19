# HELLO
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `hello`
```zsh
└─$ file hello
hello: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
```
Đây là file thực thi trên linux `64-bit` và lưu trữ theo `Little endian (LSB)`
### Disassembly
#### Vùng `.data`
```asm
.data:0000000000402000 ; ===========================================================================
.data:0000000000402000
.data:0000000000402000 ; Segment type: Pure data
.data:0000000000402000 ; Segment permissions: Read/Write
.data:0000000000402000 _data           segment dword public 'DATA' use64
.data:0000000000402000                 assume cs:_data
.data:0000000000402000                 ;org 402000h
.data:0000000000402000 ; char msg[]
.data:0000000000402000 msg             db 'Please enter your name: ',0
.data:0000000000402000                                         ; DATA XREF: LOAD:00000000004000C0↑o
.data:0000000000402000                                         ; _start+A↑o
.data:0000000000402019 hello           db 'Hello ',0           ; DATA XREF: _start+47↑r
.data:0000000000402020 ; char prompt[]
.data:0000000000402020 prompt          db 'Enter your Password: ',0
.data:0000000000402020                                         ; DATA XREF: _start+8A↑o
.data:0000000000402036 ; char wrong[]
.data:0000000000402036 wrong           db 1Bh,'[31mWrong Credentials, GTFO',0
.data:0000000000402036                                         ; DATA XREF: _start+101↑o
.data:0000000000402053 ; char success[]
.data:0000000000402053 success         db 1Bh,'[32mGreat H4x0r Skillz!!!!!',0
.data:0000000000402053                                         ; DATA XREF: _start+E4↑o
.data:0000000000402070 ret_code        db    0                 ; DATA XREF: _start:_start_error↑w
.data:0000000000402070                                         ; _start+121↑o
.data:0000000000402070 _data           ends
.data:0000000000402070
```
Chương trình yêu cầu mình nhập vào `name` và `Password` và sẽ báo về kết quả
```asm
> Wrong Credentials (nếu sai)
> Great H4x0r Skillz!!!!! (nếu đúng)
```
Vì là file 64-bit nên mình dùng `IDA Pro 64-bit` để disassembly. Nhìn qua qua có nhiều nhánh thực thi nên mình dùng chế độ xem `pseudocode`
#### Hàm `start`
```c
void __noreturn start()
{
  signed __int64 v0; // rax
  __int64 v1; // rax
  signed __int64 v2; // rax
  signed __int64 v3; // rax
  signed __int64 v4; // r15
  signed __int64 v5; // rax
  signed __int64 v6; // rax
  signed __int64 v7; // rax

  v0 = sys_write(1u, msg, 0x19uLL);
  v1 = sys_read(0, buf, 0x20uLL);
  if ( v1 < 0 )
  {
    ret_code = v1;
    goto _start_exit;
  }
  *(_QWORD *)welcome = *(_QWORD *)hello;
  *(_QWORD *)&welcome[6] = *(_QWORD *)buf;
  v2 = sys_write(1u, welcome, v1 + 6);
  v3 = sys_write(1u, prompt, 0x16uLL);
  v4 = sys_read(0, buf, 0x20uLL) - 1;
  while ( welcome[v4 + 5] + 5 == byte_402073[v4] )
  {
    if ( !--v4 )
    {
      v5 = sys_write(1u, success, 0x18uLL);
_start_exit:
      v7 = sys_exit((int)&ret_code);
      JUMPOUT(0x40112DLL);
    }
  }
  v6 = sys_write(1u, wrong, 0x18uLL);
  goto _start_exit;
}
```
#### Phần 1 của start, input/output
Đầu tiên chương trình in ra các lời chào và nhận chuỗi nhập vào từ `console`.
```c
  v0 = sys_write(1u, msg, 0x19uLL);
  v1 = sys_read(0, buf, 0x20uLL);
  if ( v1 < 0 )
  {
    ret_code = v1;
    goto _start_exit;
  }
  *(_QWORD *)welcome = *(_QWORD *)hello;
  *(_QWORD *)&welcome[6] = *(_QWORD *)buf;
  v2 = sys_write(1u, welcome, v1 + 6);
  v3 = sys_write(1u, prompt, 0x16uLL);
  v4 = sys_read(0, buf, 0x20uLL) - 1;
```
Chương trình nhận vào `name` lưu ở vùng nhớ `buf`.
Sau đó in ra câu chào `hello {name}`, chuyển dữ liệu ở `name` sang `welcome`.
Tiếp theo, chương trình nhận vào `Password` và lưu ở vùng nhớ `buf`.
Vậy,
> `name` lưu ở `welcome[6]` trở đi. Vì `welcome` = "hello" + `name`
> `Password` lưu ở `buf` trở đi
#### Phần 2 của start: kiểm tra `name` và `Password`
```c
v4 = sys_read(0, buf, 0x20uLL) - 1;
  while ( welcome[v4 + 5] + 5 == byte_402073[v4] )
  {
    if ( !--v4 )
    {
      v5 = sys_write(1u, success, 0x18uLL);
_start_exit:
      v7 = sys_exit((int)&ret_code);
      JUMPOUT(0x40112DLL);
    }
  }
  v6 = sys_write(1u, wrong, 0x18uLL);
  goto _start_exit;
```
`sys_read` trả về số lượng kí tự đã nhận vào của chuỗi từ console, bao gồm cả kí tự `NULL` hay `\0`.
Nên `v4 = {sys_read} - 1` là độ dài của chuỗi `Password`, không bao `NULL` hay `\0`. Chuỗi `Password` có ít nhất 1 kí tự nên **`v4 >= 1`**
> `welcome` bắt đầu tại 0x402094
> `buf` bắt đầu tại 0x402074
> `byte_402073` nằm tại 0x402073

`byte_402073[1]` tương đương với `buf[0]` hay `Password[0]`
`welcome[6]` tương đương với `name[0]`
Vậy câu pseudocode 
```c
while ( welcome[v4 + 5] + 5 == byte_402073[v4] )
```
tương đương với việc kiểm tra `name[i] + 5 == Password[i]` cho đến khi gặp kí tự `NULL`
### Answer
`name` và `Password` có độ dài bằng nhau và liên hệ với nhau qua công thức `name[i] + 5 == Password[i]`.
Chọn `name` và `password` có độ dài bằng 1 cho đơn giản.
> `name` = 'a'
> `Password` = 'a' + 5 = 'f'
## Execute
```zsh
└─$ ./hello
Please enter your name: a
Hello a
Enter your Password: f
Great H4x0r Skillz! 
```

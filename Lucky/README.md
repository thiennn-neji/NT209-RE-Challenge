
# LUCKY
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `lucky_nb`
```sh
└─$ file lucky_nb           
lucky_nb: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, stripped
```
Đây là file thực thi trên linux `32-bit` và lưu trữ theo `Little endian (LSB)`
### Disassembly
Mình dùng `IDA Pro` để disassembly
#### Hàm `start`
```asm
.text:0804903A start           proc near               ; DATA XREF: LOAD:08048018↑o
.text:0804903A
.text:0804903A ; FUNCTION CHUNK AT .text:0804901D SIZE 0000001D BYTES
.text:0804903A
.text:0804903A                 mov     eax, 4
.text:0804903F                 mov     ebx, 1          ; fd
.text:08049044                 mov     ecx, offset aLuckyNumbers ; addr
.text:08049049                 mov     edx, 0Fh        ; len
.text:0804904E                 int     80h             ; LINUX - sys_write
.text:08049050                 mov     eax, 3
.text:08049055                 mov     ebx, 2          ; fd
.text:0804905A                 mov     ecx, offset byte_804A024 ; addr
.text:0804905F                 mov     edx, 2          ; len
.text:08049064                 int     80h             ; LINUX - sys_read
.text:08049066                 mov     al, ds:byte_804A024
.text:0804906B                 sub     al, 30h ; '0'
.text:0804906D                 mov     bl, ds:byte_804A025
.text:08049073                 sub     bl, 30h ; '0'
.text:08049076                 adc     al, bl
.text:08049078                 daa
.text:08049079                 add     bl, 30h ; '0'
.text:0804907C                 cmp     al, 16h
.text:0804907E                 jnz     short sub_8049000
.text:08049080                 cmp     bl, 38h ; '8'
.text:08049083                 jnz     sub_8049000
.text:08049089                 cmp     eax, eax
.text:0804908B                 jz      short loc_804901D
.text:0804908B start           endp
```
#### Input
Chương trình nhập vào một chuỗi có 2 kí tự (không bao gồm kí tự `NULL` và `\r`|`\n`|`\r\n`). Dựa vào tên bài thì có thể đây là 2 kí tự số, đại diện cho số có 2 chữ số. Hai kí tự này được lưu vào `byte_804A024` và `byte_804A025`
```asm
.text:08049050                 mov     eax, 3
.text:08049055                 mov     ebx, 2          ; fd
.text:0804905A                 mov     ecx, offset byte_804A024 ; addr
.text:0804905F                 mov     edx, 2          ; len
.text:08049064                 int     80h             ; LINUX - sys_read
```
Sau đó, hai kí tự số này được `load` vào thanh ghi `AL` và `BL`. Và chương trình trừ các kí tự này cho `0x30` hay `'0'` để được số nguyên mà kí tự đó biểu diễn. Vì các kí tự này biểu diễn số nguyên nên đều lớn hơn `0x30` nên **cờ `CF` sẽ không bật (hay `CF = 0`)**
```asm
.text:08049066                 mov     al, ds:byte_804A024
.text:0804906B                 sub     al, 30h ; '0'
.text:0804906D                 mov     bl, ds:byte_804A025
.text:08049073                 sub     bl, 30h ; '0'
```
#### Kí tự số thứ hai
Đây là các câu lệnh sau khi thực hiện phép trừ cho `0x30` ở trên. Chú ý, thanh ghi `BL` sau khi trừ cho `0x30` ở trên, tiếp tục được cộng lại `0x30` và so sánh với `0x38` (hay `'8'`).
> Tức là `BL` trở lại giá trị bằng input ban đầu

Nếu như không bằng sẽ nhảy đến `sub_8049000` (sai Lucky number). Vậy `BL` ban đầu phải là `'8'` hay kí tự số thứ 2 chính là `'8'`.
```asm
.text:08049076                 adc     al, bl
.text:08049078                 daa
.text:08049079                 add     bl, 30h ; '0'
.text:0804907C                 cmp     al, 16h
.text:0804907E                 jnz     short sub_8049000
.text:08049080                 cmp     bl, 38h ; '8'
.text:08049083                 jnz     sub_8049000
```
### `ADC` instruction
Lệnh `adc` là lệnh cộng với carry, nghĩa là 
```asm
adc al, bl <=> al = al + bl + CF
```
>`CF` chính là cờ CF đó : )

và lệnh này sẽ tác động đến 2 cờ mà mình quan tâm, là CF và AF.
Trong các câu lệnh này thực thi trên thanh ghi 8-bit là `AL` và `BL`
* `CF` sẽ bật nếu như 
	* Khi cộng hai số 8-bit với nhau mà "tràn" ra bit thứ 9, hoặc
	* Khi trừ hai số 8-bit mà cần mượn từ bit thứ 9
* `AF` sẽ bật nếu như
	* Khi cộng hai số, mà có "nhớ" từ 4 bits thấp sang 4 bits cao, hoặc
	* Khi trừ hai số mà có "mượn" từ 4 bits cao sang 4 bits thấp

|   1st operand   |    2nd operand   |      Sum     |  CF |  AF |
|-----------------|------------------|--------------|-----|-----|
| 0010 1101 (45)  |  0100 1000 (72)  |  0 0011 1001 |   0 |   1 |
| 1010 1101 (173) |  1100 1000 (200) |  **1** 0111 0101 |   1 |   1 |

**Bây giờ câu hỏi cần quan tâm là cần phải bật cờ CF hay AF, hay cả hai? Và vì sao?**
### `DAA` instruction
Hàm **DAA** được mô tả trong [Instruction Set Reference (3-310 Vol. 2A)](https://github.com/neji-uit/NT209-RE-Challenge/blob/main/Intel%C2%AE%2064%20and%20IA-32%20Architectures%20Software%20Developer%E2%80%99s%20Manual%20Combined%20Volumes%201,%202A,%202B,%202C,%202D,%203A,%203B,%203C,%203D,%20and%204.pdf)
dùng để chỉnh sửa các giá trị bit trên thanh ghi `AL` để biểu diễn số BCD. Các bạn có thể đọc cụ thể. Ở đây mình chỉ mô tả lệnh này hoạt động như nào
```
- If the AL register is greater than 0x99, OR the Carry flag is SET, then

    The upper four bits of the Correction Factor are set to 6,
    and the Carry flag (CF) will be SET.
  Else
    The upper four bits of the Correction Factor are set to 0,
    and the Carry flag will be CLEARED.


- If the lower four bits of the AL register (AL AND 0x0F) is greater than 9,
  OR the Half-Carry flag (AF) is SET, then

    The lower four bits of the Correction Factor are set to 6.
  Else
    The lower four bits of the Correction Factor are set to 0.


- This results in a Correction Factor of 0x00, 0x06, 0x60 or 0x66.


- If the N flag is CLEAR, then

    ADD the Correction Factor to the AL register.
  Else
    SUBTRACT the Correction Factor from the AL register.
```
Trong bài này `NF (N flag) = 0`,
nên ta sẽ lấy `AL` sau khi thực hiện lệnh `ADC` cộng với một trong 4 `Correction Factor` tương ứng là `0x00, 0x06, 0x60 or 0x66`
Sau khi thực hiện cộng thì `AL` phải bằng `0x16`

Các con số mình thao tác ở đây là 8-bit và không dấu nên để được `0x16` thì cần phải cộng `AL` với `0x00` hoặc `0x06`

##### **Case 1: 0x00**
`AL` sau khi thực hiện lệnh `ADC` có giá trị là `0x16` và `CF = 0` và `AF = 0`.
Nhưng `AL` và `BL` trước khi thực hiện lệnh `ADC` chỉ có giá trị nằm trong `[0; 9]` nên không thể nào cộng lại ra `> 18 hay > 0x12`
> Bỏ case này

##### **Case 2: 0x06**
`AL` sau khi thực hiện lệnh `ADC` có giá trị là `0x10` và `CF = 0` và `AF = 1`.
Vì `BL = 8` như mình đã giải thích [ở đây](s) nên `AL = 8`
### Answer
Lucky number cần nhập là chuỗi `88`

## Execute
```zsh
└─$ ./lucky_nb        
Lucky Numbers: 88
Good Job !
```

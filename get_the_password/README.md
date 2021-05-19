# GET_THE_PASSWORD
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `crackme1.EXE`
```zsh
└─$ file crackme1.EXE
crackme1.EXE: PE32 executable (console) Intel 80386, for MS Windows
```
Đây là file thực thi trên giao diện consolde của Windows, `32-bit` 
### Disassembly
Mình dùng `IDA Pro` để disassembly.
#### Hàm `start`
```c
void __noreturn start()
{
  char v0; // cl
  int v1; // edx
  char *v2; // esi
  char v3; // al

  hConsoleInput = GetStdHandle(0xFFFFFFF6);
  hConsoleOutput = GetStdHandle(0xFFFFFFF5);
  WriteConsoleA(hConsoleOutput, aEnterPassword, 0x11u, 0, 0);
  ReadConsoleA(hConsoleInput, &unk_402010, 0x64u, &NumberOfCharsRead, 0);
  v0 = 0;
  v1 = 0;
  v2 = (char *)&unk_402010;
  while ( 1 )
  {
    while ( 1 )
    {
      v3 = *v2++;
      if ( v3 == 13 )
        goto LABEL_32;
      if ( ++v0 != 1 )
        break;
      ++v1;
      if ( (unsigned __int8)v3 <= 'G' )
        --v1;
    }
    switch ( v0 )
    {
      case 2:
        ++v1;
        if ( v3 >= 'm' )
          --v1;
        break;
      case 3:
        ++v1;
        if ( v3 != 'V' )
          --v1;
        break;
      case 4:
        ++v1;
        if ( (unsigned __int8)v3 < 'f' )
          --v1;
        break;
      case 5:
        ++v1;
        if ( (unsigned __int8)v3 > '3' )
          --v1;
        break;
      case 6:
        ++v1;
        if ( (unsigned __int8)v3 <= 'y' )
          --v1;
        break;
      case 7:
        ++v1;
        if ( v3 < '8' )
          --v1;
        break;
      case 8:
        ++v1;
        if ( v3 >= 'N' )
          --v1;
        break;
      case 9:
        ++v1;
        if ( v3 == 'R' )
          --v1;
        break;
      default:
        ++v1;
        if ( v3 != '2' )
          --v1;
LABEL_32:
        if ( v1 == 10 )
          WriteConsoleA(hConsoleOutput, aPasswordIsCorr, 0x18u, 0, 0);
        else
          WriteConsoleA(hConsoleOutput, aWrongPassword, 0x10u, 0, 0);
        ExitProcess(0);
    }
  }
}
```
Chương trình sẽ lưu chuỗi người dùng nhập vào vùng nhớ `unk_402010` hay `0x402010`. Biến `v2` lưu địa chỉ bắt đầu của vùng nhớ này,  tức là `&Password[0]`
#### Phần 1: Vòng lặp while-nhỏ
```c
v0 = 0;
v1 = 0;
v2 = (char *)&unk_402010;
...
    while ( 1 )
    {
      v3 = *v2++;
      if ( v3 == 13 )
        goto LABEL_32;
      if ( ++v0 != 1 )
        break;
      ++v1;
      if ( (unsigned __int8)v3 <= 'G' )
        --v1;
    }
```
Vòng lặp while-nhỏ này kiểm tra `v3`, hay kí tự hiện tại của `Pasword`, hay`Password[i]`. Nếu `v3 == 13` (kí tự `\r`) hoặc `v0!= 1` thì vòng lặp `break`.
Khởi tạo `v0 = 0` nên while-nhỏ **lặp 2 lần**.
Sau đó, mỗi lần lặp của while-lớn thì `v0` luôn khác 0 nên while-nhỏ chỉ lặp **một lần** để kiểm tra đến kí tự `\r` chưa.
Mỗi lần lặp của while-nhỏ tăng `v2` lên 1, tức là lấy kí tự tiếp theo trong chuỗi `Password`
#### Phần 2: switch-case
```c
switch ( v0 )
    {
      case 2:
        ++v1;
        if ( v3 >= 'm' )
          --v1;
        break;
      case 3:
        ++v1;
        if ( v3 != 'V' )
          --v1;
        break;
      case 4:
        ++v1;
        if ( (unsigned __int8)v3 < 'f' )
          --v1;
        break;
      case 5:
        ++v1;
        if ( (unsigned __int8)v3 > '3' )
          --v1;
        break;
      case 6:
        ++v1;
        if ( (unsigned __int8)v3 <= 'y' )
          --v1;
        break;
      case 7:
        ++v1;
        if ( v3 < '8' )
          --v1;
        break;
      case 8:
        ++v1;
        if ( v3 >= 'N' )
          --v1;
        break;
      case 9:
        ++v1;
        if ( v3 == 'R' )
          --v1;
        break;
      default:
        ++v1;
        if ( v3 != '2' )
          --v1;
LABEL_32:
        if ( v1 == 10 )
          WriteConsoleA(hConsoleOutput, aPasswordIsCorr, 0x18u, 0, 0);
        else
          WriteConsoleA(hConsoleOutput, aWrongPassword, 0x10u, 0, 0);
        ExitProcess(0);
    }
```
Trước khi vào `switch`, nếu kí tự đầu tiên trong chuỗi `Password`, `Password[0] > 'G'` thì `v1 = 1`.
Chương trình in ra `PasswordIsCorr` khi `v1 = 10`, hay là ta phải duyệt qua tất cả các case. **Điều này xảy khi `Password` có 10 kí tự**
Đặc biệt, các kí tự không được thỏa điều kiện trong `if` ở mỗi `case`, vì khi đó `v1` giảm đi 1.
### Answer
Ta có bảng mối liên hệ giữa các kí tự trong chuỗi `Password` để có được password đúng:
```c
Password[0]  >  'G'
Password[1]  <  'm'
Password[2]  == 'V'
Password[3]  >= 'f'
Password[4]  <= '3'
Password[5]  >  'y'
Password[6]  >= '8'
Password[7]  <  'N'
Password[8]  != 'R'
Password[9]  == '2'
```
Vậy 1 chuỗi `Password` là `HlVg2z9Ma2`
## Execute
```cmd
~ get_the_password>crackme1.EXE
Enter password:  HlVg2z9Ma2
Password is correct! ;)
```

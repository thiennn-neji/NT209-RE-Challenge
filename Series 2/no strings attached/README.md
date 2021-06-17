# no strings attached

## Solution

### Architecture

Dùng lệnh `file` để xác định kiến trúc của file thực thi `crackme.exe`

```zsh
└─$ file crackme.exe
crackme.exe: PE32 executable (console) Intel 80386, for MS Windows
```

Đây là file thực thi trên giao diện `console` `Windows 32-bit`

### Disassembly

Sử dụng IDA Pro để đọc pseudocode

#### Hàm `main`:

```c
int __cdecl main_0(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  char v5[108]; // [esp+14h] [ebp-E0h] BYREF
  char in_password[36]; // [esp+80h] [ebp-74h] BYREF
  char correct_message[16]; // [esp+A4h] [ebp-50h] BYREF
  char wrong_message[24]; // [esp+B4h] [ebp-40h] BYREF
  char Str[24]; // [esp+CCh] [ebp-28h] BYREF
  int v10; // [esp+F0h] [ebp-4h]

  strcpy(Str, "Enter password: ");
  strcpy(wrong_message, "WRONG PASSWORD");
  strcpy(correct_message, "CORRECT");
  sub_BB12D0(std::cout, Str);
  sub_BB10C8();
  v10 = 0;
  sub_BB10AF(std::cin, in_password);
  sub_BB1352(v5);
  LOBYTE(v10) = 1;
  sub_BB12C1(in_password);
  if ( (unsigned __int8)sub_BB1438(v5) )
    v3 = sub_BB12D0(std::cout, correct_message);
  else
    v3 = sub_BB12D0(std::cout, wrong_message);
  std::ostream::operator<<(v3, sub_BB13C5);
  while ( !std::ios_base::eof((std::ios_base *)(*(_DWORD *)(std::cin + 4) + std::cin)) )
    ;
  LOBYTE(v10) = 0;
  sub_BB1177(v5);
  v10 = -1;
  sub_BB1343(in_password);
  return 0;
}
```

**Các biến đã được đổi tên để dễ debug**

Chương trình nhận `password` từ console và lưu vào biến `in_password`.

#### Discrete string

Chương trình tiếp tục khởi tạo mảng/chuỗi `v5` như sau (hàm `sub_BB1352` gọi hàm `sub_BB3A60`)

```c
_DWORD *__thiscall sub_BB3A60(_DWORD *this)
{
  *this = 'e';
  this[1] = 'n';
  this[2] = 'c';
  this[3] = 'r';
  this[4] = 'y';
  this[5] = 'p';
  this[6] = 't';
  this[7] = 'e';
  this[8] = 'd';
  this[9] = '-';
  this[10] = 'c';
  this[11] = '-';
  this[12] = 's';
  this[13] = 't';
  this[14] = 'r';
  this[15] = 'i';
  this[16] = 'n';
  this[17] = 'g';
  sub_BB10C8();
  return this;
}
```

Vì kiểu dữ liệu đầu vào là `_DWORD` nên các phần tử này là `4-byte align`. Do đó sau khi thực hiện xong hàm, mảng `v5` chứa các kí tự cách nhau 4 bytes, là một chuỗi rời rạc. Nếu `align 1 byte` thì được chuỗi `encrypted-c-string`.
Đây có vẻ là chuỗi thú vị, và nó chính là `password` cần tìm.

#### Kiểm tra chuỗi đầu vào

Để chương trình có thể in ra chuỗi `correct_message` thì điều kiện `if ( (unsigned __int8)sub_BB1438(v5) )` phải `true`. Đi vào phân tích hàm `sub_BB1438` và qua các lời gọi hàm lần lượt, ta được

```c
char __thiscall sub_BB63D0(char *this)
{
  int i; // [esp+0h] [ebp-Ch]

  if ( sub_BB1645(this + 72, 0xCCCCCCCC) != 18 )
    return 0;
  for ( i = 0; i < 18; ++i )
  {
    if ( *(char *)sub_BB164A(i) != this[4 * i] )
      return 0;
  }
  return 1;
}
```

Đầu tiên tại điều kiện `if ( sub_BB1645(this + 72, 0xCCCCCCCC) != 18 )` chính là đang kiểm tra độ dài `password` được nhập. Suy ra `password` dài 18 kí tự.
Tiếp theo vòng lặp `for` sẽ kiểm tra từng kí tự của `password` (`*(char *)sub_BB164A(i)`) với từng kí tự trong mảng `v5` (lúc này con trỏ `this` là kiểu `char*` còn mảng `v5` được lưu theo kiểu `_DWORD` (4 bytes) nên phải nhân 4 , do đó `this[4 * i]`)
Kết luận `password` cần tìm là `encrypted-c-string`

## Execute

```bash
> .\crackme.exe
Enter password: encrypted-c-string
CORRECT
```

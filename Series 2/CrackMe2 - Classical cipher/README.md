# CrackMe2 - Classical cipher

## Solution

### Architecture

Dùng lệnh `file` để xác định kiến trúc của file thực thi `a.out`

```zsh
└─$ file CrackMe2.exe
CrackMe2.exe: PE32 executable (console) Intel 80386, for MS Windows
```

Đây là file thực thi trên giao diện `console` `Windows 32-bit`

### Disassembly

Sử dụng IDA Pro để đọc pseudocode
Hàm `main`:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  unsigned __int8 v3; // al
  char *i; // ecx
  int v5; // eax
  char v7; // [esp-Ch] [ebp-110h]
  char v8; // [esp-8h] [ebp-10Ch]
  char v9; // [esp-4h] [ebp-108h]
  char Password[256]; // [esp+0h] [ebp-104h] BYREF

  sub_4010B0("-----------------------------------\n", Password[0]);
  sub_4010B0("--           CrackMe 2           --\n", v9);
  sub_4010B0("--      by github.com/dajoh      --\n", v8);
  sub_4010B0("-----------------------------------\n\n", v7);
  while ( 1 )
  {
    sub_401010((int)"Enter password: ", 15u);
    gets_s(Password, 256u);
    v3 = Password[0];
    for ( i = Password; *i; v3 = *i )
      *i++ = byte_4188F0[v3];
    v5 = strcmp(Password, "HfyhgrgfgrlmYlc579");
    if ( v5 )
      v5 = v5 < 0 ? -1 : 1;
    if ( !v5 )
      break;
    sub_401010((int)"Fail! You entered the wrong password.\n\n", 0xCu);
  }
  sub_401010((int)"Congratulations! You entered the correct password.\n\n", 0xAu);
  sub_401010((int)"Press enter to exit...", 8u);
  sub_404D1E();
  return 0;
}
```

Chương trình nhận vào chuỗi `password`, lưu tại `Password` (tên biến đã được thay đổi).

Xem xét đoạn code sau

```c
v3 = Password[0];
for ( i = Password; *i; v3 = *i )
  *i++ = byte_4188F0[v3];
v5 = strcmp(Password, "HfyhgrgfgrlmYlc579");
```

Đúng như tên của challenge, chương trình sẽ biến đổi chuỗi `password` thành 1 chuỗi khác thông qua 1 substitution box, sau đó so sánh với chuỗi hằng có sẵn `HfyhgrgfgrlmYlc579`. Nếu đúng sẽ in ra màn hình `Congratulations! You entered the correct password.`

Substitution box ở đây là `byte_4188F0`.
**Công thức biến đổi** là sẽ lấy giá trị `ASCII` của từng kí tự trong `password`, thay đổi thành kí tự tại vị trí đó trong mảng `byte_4188F0`

Và mảng `byte_4188F0` tương tự như bảng mã `ASCII`, có 256 kí tự, các kí tự đặc biệt thì ở đúng vị trí như mã `ASCII`, nhưng kí tự số, alphabet thì lại ngược lại `9 -> 0, Z -> A, z -> a`
Vậy, kí tự số và alphabet trong `password` biến thành một kí tự cùng vị trí nhưng tính theo chiều ngược lại (ví dụ Z thành A, B thành Y...)

Áp dụng công thức đó, giải mã chuỗi `HfyhgrgfgrlmYlc579` ta được chuỗi `SubstitutionBox420`. **Đây là password đúng.**

## Execute

```bash
>CrackMe2.exe
-----------------------------------
--           CrackMe 2           --
--      by github.com/dajoh      --
-----------------------------------

Enter password: SubstitutionBox420
Congratulations! You entered the correct password.

Press enter to exit...
```

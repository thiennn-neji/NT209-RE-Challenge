# WarGames
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `WarGames`
```zsh
└─$ file WarGames
WarGames: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=9a0e6dfa0e34cb42a1d5524f94d26424fff8625e, for GNU/Linux 3.2.0, not stripped
```
Đây là file thực thi trên `linux 64-bit`
### Disassembly
Dùng IDA Pro để đọc pseudocode
Hàm `main` :
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  int v4; // [rsp+18h] [rbp-28h]
  unsigned __int64 i; // [rsp+20h] [rbp-20h]
  _BYTE v6[9]; // [rsp+2Fh] [rbp-11h] BYREF
  unsigned __int64 v7; // [rsp+38h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  if ( argc == 2 )
  {
    if ( j_strlen_ifunc() == (int (__fastcall *)(const __m128i *))9 )
    {
      qmemcpy(v6, "gssw#tpcz", sizeof(v6));
      v4 = 0;
      srandom(1983LL);
      for ( i = 0LL; i <= 8; ++i )
      {
        v6[i] -= (int)rand() % 5 + 1;
        if ( v6[i] != argv[1][i] )
        {
          v4 = 1;
          break;
        }
      }
      if ( v4 )
        puts("Wrong Password !!!");
      else
        puts("Congratulation !!!");
      result = 0;
    }
    else
    {
      puts("Wrong Password !!!");
      result = 0;
    }
  }
  else
  {
    puts("Use ./WarGames pass");
    result = 0;
  }
  return result;
}
```
Chuỗi `password` cần tìm lấy từ `argv[1]` hay là tham số thứ 1.
Điều kiện `j_strlen_ifunc() == (int (__fastcall *)(const __m128i *))9` kiểm tra xem chuỗi `password` nhập vào có độ dài bằng 9 hay không, nếu không thì là `Wrong Password !!!`

Để chương trình in ra màn hình chuỗi `Congratulation !!!` thì biến `v4` phải bằng `0` (để thực hiện khối lệnh else). Và `v4 == 0` nếu trong vòng lặp `for`, giá trị của chuỗi `v6` tại vị trí `i` bằng giá trị của chuỗi `password` tại vị trí `i`.

```c
qmemcpy(v6, "gssw#tpcz", sizeof(v6));
v4 = 0;
srandom(1983LL);
for ( i = 0LL; i <= 8; ++i )
{
  v6[i] -= (int)rand() % 5 + 1;
  if ( v6[i] != argv[1][i] )
  {
    v4 = 1;
    break;
  }
}
```

Ban đầu chuỗi `v6` được gán bằng `gssw#tpcz`. Sau đó được biến đổi với giá trị random theo công thức `v6[i] -= (int)rand() % 5 + 1`. Bởi vì hàm `rand()` được seed giá trị `1983` nên những lần chạy khác nhau, các số random là **như nhau**

Vậy để tìm được chuỗi `v6` cần chạy debug để xem chương trình `rand()` ra giá trị như thế nào. Và đây là 9 giá trị random đầu tiên sau khi debug.
```
0x13329EA0
0x4DF09890
0x50C0A14C
0x208CB496
0x13DAF7C1
0x2F85953B
0x70B47F9A
0x409FAFB2
0x629988D5
```
Từ 9 giá trị này và áp dụng công thức ở trên, suy ra được chuỗi `v6` cần tìm là `dont play`, cũng chính là `password`
Vì dấu khoảng trắng dùng để tách các `arguments` nên trong linux để escape ta dùng dấu `Backslash (\)`

## Execute
```zsh
└─$ ./WarGames dont\ play
Congratulation !!!
```

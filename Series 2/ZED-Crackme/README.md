# ZED-Crackme

## Solution

### Architecture

Dùng lệnh `file` để xác định kiến trúc của file thực thi `ZED-Crackme-x64.bin`

```zsh
└─$ file ZED-Crackme-x64.bin
ZED-Crackme-x64.bin: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), statically linked, no section header
```

Đây là file thực thi `linux 64-bit`

Ở phần xem kiến trúc của file, mình thấy có thông báo là `no section header` nên nghĩ là file thực thi đã được `pack`
Và đúng khi sử dụng IDA Pro để disassembly và đọc pseudocode thì chỉ có 4 `functions`
Vậy nên mình sử dụng công cụ `upx` để unpack file

```zsh
└─$ upx -d ZED-Crackme-x64.bin
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2020
UPX 3.96        Markus Oberhumer, Laszlo Molnar & John Reiser   Jan 23rd 2020

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
     13184 <-      7656   58.07%   linux/amd64   ZED-Crackme-x64.bin

Unpacked 1 file.
```

Sau đó mình xem lại kiến trúc file:

```zsh
└─$ file ZED-Crackme-x64.bin
ZED-Crackme-x64.bin: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=6d5e1ea9a99de8dd8b9e18a01ec6925571114484, not stripped
```

Và chạy thử

```zsh
└─$ ./ZED-Crackme-x64.bin
***********************
**      rules:       **
***********************

* do not bruteforce
* do not patch, find instead the serial.

enter the passphrase: sss
try again
```

Ok đã unpack.

### Disassembly

Sử dụng IDA Pro để đọc pseudocode

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+14h] [rbp-9Ch]
  char v5[6]; // [rsp+1Ah] [rbp-96h] BYREF
  __int64 v6[4]; // [rsp+20h] [rbp-90h] BYREF
  char s2[32]; // [rsp+40h] [rbp-70h] BYREF
  char s1[32]; // [rsp+60h] [rbp-50h] BYREF
  char v9[40]; // [rsp+80h] [rbp-30h] BYREF
  unsigned __int64 v10; // [rsp+A8h] [rbp-8h]

  v10 = __readfsqword(0x28u);
  puts("***********************");
  puts("**      rules:       **");
  puts("***********************");
  putchar(10);
  puts("* do not bruteforce");
  puts("* do not patch, find instead the serial.");
  putchar(10);
  strcpy(v9, "This is a top secret text message!");
  __sidt(v5);
  if ( v5[5] == -1 )
  {
    puts("VMware detected");
    exit(1);
  }
  rot(13LL, v9);
  rot(13LL, v9);
  qmemcpy(v6, "AHi23DEADBEEFCOFFEE", 19);
  printf("enter the passphrase: ");
  __isoc99_scanf("%s", s2);
  if ( ptrace(PTRACE_TRACEME, 0LL) < 0 )
  {
    puts("This process is being debugged!!!");
    exit(1);
  }
  s1[0] = LOBYTE(v6[0]) ^ 2;
  s1[1] = BYTE3(v6[0]) - 10;
  s1[2] = BYTE2(v6[0]) + 12;
  s1[3] = BYTE2(v6[0]);
  s1[4] = BYTE1(v6[0]) + 1;
  for ( i = 5; i <= 18; ++i )
    s1[i] = *((_BYTE *)v6 + i) - 1;
  if ( !strcmp(s1, s2) )
    puts("you succeed!!");
  else
    puts("try again");
  return 0;
}
```

`password` được nhập vào lưu ở chuỗi `s2`.
Để chương trình in ra `you succeed!!` thì chuỗi `s2` cần giống chuỗi `s1`

Chuỗi `s1` (dài 19 kí tự) được tạo ra từ biến đổi trên chuỗi `v6 = AHi23DEADBEEFCOFFEE`

```c
s1[0] = LOBYTE(v6[0]) ^ 2;
s1[1] = BYTE3(v6[0]) - 10;
s1[2] = BYTE2(v6[0]) + 12;
s1[3] = BYTE2(v6[0]);
s1[4] = BYTE1(v6[0]) + 1;
for ( i = 5; i <= 18; ++i )
  s1[i] = *((_BYTE *)v6 + i) - 1;
```

Đoạn code này hiểu đơn giản hơn chính là

```c
s1[0] = v6[0] ^ 2;
s1[1] = v6[3] - 10;
s1[2] = v6[2] + 12;
s1[3] = v6[2];
s1[4] = v6[1] + 1;
for ( i = 5; i <= 18; ++i )
  s1[i] = v6[i] - 1;
```

Vậy chuỗi `s1` có giá trị là `C(uiICD@CADDEBNEEDD`

## Execute

```zsh
└─$ ./ZED-Crackme-x64.bin
***********************
**      rules:       **
***********************

* do not bruteforce
* do not patch, find instead the serial.

enter the passphrase: C(uiICD@CADDEBNEEDD
you succeed!!
```

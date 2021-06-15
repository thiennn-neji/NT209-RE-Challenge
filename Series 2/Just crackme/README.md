# Just crackme

## Solution

### Architecture

Dùng lệnh `file` để xác định kiến trúc của file thực thi `a.out`

```zsh
└─$ file a.out
a.out: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=ed76b7e31e4e28ac60796e87722903fcffaf9af3, for GNU/Linux 3.2.0, not stripped
```

Đây là file thực thi `linux 64-bit`

### Disassembly

Sử dụng IDA Pro để đọc pseudocode
Hàm `main`:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  const char *src; // [rsp+8h] [rbp-E8h]
  char *s; // [rsp+10h] [rbp-E0h]
  __int64 v6; // [rsp+18h] [rbp-D8h]
  char v7[200]; // [rsp+20h] [rbp-D0h] BYREF
  unsigned __int64 v8; // [rsp+E8h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  if ( !malloc(0x46uLL) )
    exit(1);
  src = getenv("USER");
  s = (char *)malloc(300uLL);
  if ( !s )
    exit(1);
  strcpy(&s[strlen(s)], "Wait, your name is");
  strcat(s, src);
  puts("Enter your flag.");
  __isoc99_scanf("%s", v7);
  v6 = compare((__int64)s);
  if ( (unsigned int)strcp(v6, v7) )
    printf("Try again");
  else
    printf("Done.");
  return 0;
}
```

Đầu tiên, chương trình lấy tên `user` đang thực thi file này và ghép với chuỗi `Wait, your name is` lưu trong chuỗi `s`, sau đó biến đổi chuỗi `s` và lưu vào `v6`

```c
src = getenv("USER");
s = (char *)malloc(300uLL);
if ( !s )
  exit(1);
strcpy(&s[strlen(s)], "Wait, your name is");
strcat(s, src);
```

Với máy mình, `user` là `neji` nên chuỗi **`s = Wait, your name isneji`**

Sau đó chương trình nhận chuỗi `password` nhập vào lưu ở `v7`.

Để khai thác thành công (chương trình in ra màn hình chuỗi `Done.`) thì chuỗi `v7` phải giống chuỗi `v6`

Chuỗi `s` được biến đổi thành chuỗi `v6` bằng hàm `compare`.

```c
__int64 __fastcall compare(__int64 a1)
{
  int i; // [rsp+18h] [rbp-28h]
  time_t timer; // [rsp+28h] [rbp-18h] BYREF
  struct tm *v4; // [rsp+30h] [rbp-10h]
  unsigned __int64 v5; // [rsp+38h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  time(&timer);
  v4 = localtime(&timer);
  for ( i = 0; i < (int)stlen(a1); ++i )
    *(_BYTE *)(i + a1) ^= v4->tm_min >> v4->tm_mday;
  return a1;
}
```

`v4` lưu `localtime` chính là thời gian hiện tại trên máy tính lúc thực thi đến câu lệnh này. Và từng kí tự trong chuỗi `s1` được `xor` với ` phút hiện tại >> ngày hiện tại`

Mình viết đoạn code sau (`solve.py`) để tính theo thời gian gần đúng (có thể lệch 1 phút, thì chạy lại là được)

```python
import os
import time
src = 'Wait, your name is' + os.getenv('USER')
s = [char for char in src]
t = time.localtime()
shift = t.tm_min >> t.tm_mday
for i in range(len(s)):
    s[i] = chr(ord(s[i]) ^ shift)
result = ''.join(s)
print(result)
```

## Execute

```zsh
└─$ python2 solve.py | ./a.out
Enter your flag.
Done.
```

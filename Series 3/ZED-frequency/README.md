# ZED-frequency
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `ZED-Frequency.bin`
```zsh
└─$ file ZED-Frequency.bin
ZED-Frequency.bin: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=3e0bc53b0b5739a9f0c588fafc92ec6cfdde1b42, not stripped
```
Đây là file thực thi trên linux 64-bit (`ELF64`)

### Disassembly

Đầu tiên mở IDA Pro lên và tìm đến các String trong chương trình. Và không có chuỗi nào liên quan đến chúc mừng hay giải thành công. Vậy bỏ qua.

Mình disassembly hàm `main`

#### Hàm `main`
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+10h] [rbp-B0h]
  int v5; // [rsp+10h] [rbp-B0h]
  int j; // [rsp+14h] [rbp-ACh]
  FILE *stream; // [rsp+18h] [rbp-A8h]
  int v8[28]; // [rsp+20h] [rbp-A0h]
  char s1[40]; // [rsp+90h] [rbp-30h] BYREF
  unsigned __int64 v10; // [rsp+B8h] [rbp-8h]

  v10 = __readfsqword(0x28u);
  if ( argc <= 1 )
  {
    printf("usage: %s <keyfile>\n", *argv);
    exit(1);
  }
  stream = fopen(argv[1], "rt");
  for ( i = 0; i <= 25; ++i )
    v8[i] = 0;
  while ( 1 )
  {
    v5 = fgetc(stream);
    if ( v5 == -1 )
      break;
    if ( v5 <= '`' || v5 > 122 )
    {
      if ( v5 > 64 && v5 <= 90 )
        ++v8[v5 - 65];
    }
    else
    {
      ++v8[v5 - 97];
    }
  }
  printf("the generated key is: ");
  for ( j = 0; j <= 25; ++j )
  {
    printf("%d", (unsigned int)v8[j]);
    s1[j] = LOBYTE(v8[j]) + 48;
  }
  s1[26] = 0;
  putchar(10);
  if ( !strcmp(s1, "01234567890123456789012345") )
    puts("you succeed!!");
  else
    puts("you failed!!");
  return 0;
}
```

Đọc đoạn code sau kết hợp với tên đề bài thì đoạn code này làm nhiệm vụ đếm `tần suất xuất hiện` của các kí tự `alphabet` (không phân biệt hoa, thường - `case-insensitive`) đọc được từ file
```c
if ( argc <= 1 )
{
  printf("usage: %s <keyfile>\n", *argv);
  exit(1);
}
stream = fopen(argv[1], "rt");
for ( i = 0; i <= 25; ++i )
  v8[i] = 0;
while ( 1 )
{
  v5 = fgetc(stream);
  if ( v5 == -1 )
    break;
  if ( v5 <= '`' || v5 > 122 )
  {
    if ( v5 > 64 && v5 <= 90 )
      ++v8[v5 - 65];
  }
  else
  {
    ++v8[v5 - 97];
  }
}
```

Và chuỗi tần suất này lưu theo thứ tự xuất hiện của chữ cái trong bảng alphabet.

Sau đó so sánh chuỗi tần suất này với chuỗi `01234567890123456789012345`, nếu đúng thì thành công.

Suy ra chuỗi này phải có quy luật là
1. Chữ `a`/`A` xuất hiện 0 lần
1. Chữ `b`/`B` xuất hiện 1 lần
1. Chữ `c`/`C` xuất hiện 2 lần
1. Chữ `d`/`D` xuất hiện 3 lần ......

Vậy mình tạo chuỗi nhờ đoạn [code](generate.py) sau để tạo chuỗi như yêu cầu và lưu vào file
```python
from string import ascii_uppercase
from random import shuffle

def generate():
    frequency = list(map(int, list("01234567890123456789012345")))
    alphabet = list(ascii_uppercase)
    key = list(''.join([alphabet[i] * frequency [i] for i in range(len(alphabet))]))
    shuffle(key)
    return ''.join(key)

if __name__ == '__main__':
   key = generate()
   with open('key.txt', 'w+') as fout:
       fout.write(key)
       fout.flush()
```

#### Kết luận
Vậy file `key` phải chứa các kí tự với tần suất là `01234567890123456789012345` theo thứ tự xuất hiện trong alphabet
## Execute

```zsh
└─$ ./ZED-Frequency.bin key.txt
the generated key is: 01234567890123456789012345
you succeed!!
```

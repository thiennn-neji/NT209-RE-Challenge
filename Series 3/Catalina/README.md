# Catalina
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `crackme`
```zsh
└─$ file crackme
crackme: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=4e67f827e2bb32da50b2ce98842c4a9e9fde0996, stripped
```
Đây là file thực thi trên linux 64-bit (`ELF64`)

### Disassembly

Đầu tiên mở IDA Pro lên và tìm đến các String trong chương trình
![image](https://user-images.githubusercontent.com/59532111/124393301-00634900-dd24-11eb-9a28-53398723d2f0.png)Thì mình thấy được chuỗi chúc mừng khi giải thành công. Và chuỗi này được sử dụng trong hàm `main`. Vậy thì xem pseudocode của hàm `main`

#### Hàm `main`
```c
__int64 __fastcall main(int argc, char **argv, char **a3)
{
  __int64 result; // rax
  int v4; // ebx
  const char *v5; // r12
  size_t v6; // rax
  size_t v7; // rax
  char v8[32]; // [rsp+10h] [rbp-100h] BYREF
  char v9[32]; // [rsp+30h] [rbp-E0h] BYREF
  char v10; // [rsp+50h] [rbp-C0h]
  int v11[34]; // [rsp+60h] [rbp-B0h]
  const char *v12; // [rsp+E8h] [rbp-28h]
  int v13; // [rsp+F4h] [rbp-1Ch]
  int i; // [rsp+F8h] [rbp-18h]
  int count; // [rsp+FCh] [rbp-14h]

  if ( argc == 2 )
  {
    v12 = "JTQSRyZKSB05Dh9JgH6fQJIVjJ04UpA7ezxMIHcvpX6X70NJHW4xlxSHHMuLDjCJbzl9ITfgeLbTDLExZENyYrAzn7ehjAMuZf1siTB4HBLgyJ"
          "gpK38LHCq4UvpgqOxeoh72AVgDOYS8HU9xg";
    v11[0] = 4;
    v11[1] = 4;
    v11[2] = 5;
    v11[3] = 4;
    v11[4] = 2;
    v11[5] = 4;
    v11[6] = 3;
    v11[7] = 4;
    v11[8] = 2;
    v11[9] = 4;
    v11[10] = 6;
    v11[11] = 2;
    v11[12] = 4;
    v11[13] = 6;
    v11[14] = 2;
    v11[15] = 5;
    v11[16] = 5;
    v11[17] = 2;
    v11[18] = 3;
    v11[19] = 3;
    v11[20] = 5;
    v11[21] = 4;
    v11[22] = 2;
    v11[23] = 3;
    v11[24] = 4;
    v11[25] = 2;
    v11[26] = 2;
    v11[27] = 3;
    v11[28] = 3;
    v11[29] = 2;
    v11[30] = 4;
    v11[31] = 5;
    *(_QWORD *)v9 = 0LL;
    *(_QWORD *)&v9[8] = 0LL;
    *(_QWORD *)&v9[16] = 0LL;
    *(_QWORD *)&v9[24] = 0LL;
    v10 = 0;
    count = 0;
    for ( i = 0; i <= 31; ++i )
    {
      v9[i] = v12[count];
      count += v11[i] + 1;
    }
    sub_1482((__int64)v9, (__int64)v8, 32);
    count = 0;
    v13 = 0;
    while ( count <= 23 )
    {
      v8[count] ^= 0x41u;
      v4 = (unsigned __int8)v8[count];
      v5 = argv[1];
      v6 = strlen(v5);
      if ( v6 >= count )
        v7 = count;
      else
        v7 = strlen(argv[1]);
      v13 += v4 == v5[v7];
      ++count;
    }
    if ( v13 == 24 )
      puts("Congratulations !! you solved the first challenge.");
    else
      puts("Invalid flag, try again");
    result = 0LL;
  }
  else
  {
    puts("Welcome to crackme N1");
    printf("Usage:\n%s <password>\n", *argv);
    result = 0xFFFFFFFFLL;
  }
  return result;
}
```

Chương trình yêu cầu `argc == 2` tức là chuỗi `password` cần tìm là 1 tham số khi gọi chương trình luôn. 
> `$ ./crackme <password>`

**First of all**

Đọc ngược từ dưới lên, để có thể in ra chuỗi thành công thì `v13 == 24` suy ra trong 24 kí tự đầu tiên (biến lặp `count`) của chuỗi `v8 ^ 0x41` (`password` cần tìm) bằng với chuỗi `v5` (input)

**Next**

`v9` sau khi `debug` là`Jy0gJjpzcXNxHjIgLyAeMiByKCUge2g8`
Chuỗi `v8` dài 32 kí tự được tạo ra từ chuỗi `v9`
> `sub_1482((__int64)v9, (__int64)v8, 32);`

Hàm đó mình không đi sâu vào (đọc khá rối, mà không cần thiết)
Vì chương trình so sánh toàn bộ 24 phần tử đầu của `v8` với `v5` rồi mới kết luận nên tiếp tục `debug` đến khi gặp khối lệnh 
```c
if ( v13 == 24 )
  puts("Congratulations !! you solved the first challenge.");
else
  puts("Invalid flag, try again");
```
Được 24 kí tự đầu của chuỗi `v8` là `flag{2020_sana_sa3ida:)}@`

#### Kết luận
Vậy `password` cần tìm có ít nhất 24 kí tự, 24 kí tự đầu là `flag{2020_sana_sa3ida:)}@`
Tuy nhiên khi thực thi cần `escape` kí tự `)`
```zsh
└─$ ./crackme flag{2020_sana_sa3ida:)}@
zsh: parse error near `)'
```
## Execute

```zsh
└─$ ./crackme flag{2020_sana_sa3ida:\)}@
Congratulations !! you solved the first challenge.

└─$ ./crackme flag{2020_sana_sa3ida:\)}@123
Congratulations !! you solved the first challenge.
```

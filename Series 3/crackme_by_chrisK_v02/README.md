# crackme_by_chrisK_v02
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `crackme_by_chrisK_v02.exe`
```zsh
└─$ file crackme_by_chrisK_v02.exe
crackme_by_chrisK_v02.exe: PE32 executable (console) Intel 80386, for MS Windows
```
Đây là file thực thi trên Windows 32-bit, `console`

### Disassembly
Mở IDA Pro và tìm xem các String thì có chuỗi là `Nice!!` và [`https://imgur.com/a/pql7Epy`](https://imgur.com/a/pql7Epy)

![image](https://user-images.githubusercontent.com/59532111/124441521-f4b86680-dda5-11eb-8679-4d1dda25777f.png)

Xem qua link thì dẫn đến bức ảnh, nội dung chắc tác giả muốn chúc mừng Giáng sinh (bức ảnh up ngày 20/12)

#### Hàm `main`

Đây là pseudocode của hàm `main`

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  int v4; // eax
  int *v5; // ebx
  char passwordKey[50]; // [esp+10h] [ebp-74h] BYREF
  char password[50]; // [esp+42h] [ebp-42h] BYREF
  int *v8; // [esp+74h] [ebp-10h]
  signed int passwordLength; // [esp+78h] [ebp-Ch]
  int i; // [esp+7Ch] [ebp-8h]

  __main();
  i = 0;
  passwordLength = 0;
  printf("Enter Password: ");
  scanf("%s", password);
  if ( strlen(password) > 9 && password[5] == '.' )
  {
    printf("Enter password key: ");
    scanf("%s", passwordKey);
    while ( 1 )
    {
      v4 = i++;
      if ( !password[v4] )
        break;
      ++passwordLength;
    }
    v8 = (int *)malloc(4 * passwordLength);
    srand(passwordLength);
    for ( i = 0; i < passwordLength; ++i )
    {
      v5 = &v8[i];
      *v5 = rand() % passwordLength + passwordLength / -2;
    }
    magic(password, v8);
    if ( !strcmp(mstring, passwordKey) )
    {
      printf("Nice!!");
      result = 0;
    }
    else
    {
      printf("Wrong");
      result = 1;
    }
  }
  else
  {
    printf("Wrong");
    result = 1;
  }
  return result;
}
```

**Các tên biến đã được thay đổi.**

Chương trình yêu cầu mình nhập vào một `password` và `password key` tương ứng.
1. `password` có độ dài ít nhất là 10 kí tự, và kí tự thứ 6 là dấu chấm `.`
2. `password key` được tạo từ `password` theo một công thức nào đấy. Vậy đây là một bài `keygen` điển hình

#### Tạo random 

Sau khi nhập xong `password` và `password key`, chương trình tính độ dài của `passsword` (là `passwordLength`), tạo mảng số nguyên `v8` có số phần tử bằng `passwordLength` và `v8[i] = rand() % passwordLength - passwordLength/2` với seed là `srand(passwordLength)`
> Suy ra với các `password` cùng độ dài thì mảng `v8` có giá trị giống nhau

#### Tạo mstring (magic string/password key)

`password` và mảng số nguyên random `v8` đưa vào hàm `magic` để sinh ra `passsword key` tương ứng

```c
char *__cdecl magic(char *a1, int *a2)
{
  int v2; // eax
  char *result; // eax
  int i; // [esp+8h] [ebp-Ch]
  int a1_length; // [esp+Ch] [ebp-8h]
  int j; // [esp+Ch] [ebp-8h]

  a1_length = 0;
  for ( i = 0; ; ++i )
  {
    v2 = a1_length++;
    if ( !a1[v2] )
      break;
  }
  for ( j = 0; j < i; ++j )
    mstring[j] += LOBYTE(a2[j]) + a1[j];
  result = &mstring[j];
  mstring[j] = 0;
  return result;
}
```

**Công thức tổng quát trong hàm này là `mstring[i] = password[i] + v[i]`.**

#### Kết luận

Vậy mình suy ra được công thức `keygen` tạo `password key` từ `password` là

**`passwordKey[i] = password[i] + rand() % passwordLength - passwordLength/2` với `srand(passwordLength)`**
> Đáp án để làm keygen là đây

Đồng thời thỏa các điều kiện sau:
1. `password` có độ dài tối thiểu là 10 và kí tự thứ 6 là dấu chấm `.`
2. `password key` có độ dài bằng với `password`
#### Keygen - Giải pháp 1

Vấn đề là hàm `random` là hàm phụ thuộc vào nhiều `API` bên dưới, các ngôn ngữ lập trình khác nhau thì hành vi của `random` cũng khác nhau. Trong C/C++, thì `RNG`(random number generator) cũng phụ thuộc vào compiler, phiên bản của compiler, compile trên các OS khác nhau. 

```zsh
└─$ strings crackme_by_chrisK_v02.exe | grep -E 'GCC|GNU'
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (MinGW.org GCC-6.3.0-1) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GCC: (GNU) 6.3.0
GNU AS 2.28
GNU C11 6.3.0 -mtune=generic -march=i586 -g -g -g -O2 -O2 -O2 -fbuilding-libgcc -fno-stack-protector
```

File thực thi này compile bằng `mingw64` version `6.3.0`, sử dụng `C11`, compile trên `Windows`


Mình sử dụng `mingw64` nhưng version `10.3.0`, và dùng `C99`, compile trên `Windows 10` cho đoạn [code](solve.c) `keygen`.

Đây là kết quả thực thi keygen cho `password = "hello.world"`
```bash
> gcc .\solve.c -o solve.exe

> strings .\solve.exe | grep -E 'GNU|GCC'
GCC: (Rev2, Built by MSYS2 project) 10.3.0
GNU C99 10.3.0 -m64 -mtune=generic -march=x86-64 -g -O2 -std=gnu99

> .\solve.exe
hello.world
kelms,rrnna
```

Áp dụng vào chương trình cần giải và nó đúng
> Vậy keygen đúng (nhưng có thể sẽ không hoạt động được trên OS, compiler khác)
## Execute

```bash
> .\crackme_by_chrisK_v02.exe
Enter Password: hello.world
Enter password key: kelms,rrnna
Nice!!
```

```bash
> .\crackme_by_chrisK_v02.exe
Enter Password: hello.world
Enter password key: cgqls.vltja
Wrong
```

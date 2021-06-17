# Find password

## Solution

### Architecture

Dùng lệnh `file` để xác định kiến trúc của file thực thi `password.exe`

```zsh
└─$ file password.exe
password.exe: PE32 executable (console) Intel 80386 (stripped to external PDB), for MS Windows
```

Đây là file thực thi trên giao diện `console` `Windows 32-bit`

### Disassembly

Sử dụng IDA Pro để đọc pseudocode

#### Hàm `main`:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+0h] [ebp-88h] BYREF
  char v5[4]; // [esp+1Ch] [ebp-6Ch] BYREF
  int v6; // [esp+20h] [ebp-68h]
  int (__cdecl *v7)(int, int, __int64, _BYTE *, int); // [esp+34h] [ebp-54h]
  int *v8; // [esp+38h] [ebp-50h]
  char *v9; // [esp+3Ch] [ebp-4Ch]
  void (__noreturn *v10)(); // [esp+40h] [ebp-48h]
  int *v11; // [esp+44h] [ebp-44h]
  void *Buf2[2]; // [esp+50h] [ebp-38h] BYREF
  char v13[16]; // [esp+58h] [ebp-30h] BYREF
  void *Buf1; // [esp+68h] [ebp-20h] BYREF
  size_t Size; // [esp+6Ch] [ebp-1Ch]
  char v16[16]; // [esp+70h] [ebp-18h] BYREF
  char v17; // [esp+80h] [ebp-8h] BYREF

  v7 = sub_4017D0;
  v8 = dword_4B5DE0;
  v9 = &v17;
  v11 = &v4;
  v10 = sub_4B5965;
  sub_427910(v5);
  sub_4270A0();
  Buf2[0] = v13;
  v6 = -1;
  sub_401360(Buf2, "djejie", (int)"");
  Buf1 = v16;
  v6 = 1;
  sub_401360(&Buf1, "ggkfjgjfrg", (int)"");
  v6 = 2;
  sub_4B2DC0((int)&dword_4C6860, "inserisci la password per accedere al programma ");
  sub_403800(&dword_4C6900, &Buf1);
  do
  {
    do
    {
      v6 = 2;
      sub_4B0060(&dword_4C6860, (int)"password errata.\n", 17);
      sub_4B0060(&dword_4C6860, (int)"inserisci la password per accedere al programma ", 48);
      sub_403800(&dword_4C6900, &Buf1);
    }
    while ( (void *)Size != Buf2[1] );
  }
  while ( memcmp(Buf1, Buf2[0], Size) );
  sub_4B0060(&dword_4C6860, (int)"benvenuto", 9);
  sub_4B0D70(&dword_4C6860);
  if ( Buf1 != v16 )
    j_free(Buf1);
  if ( Buf2[0] != v13 )
    j_free(Buf2[0]);
  sub_427A70(v5);
  return 0;
}
```

#### Các chuỗi kì lạ và STRUCT

Tại câu lệnh này

```c
sub_401360(Buf2, "djejie", (int)"");
...
sub_401360(&Buf1, "ggkfjgjfrg", (int)"");
```

Ban đầu mình nghĩ là chương trình copy 2 chuỗi vào 2 biến tương ứng. Nhưng khi mình debug và quan sát bộ nhớ trên stack, thì mình phát hiện ra một điều lý thú hơn

```
Stack[00001314]:006CFEC0 dd offset aDjejie_0                     ; "djejie"
Stack[00001314]:006CFEC4 db    6
Stack[00001314]:006CFEC5 db    0
Stack[00001314]:006CFEC6 db    0
Stack[00001314]:006CFEC7 db    0
Stack[00001314]:006CFEC8 aDjejie_0 db 'djejie',0                 ; DATA XREF: Stack[00001314]:006CFEC0↑o
Stack[00001314]:006CFECF db    0
Stack[00001314]:006CFED0 db 0C0h ; À
Stack[00001314]:006CFED1 db 0CCh ; Ì
Stack[00001314]:006CFED2 db  54h ; T
Stack[00001314]:006CFED3 db  75h ; u
Stack[00001314]:006CFED4 db    3
Stack[00001314]:006CFED5 db 0FEh ; þ
Stack[00001314]:006CFED6 db  67h ; g
Stack[00001314]:006CFED7 db  44h ; D
Stack[00001314]:006CFED8 dd offset aGgkfjgjfrg_0                 ; "ggkfjgjfrg"
Stack[00001314]:006CFEDC db  0Ah
Stack[00001314]:006CFEDD db    0
Stack[00001314]:006CFEDE db    0
Stack[00001314]:006CFEDF db    0
Stack[00001314]:006CFEE0 aGgkfjgjfrg_0 db 'ggkfjgjfrg',0         ; DATA XREF: Stack[00001314]:006CFED8↑o
Stack[00001314]:006CFEEB db    0
Stack[00001314]:006CFEEC db  7Eh ; ~
Stack[00001314]:006CFEED db  70h ; p
Stack[00001314]:006CFEEE db  42h ; B
Stack[00001314]:006CFEEF db    0
```

Đó là `buf1` và `buf2` mình nghĩ là 1 struct có dạng

```c
struct buf
{
	char * p;
	int length;
	char[] str;
}
```

Nhưng có thể hiểu đơn giản hơn là `Buf2` trỏ đến chuỗi `djejie`
`Buf1` trỏ đến chuỗi `ggkfjgjfrg`

#### Lời giải

Trong đoạn code tiếp theo

```c
sub_4B2DC0((int)&dword_4C6860, "inserisci la password per accedere al programma ");
sub_403800(&dword_4C6900, &Buf1);
do
{
  do
  {
    v6 = 2;
    sub_4B0060(&dword_4C6860, (int)"password errata.\n", 17);
    sub_4B0060(&dword_4C6860, (int)"inserisci la password per accedere al programma ", 48);
    sub_403800(&dword_4C6900, &Buf1);
  }
  while ( (void *)Size != Buf2[1] );
}
while ( memcmp(Buf1, Buf2[0], Size) );
sub_4B0060(&dword_4C6860, (int)"benvenuto", 9);
```

Chương trình yêu cầu nhập vào `password` với câu dẫn: `inserisci la password per accedere al programma`

`password` được nhập sẽ lưu tại `struct Buf1` mà mình đã phân tích ở trên. Nhưng không kiểm tra gì mà thực hiện tiếp 2 vòng lặp `do-while`. Vì vậy `password` nhập lần đầu luôn in ra sai `password errata.\n`.

Để chương trình in ra màn hình `benvenuto` thì cần thoát cả 2 vòng lặp. Do đó phải thỏa lần lượt 2 điều kiện:

1. `password` nhập vào phải có độ dài (`Buf1[1]`) bằng với `Size`. Sau khi debug thì mình biết được `Size == Buf2[1]` tức là bằng 6 (vì `Buf2` luôn là `djejie`)
2. `password` phải giống với `Buf2`. Suy ra `password == djejie`

## Execute

```bash
>password.exe
inserisci la password per accedere al programma djejie
password errata.
inserisci la password per accedere al programma djejie
benvenuto
```

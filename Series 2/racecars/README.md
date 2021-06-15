# racecars

## Solution

### Architecture

Dùng lệnh `file` để xác định kiến trúc của file thực thi `racecars`

```zsh
└─$ file racecars
racecars: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=84eee6611847da3272d223e4129ccbc5febe4231, for GNU/Linux 3.2.0, with debug_info, not stripped
```

Đây là file thực thi `linux 64-bit`

### Disassembly

Sử dụng IDA Pro để đọc pseudocode
Hàm `main`:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int start; // [rsp+18h] [rbp-8h]
  int end; // [rsp+1Ch] [rbp-4h]

  end = strlen(*argv) - 1;
  for ( start = end; (*argv)[start - 1] != '/'; --start )
    ;
  while ( start < end )
  {
    if ( (*argv)[start] != (*argv)[end] )
    {
      puts("Gimme what I want!");
      exit(1);
    }
    --end;
    ++start;
  }
  puts("That's exactly what I wanted!");
  return 0;
}
```

Hàm kiểm tra các điều kiện liên quan đến mảng `argv`
`argv` là mảng các tham số truyền vào chương trình, và ở trong hàm `main`, ta thao tác trên `argv[0]` hay `*argv`. Đây chính là đường dẫn tuyệt đối của tên file thực thi.
Trong trường hợp máy mình thì:
`argv[0] = /home/neji/Downloads/Challenge1-2/racecars`

Sau đó tại đoạn code này

```c
int start; // [rsp+18h] [rbp-8h]
int end; // [rsp+1Ch] [rbp-4h]

end = strlen(*argv) - 1;
for ( start = end; (*argv)[start - 1] != '/'; --start )
  ;
```

Biến `end` nằm tại vị trị cuối chuỗi `argv[0]` và biến `start` sau khi hết vòng `for` sẽ nằm tại vị trí sau dấu `/` cuối cùng. Cụ thể trong máy mình thì sau khi thực thi vòng `for` thì `argv[0][start:end] = racecars` và đây chính là tên file thực thi của mình : )

Để chương trình in ra màn hình `That's exactly what I wanted!` thì chuỗi `argv[0]` từ vị trí `start` đến `end` phải là chuỗi đối xứng (hay là chuỗi **palindrome**)
Suy ra t cần đổi tên file thành chuỗi palindrome

```zsh
└─$ mv racecars aa
```

## Execute

```zsh
└─$ ./aa
That's exactly what I wanted!
```

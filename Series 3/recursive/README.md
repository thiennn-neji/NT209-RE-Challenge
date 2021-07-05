# recursive
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `CRACKME.exe`
```zsh
└─$ file CRACKME.exe
CRACKME.exe: PE32 executable (console) Intel 80386, for MS Windows
```
Đây là file thực thi trên Windows 32-bit, `console`

### Assembly
Mở IDA Pro và tìm xem các String
![image](https://user-images.githubusercontent.com/59532111/124500762-86e25e00-ddea-11eb-9392-f2f9cbbb5090.png)

Thấy có một chuỗi là `SUCCESS! tell us how this crackme was solved`. Vậy mình cần tìm xem làm sao để chương trình in ra chuỗi đó.

Trong bài này, mình không dùng `pseudocode` của IDA làm công cụ hỗ trợ chính cho `crack` vì khi mình thử `disassembly` hàm main thì có quá nhiều và code nó khá rối, rối tung mù cả lên. Thay vào đó, chế độ `graph overview`của IDA cho mình cái nhìn tổng quan hơn khi chương trình thực hiện các hàm, khối lệnh.

### Start - `sub_FA1300`

Mình bắt đầu từ manh mối là chuỗi success ở trên, và xem tham chiếu thì thấy nó được gọi trong hàm **`sub_FA1300`**

![image](https://user-images.githubusercontent.com/59532111/124501472-ce1d1e80-ddeb-11eb-8d72-8a7a4d78107a.png)

Và đây là sơ đồ cho toàn bộ hàm `sub_FA1300`

<div align="center">
    <img src="https://user-images.githubusercontent.com/59532111/124501900-9e224b00-ddec-11eb-94f8-927b6c90fa12.png"/>
</div>

Và mình lên đầu của hàm `sub_FA1300`, tìm xem nó được gọi từ đâu
![image](https://user-images.githubusercontent.com/59532111/124502071-ef323f00-ddec-11eb-817e-e054da972f28.png)

Vậy là nó được gọi 1 lần (đỡ được một chút) và trong hàm `main` (good :> ) tại vị trí `_main + 6F5`. Và đây là tổng quan hàm `main` cũng như vị trí câu lệnh gọi hàm `sub_FA1300`
<div align="center">
    <img src="https://user-images.githubusercontent.com/59532111/124502431-ac249b80-dded-11eb-91f0-961c4480342d.png"/>
</div>

### Next - Hàm `main` và những `block` "thừa"

Đầu tiên mình xem xét block đầu tiên trong hàm `main` (chế độ text) và tìm thấy nơi nhận input vào

![image](https://user-images.githubusercontent.com/59532111/124503675-3d950d00-ddf0-11eb-9e96-82c007d6a242.png)

Và khi debug thực tế, thì `ebp+Src` trong hàm `main` là nơi lưu giữ chuỗi input.

Trở lại với hàm `main`, sau khi lưu input tại `ebp+Src` thì những khối lệnh sau khá là dư thừa
<div align="center">
    <img src="https://user-images.githubusercontent.com/59532111/124504260-4cc88a80-ddf1-11eb-845f-fb10d39580c0.png"/>
</div>

Ví dụ với một khối lệnh (block) trong số các block đầu tiên
<div align="center">
    <img src="https://user-images.githubusercontent.com/59532111/124504560-f3ad2680-ddf1-11eb-9354-2fbf9bb9b1fe.png"/>
</div>

Nó sẽ so sánh kí tự đầu tiên trong chuỗi input (lưu tại `ebp+Src`, và tại `eax`) với một số kí tự, theo thứ tự từng block là '1', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'w', 'f'. Nhưng thực tế khi debug, cũng như đọc assembly thì khi kí tự đầu là một trong các kí tự trên, nó chưa cho thấy có tác dụng gì. Bình thường, các câu lệnh chạy bình thường (trừ trường hợp throw exception) thì nó lại tiếp tục xuống các block tương tự phía dưới, không làm thay đổi giá trị tại `ebp+Src`.

Vậy nên mình sẽ bỏ qua đoạn này và đến thẳng nơi gọi `sub_FA1300`

### Trong hàm `main`, nơi gọi `sub_FA1300`

<div align="center">
    <img src="https://user-images.githubusercontent.com/59532111/124505236-39b6ba00-ddf3-11eb-8162-24917dfb1881.png"/>
</div>

Một vài lệnh asm đáng chú ý

```asm
lea     eax, (ebp+Src)
mov     ecx, esp
push    eax             ; Src
call    sub_FA2550
call    sub_FA1300
```

Thì gọi 2 hàm, hàm `sub_FA2550`, và `sub_FA1300` tham số là chuỗi input (push `eax` với `eax = ebp+Src`)
Đọc code và debug thì hàm `sub_FA2550` (dù mình chưa rõ nó làm gì) nhưng đây không phải là nơi mình cần, cũng như không thay đổi chuỗi input của mình.

### Hàm `sub_FA1300`

Trong hàm này, mình đi từ trên xuống theo hướng các mũi tên, kết hợp `debug` động với chuỗi, thì các khối lệnh dưới đây chính là so sánh các kí tự trong chuỗi input.

<div align="center">
    <div>
        <img src="https://user-images.githubusercontent.com/59532111/124505779-6fa86e00-ddf4-11eb-828a-e366ee78848c.png"/>
    </div>
    <br/><br/>
    <p align="left">Cụ thể từng kí tự được so sánh như sau. Và 6 kí tự theo thứ tự là 's', 't', 'o', 'p', 'i', 't'</p>
    <div>
        <img src="https://user-images.githubusercontent.com/59532111/124505807-7e8f2080-ddf4-11eb-88e9-5d8b4018053e.png"/>
        <img src="https://user-images.githubusercontent.com/59532111/124505956-d29a0500-ddf4-11eb-86a6-fe56f53ce9d0.png"/>
        <img src="https://user-images.githubusercontent.com/59532111/124505892-b4cca000-ddf4-11eb-8d4f-fa6b8c6d6f2a.png"/>
        <img src="https://user-images.githubusercontent.com/59532111/124505904-bdbd7180-ddf4-11eb-8555-ea8b9e248053.png"/>
        <img src="https://user-images.githubusercontent.com/59532111/124505925-c57d1600-ddf4-11eb-84cd-e5c9d9a94cf6.png"/>
        <img src="https://user-images.githubusercontent.com/59532111/124505946-cd3cba80-ddf4-11eb-8686-2da59b87df15.png"/>
    </div>
</div>

Nếu so sánh đúng thì `esi` tăng lên 1 đơn vị. Và để có thể nhảy đến vị trị xử lí chuỗi success thì `esi` cần bằng `6` tức là 6 kí tự đầu tiên phải so sánh đúng
<div align="center">
    <img src="https://user-images.githubusercontent.com/59532111/124506539-0d506d00-ddf6-11eb-88d5-384f65058e8d.png"/>
</div>

### Kết luận

Vậy input cần tìm là chuỗi có 6 kí tự đầu tiên là `stopit`. Mình khi nhập vào thì không có gì được in ra màn hình. Nhưng khác với khi nhập những chuỗi khác. Thì có 1 file txt mới được tạo ra (với một tên file random), có nội dung là `SUCCESS! tell us how this crackme was solved`

## Execute

```bash
> ls -la
total 44
drwxr-xr-x 1 thien thien     0 Jul  6 01:08 .
drwxr-xr-x 1 thien thien     0 Jul  3 17:15 ..
-rwxr-xr-x 1 thien thien 38400 Jul  3 10:13 CRACKME.exe

> .\CRACKME.exe
PASSWORD: stopit

> ls -la
total 45
drwxr-xr-x 1 thien thien     0 Jul  6 01:08 .
drwxr-xr-x 1 thien thien     0 Jul  3 17:15 ..
-rwxr-xr-x 1 thien thien 38400 Jul  3 10:13 CRACKME.exe
-rw-r--r-- 1 thien thien    44 Jul  6 01:08 sU6FUHhfr2aN3

> cat .\sU6FUHhfr2aN3
SUCCESS! tell us how this crackme was solved
```
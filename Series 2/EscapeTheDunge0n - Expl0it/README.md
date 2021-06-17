# no strings attached
## Solution
### Architecture
Dùng lệnh `file` để xác định kiến trúc của file thực thi `CrackMe.exe`
```zsh
└─$ file CrackMe.exe
CrackMe.exe: PE32 executable (console) Intel 80386, for MS Windows
```
Đây là file thực thi trên giao diện `console` `Windows 32-bit`

### Disassembly
Vì đọc hàm `main` mình chưa tìm ra bất cứ chuỗi nào liên quan đến việc giải đúng như "chúc mừng" hay "good password". Nên mình sử dụng view string của IDA. Lúc này đọc hết vẫn không tìm thấy, bấm thử vào string bất kì để xem trong assembly như nào thì đã tìm được
```c
.rdata:00403238 aKeyCode31m     db 'Key Code:',0Ah      ; DATA XREF: sub_401000+39D↑o
.rdata:00403238                 db 1Bh,'[31m$ ',0
.rdata:0040324A                 align 4
.rdata:0040324C ; const WCHAR aCongratulation
.rdata:0040324C aCongratulation:                        ; DATA XREF: sub_401000+3C2↑o
.rdata:0040324C                 text "UTF-16LE", 'CONGRATULATIONS!!!',0
.rdata:00403272                 align 8
.rdata:00403278 ; const WCHAR aCongratulation_0
.rdata:00403278 aCongratulation_0:                      ; DATA XREF: sub_401000+3C7↑o
.rdata:00403278                 text "UTF-16LE", 'Congratulations you won! You are a good cracker...',0Ah
.rdata:00403278                 text "UTF-16LE", ' @Expl0it',0
.rdata:004032F2                 align 4
.rdata:004032F4 ; const char aPause[]
.rdata:004032F4 aPause          db 'pause',0            ; DATA XREF: sub_401000:loc_4011DD↑o
.rdata:004032FA                 align 4
.rdata:004032FC ; const WCHAR aYouLost
.rdata:004032FC aYouLost:                               ; DATA XREF: sub_401000+3D7↑o
.rdata:004032FC                 text "UTF-16LE", 'YOU LOST!',0
.rdata:00403310 ; const WCHAR aYouLostTheGame
.rdata:00403310 aYouLostTheGame:                        ; DATA XREF: sub_401000+3DC↑o
.rdata:00403310                 text "UTF-16LE", 'You lost the game...Try again',0
.rdata:0040334C                 align 10h
```
Chuỗi `CONGRATULATIONS!!!` được gọi trong hàm `sub_401000`

#### Hàm `main`
Một phần hàm `main`:
```c
v8 = sub_401770(
       v7,
       "Welcome to the Dungeon! You have to solve the challenges and escape the Dungeon with a Secret Key. Survive! You"
       " have got only 100% health, be carefully!\n");
sub_401770(v8, "\x1B[0m\t\t");
sub_401770(std::cout, "PRESS [1] to play or [2] to exit\n\x1B[31m$Dunge0n ");
std::istream::operator>>(std::cin, v10);
if ( v10[0] == 1 )
{
  sub_401000();
  return 0;
}
if ( v10[0] == 2 )
  return 0;
sub_401770(std::cout, "Wrong enter, try again!");
Sleep(0x1388u);
return main(v10[0], (const char **)v10[1], savedregs);
```
Mình cần làm là phải vào được hàm  `sub_401000`. Nên kí tự đầu tiên nhập phải là `1`
#### Trò chơi
```c
int sub_401000()
{
  int v0; // eax
  int v1; // eax
  int v2; // eax
  int v3; // eax
  int v4; // eax
  int v5; // eax
  int v6; // eax
  int v7; // eax
  const char *v8; // edx
  int v9; // eax
  int v10; // eax
  int v12; // eax
  int v13; // eax
  int *v14; // eax
  int v15; // eax
  int v16; // eax
  int v17; // eax
  int v18; // eax
  int v19; // eax
  int v20; // eax
  int v21; // eax
  int v22; // eax
  int v23; // eax
  int v24; // eax
  int v25; // eax
  int v26; // eax
  int v27; // eax
  int v28; // eax
  int v29; // [esp+Ch] [ebp-14h] BYREF
  int v30; // [esp+10h] [ebp-10h] BYREF
  int v31; // [esp+14h] [ebp-Ch] BYREF
  int v32; // [esp+18h] [ebp-8h] BYREF

  SetConsoleTitleW(L"Dunge0n                                   @made by Expl0it");
  system("cls");
  v0 = sub_401770(std::cout, "\x1B[31m");
  v1 = sub_401770(v0, "HEALTH: ");
  std::ostream::operator<<(v1, 100);
  sub_401770(
    std::cout,
    "\n"
    "\n"
    "You are in the Dungeon and have to choose a way, because they are 2 ways. But be carefully you can come across a Dragon.\n");
  sub_401770(std::cout, "[1] go right\n[2] go left\n\x1B[31m$ ");
  std::istream::operator>>(std::cin, &v30);
  if ( v30 == 1 )
  {
    system("cls");
    sub_401770(
      std::cout,
      "Oh no. There are poison traps in this way, shit -10 HP it hurts! Oh no and a rock is roling behind us we have to r"
      "un, shit We fell down somewhere :( Another -10 HP. \n");
    v2 = sub_401770(std::cout, "\x1B[31m");
    v3 = sub_401770(v2, "HEALTH: ");
    std::ostream::operator<<(v3, 80);
    Sleep(0x1F40u);
    system("cls");
    v4 = sub_401770(std::cout, "\x1B[31m");
    v5 = sub_401770(v4, "HEALTH: ");
    std::ostream::operator<<(v5, 80);
    sub_401770(
      std::cout,
      "\n"
      "\n"
      "Ah hmm where I am?! Wait what? GOLDDDD everywhere!!! Oh no glad to early... \n"
      "A Goblin is there. Shit he seen me already. He is coming... But there is a way hmmm but i have otherwise a Glock.\n");
    sub_401770(std::cout, "PRESS [1] to grab Gold and run into the way or [2] to fight with the Goblin\n\x1B[31m$ ");
    std::istream::operator>>(std::cin, &v32);
    if ( v32 == 1 )
    {
      system("cls");
      sub_401770(
        std::cout,
        "Oh no another trap it wasnt a way... It's a room :( The ceiling is going down and have spikes...\n");
      v6 = sub_401770(std::cout, "\n\n\x1B[31m");
      v7 = sub_401770(v6, "HEALTH: ");
      std::ostream::operator<<(v7, 0);
      v8 = "\n\n\x1B[96mOh no you lost the Game... I wish you good luck with the next try :) @Expl0it\n";
LABEL_6:
      sub_401770(std::cout, v8);
      return system("pause");
    }
    if ( v32 == 2 )
    {
      system("cls");
      v9 = sub_401770(std::cout, "\x1B[31m");
      v10 = sub_401770(v9, "HEALTH: ");
      std::ostream::operator<<(v10, 0);
      v8 = "\n"
           "\n"
           "\x1B[96mOh no the Goblin killed you... You lost the Game... I wish you good luck with the next try :) @Expl0it\n";
      goto LABEL_6;
    }
    system("cls");
    sub_401770(std::cout, "Wrong enter, try again!\n ");
    v12 = sub_401770(std::cout, "\x1B[31m");
    v13 = sub_401770(v12, "HEALTH: ");
    std::ostream::operator<<(v13, 80);
    sub_401770(
      std::cout,
      "\n"
      "Ah hmm where I am?! Wait what? GOLDDDD everywhere!!! Oh no glad to early... A Goblin is there. Shit he seen me alr"
      "eady. He is coming... But there is a way hmmm but i have otherwise a Glock.\n");
    sub_401770(std::cout, "PRESS [1] to grab Gold and run into the way or [2] to fight with the Goblin\n\x1B[31m$ ");
    v14 = &v32;
  }
  else if ( v30 == 2 )
  {
    system("cls");
    v15 = sub_401770(std::cout, "\x1B[31m");
    v16 = sub_401770(v15, "HEALTH: ");
    std::ostream::operator<<(v16, 100);
    sub_401770(
      std::cout,
      "\n"
      "\n"
      "Shit you stepped right in the arms of the dragon :( oh but what is that? There is a chest next to the dragon. Oh a"
      "nd there is a Way behind him.\n");
    sub_401770(std::cout, "PRESS [1] to go to the chest or [2] to sneak pass the dragon\n\x1B[31m$ ");
    std::istream::operator>>(std::cin, &v31);
    if ( v31 == 1 )
    {
      system("cls");
      v17 = sub_401770(std::cout, "\x1B[31m");
      v18 = sub_401770(v17, "HEALTH: ");
      std::ostream::operator<<(v18, 100);
      sub_401770(std::cout, "\nHell yes a Sword and the Secret Key! Oh no a rock fellt on the dragon...\n");
      sub_401770(std::cout, "PRESS [1] to run or [2] to fight\n\x1B[31m$ ");
      std::istream::operator>>(std::cin, &v32);
      if ( v32 == 1 )
      {
        v19 = sub_401770(std::cout, "\x1B[31m");
        v20 = sub_401770(v19, "HEALTH: ");
        std::ostream::operator<<(v20, 0);
        v8 = "\n"
             "\n"
             "\x1B[96mOh no you tripped and the Dragon killed you...You lost the Game... I wish you good luck with the ne"
             "xt try :) @Expl0it\n";
        goto LABEL_6;
      }
      if ( v32 == 2 )
      {
        MessageBoxW(
          0,
          L"You killed the Dragon and won the game good job, congratulations! But Whats the Secret Key code now?",
          L"Wait what?!?!",
          0x40u);
        system("cls");
        sub_401770(std::cout, "Key Code:\n\x1B[31m$ ");
        std::istream::operator>>(std::cin, &v29);
        if ( v29 == 788960 )
          MessageBoxW(0, L"Congratulations you won! You are a good cracker...\n @Expl0it", L"CONGRATULATIONS!!!", 0x40u);
        else
          MessageBoxW(0, L"You lost the game...Try again", L"YOU LOST!", 0x10u);
        return system("pause");
      }
      system("cls");
      sub_401770(std::cout, "Wrong enter, try again!\n ");
      v21 = sub_401770(std::cout, "\x1B[31m");
      v22 = sub_401770(v21, "HEALTH: ");
      std::ostream::operator<<(v22, 100);
      sub_401770(std::cout, "\nHell yes a Sword and the Secret Key! Oh no a rock fellt on the dragon...\n");
      sub_401770(std::cout, "PRESS [1] to run or [2] to fight\n\x1B[31m$");
      v14 = &v32;
    }
    else
    {
      if ( v31 == 2 )
      {
        system("cls");
        sub_401770(std::cout, "Shit the dragon has woken up you are dead...\n\n");
        v23 = sub_401770(std::cout, "\x1B[31m");
        v24 = sub_401770(v23, "HEALTH: ");
        std::ostream::operator<<(v24, 0);
        v8 = "\n"
             "\n"
             "\x1B[96mOh no the Dragon killed you... You lost the Game... I wish you good luck with the next try :) @Expl0it\n";
        goto LABEL_6;
      }
      system("cls");
      sub_401770(std::cout, "Wrong enter, try again!\n ");
      v25 = sub_401770(std::cout, "\x1B[31m");
      v26 = sub_401770(v25, "HEALTH: ");
      std::ostream::operator<<(v26, 100);
      sub_401770(
        std::cout,
        "\n"
        "Shit you stepped right in the arms of the dragon :( oh but what is that? There is a chest next to the dragon. Oh"
        " and there is a Way behind him.");
      sub_401770(std::cout, "PRESS [1] to go to the chest or [2] to sneak pass the dragon\n\x1B[31m$ ");
      v14 = &v31;
    }
  }
  else
  {
    system("cls");
    sub_401770(std::cout, "\nWrong enter, try again!\n ");
    v27 = sub_401770(std::cout, "\x1B[31m");
    v28 = sub_401770(v27, "HEALTH: ");
    std::ostream::operator<<(v28, 100);
    sub_401770(
      std::cout,
      "\n"
      "You are in the Dungeon and have to choose a way, because they are 2 of these. But be careful you can come across a Dragon\n");
    sub_401770(std::cout, "[1] go right\n[2] go left\n\x1B[31m$ ");
    v14 = &v30;
  }
  return std::istream::operator>>(std::cin, v14);
}
```

Và đây là khối lệnh con có chứa chuỗi `CONGRATULATIONS!!!` 
```c
if ( v32 == 2 )
      {
        MessageBoxW(
          0,
          L"You killed the Dragon and won the game good job, congratulations! But Whats the Secret Key code now?",
          L"Wait what?!?!",
          0x40u);
        system("cls");
        sub_401770(std::cout, "Key Code:\n\x1B[31m$ ");
        std::istream::operator>>(std::cin, &v29);
        if ( v29 == 788960 )
          MessageBoxW(0, L"Congratulations you won! You are a good cracker...\n @Expl0it", L"CONGRATULATIONS!!!", 0x40u);
        else
          MessageBoxW(0, L"You lost the game...Try again", L"YOU LOST!", 0x10u);
        return system("pause");
      }
```
Theo vết ngược lên đầu hàm  `sub_401000` theo từng khối lệnh để tìm vị trí của chuỗi `CONGRATULATIONS!!!` thì các kí tự được nhập lần lượt là `2`, `1`, `2`

Và cuối cùng, để có thể thành công thì cần phải nhập đúng `Secret key`, chương trình kiểm tra ` if ( v29 == 788960 )` và `v29` là biến kiểu int. Nên `Secret key` cần nhập là `788960`

#### Kết luận
Nhập `1` `2` `1` `2` để vào được mode nhập `Secret key`

`Secret key` là `788960`.
## Execute


---
title: "Linux Shell"
date: 2019-11-14T20:26:47+08:00
draft: true
---

# 特殊字符用来处理参数
```
$#  传递到脚本的参数个数
$* 	以一个单字符串显示所有向脚本传递的参数。
    如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。
$$ 	脚本运行的当前进程ID号
$! 	后台运行的最后一个进程的ID号
$@ 	与$*相同，但是使用时加引号，并在引号中返回每个参数。
    如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。
$- 	显示Shell使用的当前选项，与set命令功能相同。
$? 	显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。
```

# 关系运算符
```
-eq 	检测两个数是否相等，相等返回 true。 	[ $a -eq $b ] 返回 false。
-ne 	检测两个数是否不相等，不相等返回 true。 	[ $a -ne $b ] 返回 true。
-gt 	检测左边的数是否大于右边的，如果是，则返回 true。 	[ $a -gt $b ] 返回 false。
-lt 	检测左边的数是否小于右边的，如果是，则返回 true。 	[ $a -lt $b ] 返回 true。
-ge 	检测左边的数是否大于等于右边的，如果是，则返回 true。 	[ $a -ge $b ] 返回 false。
-le 	检测左边的数是否小于等于右边的，如果是，则返回 true。 	[ $a -le $b ] 返回 true。
```

# 文件测试符
```
-b file 	检测文件是否是块设备文件，如果是，则返回 true。 	[ -b $file ] 返回 false。
-c file 	检测文件是否是字符设备文件，如果是，则返回 true。 	[ -c $file ] 返回 false。
-d file 	检测文件是否是目录，如果是，则返回 true。 	[ -d $file ] 返回 false。
-f file 	检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。 	[ -f $file ] 返回 true。
-g file 	检测文件是否设置了 SGID 位，如果是，则返回 true。 	[ -g $file ] 返回 false。
-k file 	检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。 	[ -k $file ] 返回 false。
-p file 	检测文件是否是有名管道，如果是，则返回 true。 	[ -p $file ] 返回 false。
-u file 	检测文件是否设置了 SUID 位，如果是，则返回 true。 	[ -u $file ] 返回 false。
-r file 	检测文件是否可读，如果是，则返回 true。 	[ -r $file ] 返回 true。
-w file 	检测文件是否可写，如果是，则返回 true。 	[ -w $file ] 返回 true。
-x file 	检测文件是否可执行，如果是，则返回 true。 	[ -x $file ] 返回 true。
-s file 	检测文件是否为空（文件大小是否大于0），不为空返回 true。 	[ -s $file ] 返回 true。
-e file 	检测文件（包括目录）是否存在，如果是，则返回 true。 	[ -e $file ] 返回 true。
```

# cut 
```
-b ：以字节为单位进行分割。这些字节位置将忽略多字节字符边界，除非也指定了 -n 标志。
-c ：以字符为单位进行分割。
-d：自定义分隔符，默认为制表符。
-f：与-d一起使用，指定显示哪个区域。
-n：取消分割多字节字符。
```

# sed
```
-e  <script>或--expression=<script> 以选项中指定的script来处理输入的文本文件。
-f  <script文件>或--file=<script文件> 以选项中指定的script文件来处理输入的文本文件。
-n  或--quiet或--silent 仅显示script处理后的结果。
a ：新增， a 的后面可以接字串，而这些字串会在新的一行出现(目前的下一行)～
c ：取代， c 的后面可以接字串，这些字串可以取代 n1,n2 之间的行！
d ：删除，因为是删除啊，所以 d 后面通常不接任何咚咚；
i ：插入， i 的后面可以接字串，而这些字串会在新的一行出现(目前的上一行)；
p ：打印，亦即将某个选择的数据印出。通常 p 会与参数 sed -n 一起运行～
s ：取代，可以直接进行取代的工作哩！通常这个 s 的动作可以搭配正规表示法！
例子：
1 在第四行后添加新字符串
    sed -e 4a\newline testfile  
2 第二行后面加入两行字
    nl /etc/passwd | sed '2a Drink tea or ......\
    > drink beer ?'
3 第2-5行的内容取代成为『No 2-5 number』
    nl /etc/passwd | sed '2,5c No 2-5 number'
4 搜索 /etc/passwd有root关键字的行
    nl /etc/passwd | sed '/root/p'
5 删除/etc/passwd所有包含root的行，其他行输出
    nl /etc/passwd | sed  '/root/d'
6 搜索/etc/passwd,找到root对应的行，执行后面花括号中的一组命令，每个命令之间用分号分隔，这里把bash替换为blueshell，再输出这行
    nl /etc/passwd | sed -n '/root/{s/bash/blueshell/;p;q}' 
```

# awk
```

    -F fs or --field-separator fs
    指定输入文件折分隔符，fs是一个字符串或者是一个正则表达式，如-F:。
    -v var=value or --asign var=value
    赋值一个用户定义变量。
    -f scripfile or --file scriptfile
    从脚本文件中读取awk命令。
    -mf nnn and -mr nnn
    对nnn值设置内在限制，-mf选项限制分配给nnn的最大块数目；-mr选项限制记录的最大数目。这两个功能是Bell实验室版awk的扩展功能，在标准awk中不适用。
    -W compact or --compat, -W traditional or --traditional
    在兼容模式下运行awk。所以gawk的行为和标准的awk完全一样，所有的awk扩展都被忽略。
    -W copyleft or --copyleft, -W copyright or --copyright
    打印简短的版权信息。
    -W help or --help, -W usage or --usage
    打印全部awk选项和每个选项的简短说明。
    -W lint or --lint
    打印不能向传统unix平台移植的结构的警告。
    -W lint-old or --lint-old
    打印关于不能向传统unix平台移植的结构的警告。
    -W posix
    打开兼容模式。但有以下限制，不识别：/x、函数关键字、func、换码序列以及当fs是一个空格时，将新行作为一个域分隔符；操作符**和**=不能代替^和^=；fflush无效。
    -W re-interval or --re-inerval
    允许间隔正则表达式的使用，参考(grep中的Posix字符类)，如括号表达式[[:alpha:]]。
    -W source program-text or --source program-text
    使用program-text作为源代码，可与-f命令混用。
例子:
1 每行按空格或TAB分割，输出文本中的1、4项
    awk '{print $1,$4}' log.txt.
2 使用","分割
    awk -F, '{print $1,$2}'   log.txt
3 使用多个分隔符。先使用空格分割，然后对分割结果再使用","分割
    awk -F '[ ,]'  '{print $1,$2,$5}'   log.txt
4 输出第二列包含 "th"，并打印第二列与第四列
    awk '$2 ~ /th/ {print $2,$4}' log.txt
```
---
title: "Linux 重置密码"
date: 2019-11-12T19:49:21+08:00
draft: true
---

1 设置随机密码
```
openssl rand -base64 16 | passwd --stdin root
lab rootpw setup
```
2 重启,在开机时按F2  
3 在加载linux内核的地方添加
```
rd.break
```
4 查看/sysroot的挂载情况  
```
mount
```
5 用读写的方式挂载  
```
mount -o remount,rw /sysroot
```
6 进入linux终端
```
chroot /sysroot/
```
7 修改密码
```
1 passwd root
2 echo redhat|passwd --stdin root
```
8 添加启动扫描文件
```
touch /.autorelabel 
```
9 重启
```
exit
exit
reboot
```


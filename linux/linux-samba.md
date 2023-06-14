---
title: "Linux Samba共享文件"
date: 2019-11-26T16:44:32+08:00
draft: true
---


1 安装samba
```
yum install -y samba*
```
2 添加用户
```
useradd smbuser
```
3 设置共享文件用户的密码
```
smbpasswd -a smbuser
```
4 创建公共共享文件
```
mkdir /home/share
chmod 777 /home/share
```
5 修改smb的配置文件
```
vim /etc/samba/smb.conf
# max protocol = used to define the supported protocol. The default is NT1.
# can set it to SMB2 if you want experimental SMB2 support.

        workgroup = MYGROUP
        server string = Samba Server Version %v

;       netbios name = MYSERVER


;       interfaces = lo eth0 ens160   192.168.12.2/24 192.168.13.2/24 192.168.0.108
;       hosts allow = 127. 192.168.12. 192.168.13. 192.168.0.

;	max protocol = SMB2
[global]
	workgroup = SAMBA
	security = user
		path = /win
		public = on
		writable = yes
[public]
	comment = Public File
	path = /home/share
	available = yes
	valid users = smbuser
	read only = no
	browsable = yes
	public = yes
	writable = yes
```
6 关闭防火墙
```
systemctl stop firewalld.service
```
7 查看SELinux模式
```
[root@localhost ~]# sestatus
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Max kernel policy version:      31
```
8 修改SELinux模式
```
[root@localhost ~]# setenforce 0
[root@localhost ~]# sestatus
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   permissive
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Max kernel policy version:      31
```
9 启动smb
```
1 service smb status
2 systemctl start smb
```
10 打开windwos，我的电脑，输入\\192.168.0.108
11 输入smbuser和密码  

参考资料：
```
https://blog.csdn.net/blade2001/article/details/19963769
https://www.cnblogs.com/yongestcat/p/11438648.html
```

---
title: "Linux Pptpd"
date: 2019-11-26T12:36:17+08:00
draft: true
---

# 准备环境
```
1 主机ip:192.168.0.107  
2 VPN服务器:  
    ens32:192.168.0.102  
    ens33:127.16.1.10
```

# 软件安装
```
[root@localhost ~]# yum install -y ppp pptpd
注意:若无法下载pptpd
    1 配置阿里云的yum源
    2 手动下载pptpd.rpm  http:##poptop.sourceforge.net/yum/stable/packages/
```

# pptpd.conf
```
[root@localhost ~]# vim /etc/pptpd.conf			##编辑pptpd的默认匹配文件
option /etc/ppp/options.pptpd
logwtmp
localip 192.168.0.102			##这个ip为虚拟机的ip地址，也就是我们在linux中用ifconfig查询出来的ip
remoteip 172.16.1.20-80		##自动分配ip范围，这里不要包含虚拟机的ip，否则会发生冲突

##说明：localip 是本机的外网IP地址；remoteip 是为接入的VPN客户端分配的IP地址范围。
```

# options.pptpd
```
[root@localhost ~]# vim /etc/ppp/options.pptpd
##有效行：如果此文件为空，添加这些行就可以
name pptpd    ##相当于身份验证时的域，一定要和/etc/ppp/chap-secrets中的内容对应
refuse-pap            		##拒绝pap身份验证
refuse-chap           		##拒绝chap身份验证
refuse-mschap        		##拒绝mschap身份验证
require-mschap-v2     		##采用mschap-v2身份验证方式
require-mppe-128      		##在采用mschap-v2身份验证方式时要使用MPPE进行加密
ms-dns 192.168.0.107    		##给客户端分配DNS服务器地址
ms-dns 8.8.8.8
proxyarp             		##启动ARP代理
debug					##开启调试模式，相关信息同样记录在 /var/logs/message 中。
lock						##锁定客户端 PTY 设备文件。
nobsdcomp				##禁用 BSD 压缩模式。
novj	            
novjccomp				##禁用 Van Jacobson 压缩模式。
nologfd					##禁止将错误信息记录到标准错误输出设备(stderr)
```

# chap-secrets
也就是我们一会在windows上登陆时用到的帐号和密码
```
[root@localhost ~]# vim /etc/ppp/chap-secrets 
# Secrets for authentication using CHAP
# client        server                  secret                  IP addresses
    zyc          pptpd                  123                           *
    root         *                      456                           *
    用户名      服务类型(*代表所有)       密码                          连入的ip(*代表任意地址)
```

# sysctl.conf
```
[root@localhost ~]# vim /etc/sysctl.conf 
net.ipv4.ip_forward = 1 					##数值改为“1”,没有则追加
[root@RHEL6 etc]# sysctl –p				##启用转发功能
net.ipv4.ip_forward = 1
```

# 启动服务并查看端口
```
[root@localhost ~]# service pptpd start		##启动服务
[root@localhost ~]# netstat -tnlp | grep pptpd				##查看端口
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:1723            0.0.0.0:*               LISTEN      63854/pptpd
```

# 防火墙
```
systemctl stop firewalld
iptables -I INPUT -p tcp --dport 1723 -j ACCEPT		##允许默认端口通过
iptables -I INPUT -p tcp --dport 47 -j ACCEPT
iptables -I INPUT -p gre -j ACCEPT
iptables -t nat -A POSTROUTING -s 172.16.1.10/24 -j SNAT --to 192.168.0.107				##转发从内网ip的数据到本机ip
iptables -t nat -A POSTROUTING -o ens33 -s 192.168.0.0/24  -j MASQUERADE	
iptables-save   
```

# 主机连接
```
设置-》网络与Internet-》VPN-》添加VPN连接
VPN提供商为Windows内置,连接名称随意,服务器地址为192.168.0.107,VPN协议选点对点隧道协议,登录类型选用户与密码
输入用户与密码
```


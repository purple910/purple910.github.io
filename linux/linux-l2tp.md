---
title: "Linux L2tp"
date: 2019-11-26T12:36:58+08:00
draft: true
---


# 准备环境
```
1 主机ip:192.168.0.107  
2 VPN服务器:  
    ens32:192.168.0.102  
    ens33:127.16.1.10
```

# 环境测试  
先看看你的主机是否支持pptp，返回结果为yes就表示通过
```
modprobe ppp-compress-18 && echo yes
```
是否开启了TUN，有的虚拟机主机需要开启，返回结果为cat: /dev/net/tun: File descriptor in bad state。就表示通过。
```
cat /dev/net/tun
```

# 软件安装
```
[root@localhost ~]# yum install -y xl2tpd libreswan lsof 
注意：若无法安装xl2tp
    yum install -y epel-release
```

# xl2tpd.conf
```
[root@localhost ~]# vim /etc/xl2tpd/xl2tpd.conf
[global]        ##全局选项
[lns default]       ##设置我们要连接的lns的IP地址，或者dns 域名
ip range = 172.16.1.100-172.16.1.199        ##将会由LNS 分配LAC PPP 隧道的IP地址列
local ip = 172.16.1.10      ##被使用作为xl2tpd 自己的IP的地址。
require chap = yes      ##拒绝或者要求，远程连接通过CHAP进行身份验证，以进行ppp身份验证
refuse pap = yes        ##拒绝或者要求，远程连接通过PAP进行身份验证，以进行ppp身份验证。
require authentication = yes        ##拒绝或者要求远程连接进行身份验证
name = LinuxVPNserver
ppp debug = yes     ##允许ppp debug
pppoptfile = /etc/ppp/options.xl2tpd
length bit = yes        ##如果这个设置为yes ，那么将会使用l2tp 数据包有效载荷中的长度位
```

# options.xl2tpd
```
[root@localhost ~]# vim /etc/ppp/options.xl2tpd
# .....
ipcp-accept-local
ipcp-accept-remote
ms-dns  114.114.114.114
ms-dns  8.8.4.4
# ms-wins 192.168.1.2
# ms-wins 192.168.1.4
name xl2tpd
#noccp
auth
#crtscts
idle 1800
mtu 1410
mru 1410
nodefaultroute
debug
#lock
proxyarp
connect-delay 5000
refuse-pap
refuse-mschap
require-mschap-v2
persist
logfile /var/log/xl2tpd.log
```

# ipsec.conf
```
[root@localhost ~]# vim /etc/ipsec.conf      # 只修改以下项，其他默认
config setup
	  protostack=netkey
        dumpdir=/var/run/pluto/		
			 	virtual_private=%v4:10.0.0.0/8,%v4:192.168.0.0/16,%v4:172.16.0.0/12,%v4:25.0.0.0/8,%v4:100.64.0.0/10,%v6:fd00::/8,%v6:fe80::/10     ## # 主要指定拨号分配给客户端的私有地址
include /etc/ipsec.d/*.conf
```

# l2tp-ipsec.conf
```
[root@localhost ~]# vim /etc/ipsec.d/l2tp-ipsec.conf     # 新建如下配置文文件，直接复制的话，前面是很多空格，在启动的时候会报错，需要将空格删除，换成tab的距离，距离相同。不能用空格！
conn L2TP-PSK-NAT
(tab距离)rightsubnet=0.0.0.0/0
        dpddelay=10
        dpdtimeout=20
        dpdaction=clear
        forceencaps=yes
        also=L2TP-PSK-noNAT
conn L2TP-PSK-noNAT
        authby=secret
        pfs=no
        auto=add
        keyingtries=3
        rekey=no
        ikelifetime=8h
        keylife=1h
        type=transport
        left=172.16.1.10    # 这个是网卡的内网IP，后面通过NAT转发
        leftprotoport=17/1701    # 端口，默认1701，不用改
        right=%any
        rightprotoport=17/%any
```

# chap-secrets
也就是我们一会在windows上登陆时用到的帐号和密码
```
[root@localhost ~]# vim /etc/ppp/chap-secrets 
# Secrets for authentication using CHAP
# client        server                  secret                  IP addresses
    root         *                      456                           *
    用户名      服务类型(*代表所有)       密码                          连入的ip(*代表任意地址)
```

# default-secrets
```
[root@localhost ~]# vim /etc/ipsec.d/default.secrets      # 新建如下文件
------------------------------------------------------------------------------------
: PSK "MyPSK"    # 就一行，填上自定义的PSK,为欲共享密钥
```

# sysctl.conf
```
[root@localhost ~]# vim /etc/sysctl.conf    # 添加如下配置到文件中,参数后面不能有空格
net.ipv4.ip_forward = 1

net.ipv4.conf.*.accept_redirects = 0
net.ipv4.conf.*.rp_filter = 0
net.ipv4.conf.*.send_redirects = 0
注：
    *为/proc/sys/net/ipv4/conf/里面所有项目
[root@localhost ~]# sysctl -p    # 加载内核参数使生效
```

# 检查配置
```
ipsec verify     # 检查命令
注：
    # 可能会出现类似如下情况：
    Checking rp_filter                                  [ENABLED]
    /proc/sys/net/ipv4/conf/ens160/rp_filter           [ENABLED]
    /proc/sys/net/ipv4/conf/ens192/rp_filter           [ENABLED]
    # 这是内核参数没有生效，直接依次手动打开这些文件，将 1 改为 0
    # 然后重新执行检查，输出如下内容则OK：
```

# 防火墙
```
firewall-cmd --permanent --add-service=ipsec      # 放行ipsec服务，安装时会自定生成此服务
firewall-cmd --permanent --add-port=1701/udp      # xl2tp 的端口，默认1701
firewall-cmd --permanent --add-port=4500/udp 
firewall-cmd --permanent --add-masquerade      # 启用NAT转发功能。必须启用此功能
firewall-cmd --reload      # 重载配置
```

# 开启服务
```
systemctl enable ipsec     # 设为开机启动
systemctl start ipsec     # 启动服务
```

# 主机连接
```
设置-》网络与Internet-》VPN-》添加VPN连接
VPN提供商为Windows内置-》连接名称随意-》服务器地址为192.168.0.107-》VPN类型选使用欲共享密钥的L2TP/IPsec-》欲共享密钥 MyPSK 
打开网络适配器-》修改VPN连接的属性-》安全-》允许使用这些协议-》勾上CHAP
输入用户与密码
注：若无法连接
windows+r 运行
    输入 services.msc-》查找ipsec policy agent-》确保它在运行
    输入 regedit-》 HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Rasman\Parameters-》添加ProhibitIpSec,类型为 DWORD(32位), vlan为1,修改AllowL2TPWeakCrypto, vlan为 1
    保存退出，重启计算机
```
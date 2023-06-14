---
title: "Linux Openvpn"
date: 2019-11-26T12:37:06+08:00
draft: true
---

# 准备环境
```
1 主机ip:192.168.0.104  
2 VPN服务器:  
    ens32:192.168.0.107  
    ens33:127.16.1.10
```

# 软件安装
```
yum install -y openssl openssl-devel lzo lzo-devel pam pam-devel automake pkgconfig
yum -y install openvpn easy-rsa  ##配置阿里云的yum源
注：这里的easy-rsa是3.0版本的与2.0版本的配置有所区别
```


# 服务端基本配置文件
```
[root@localhost ~]# cp -r /usr/share/easy-rsa/ /etc/openvpn/easy-rsa
[root@localhost ~]# cd /etc/openvpn/easy-rsa/
[root@localhost easy-rsa]# \rm 3 3.0
[root@localhost easy-rsa]# cd 3.0.6/
[root@localhost easy-rsa]# cp -r /usr/share/doc/easy-rsa-3.0.6/vars.example vars
注：若vars.example不在/usr/share/doc/easy-rsa-3.0.6里则可以通过查找文件
    find / -type f -name "vars.example" | xargs -i cp {} . && mv vars.example vars
注：vars可以不用修改,若想修改则
[root@localhost 3.0.6]# egrep '^set_var' vars  # 把下面几行解注释
set_var EASYRSA_REQ_COUNTRY "CN"
set_var EASYRSA_REQ_PROVINCE    "California"
set_var EASYRSA_REQ_CITY    "San Francisco"
set_var EASYRSA_REQ_ORG "Copyleft Certificate Co"
set_var EASYRSA_REQ_EMAIL   "me@example.net"
set_var EASYRSA_REQ_OU      "My Organizational Unit"
```

# 创建一个新的 PKI 和 CA
```
[root@localhost 3.0.6]# pwd
/etc/openvpn/easy-rsa/3.0.6
[root@localhost 3.0.6]# ./easyrsa init-pki  #创建空的pki
Note: using Easy-RSA configuration from: ./vars
init-pki complete; you may now create a CA or requests.
Your newly created PKI dir is: /etc/openvpn/easy-rsa/3.0.6/pki
[root@localhost 3.0.6]# ./easyrsa build-ca nopass #创建新的CA，不使用密码
......
Common Name (eg: your user, host, or server name) [Easy-RSA CA]: *回车*
CA creation complete and you may now import and sign cert requests.
Your new CA certificate file for publishing is at:
/etc/openvpn/easy-rsa/3.0.6/pki/ca.crt
```

# 生成服务端证书
```
[root@localhost 3.0.6]# ./easyrsa gen-req server nopass
......
Common Name (eg: your user, host, or server name) [server]: *回车*
Keypair and certificate request completed. Your files are:
req: /etc/openvpn/easy-rsa/3.0.6/pki/reqs/server.req
key: /etc/openvpn/easy-rsa/3.0.6/pki/private/server.key
```
# 签约服务端证书
```
[root@localhost 3.0.6]# ./easyrsa sign server server
......
Type the word 'yes' to continue, or any other input to abort.
  Confirm request details: *yes*
Using configuration from ./openssl-1.0.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'server'
Certificate is to be certified until Apr  7 14:54:08 2028 GMT (3650 days)
Write out database with 1 new entries
Data Base Updated
Certificate created at: /etc/openvpn/easy-rsa/3.0.6/pki/issued/server.crt
```

# 创建 Diffie-Hellman
```
[root@localhost 3.0.6]# ./easyrsa gen-dh
......
DH parameters of size 2048 created at /etc/openvpn/easy-rsa/3.0.6/pki/dh.pem
```


# 客户端基本配置
```
[root@localhost ~]# cp -r /usr/share/easy-rsa/ /etc/openvpn/client/easy-rsa
[root@localhost ~]# cd /etc/openvpn/client/easy-rsa/
[root@localhost easy-rsa]# \rm 3 3.0
[root@localhost easy-rsa]# cd 3.0.6/
[root@localhost 3.0.6]# cp -r /usr/share/doc/easy-rsa-3.0.6/vars.example vars
```

# 生成客户端证书
```
[root@localhost 3.0.6]# pwd
/etc/openvpn/client/easy-rsa/3.0.6
[root@localhost 3.06]# ./easyrsa init-pki #创建新的pki
......
init-pki complete; you may now create a CA or requests.
Your newly created PKI dir is: /etc/openvpn/client/easy-rsa/3.0.6/pki
[root@localhost 3.0.6]# ./easyrsa gen-req client nopass  #客户证书名为大林，木有密码
......
Common Name (eg: your user, host, or server name) [client]: *回车*
Keypair and certificate request completed. Your files are:
req: /etc/openvpn/client/easy-rsa/3.0.6/pki/reqs/client.req
key: /etc/openvpn/client/easy-rsa/3.0.6/pki/private/client.key
```

# 最后签约客户端证书
```
[root@localhost 3.0.6]# cd /etc/openvpn/easy-rsa/3.0.6/
[root@localhost 3.0.6]# pwd
/etc/openvpn/easy-rsa/3.0.6
[root@localhost 3.0.6]# ./easyrsa import-req /etc/openvpn/client/easy-rsa/3.0.6/pki/reqs/client.req client
......
The request has been successfully imported with a short name of: client
You may now use this name to perform signing operations on this request.
[root@localhost 3.0.6]# ./easyrsa sign client client
......
Type the word 'yes' to continue, or any other input to abort.
  Confirm request details: *yes*
Using configuration from ./openssl-1.0.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'client'
Certificate is to be certified until Apr  8 01:54:57 2028 GMT (3650 days)
Write out database with 1 new entries
Data Base Updated
Certificate created at: /etc/openvpn/easy-rsa/3.0.6/pki/issued/client.crt
```

# 证书整理
## 服务端
```
[root@localhost ~]# mkdir /etc/openvpn/certs
[root@localhost ~]# cd /etc/openvpn/certs/  
[root@localhost certs]# cp /etc/openvpn/easy-rsa/3.0.6/pki/dh.pem .        
[root@localhost certs]# cp /etc/openvpn/easy-rsa/3.0.6/pki/ca.crt .
[root@localhost certs]# cp /etc/openvpn/easy-rsa/3.0.6/pki/issued/server.crt .
[root@localhost certs]# cp /etc/openvpn/easy-rsa/3.0.6/pki/private/server.key .
[root@localhost certs]# ll
总用量 20
-rw-------. 1 root root 1172 4月  11 10:02 ca.crt
-rw-------. 1 root root  424 4月  11 10:03 dh.pem
-rw-------. 1 root root 4547 4月  11 10:03 server.crt
-rw-------. 1 root root 1704 4月  11 10:02 server.key
```
## 客户端
```
[root@localhost certs]# mkdir /etc/openvpn/client/client/
[root@localhost certs]# cp /etc/openvpn/easy-rsa/3.0.6/pki/ca.crt /etc/openvpn/client/client/
[root@localhost certs]# cp /etc/openvpn/easy-rsa/3.0.6/pki/issued/client.crt /etc/openvpn/client/client/
[root@localhost certs]# cp /etc/openvpn/client/easy-rsa/3.0.6/pki/private/client.key /etc/openvpn/client/client/
[root@localhost certs]# ll /etc/openvpn/client/client/
总用量 16
-rw-------. 1 root root 1172 4月  11 10:07 ca.crt
-rw-------. 1 root root 4431 4月  11 10:08 client.crt
-rw-------. 1 root root 1704 4月  11 10:08 dali
```

# server.conf
```
[root@localhost certs]# cp /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/server.conf /etc/openvpn/
[root@localhost certs]# vim /etc/openvpn/server.conf
# Sample Open××× 2.0
port 1194   ##监听哪个TCP/UDP端口
proto udp   ##使用TCP还是UDP协议
dev tun   ##创建的通信隧道类型(路由IP,以太网)
ca /etc/openvpn/certs/ca.crt    ##根证书
cert /etc/openvpn/certs/server.crt    
key /etc/openvpn/certs/server.key   ##私钥
dh /etc/openvpn/certs/dh.pem    ##密钥
auth SHA512
topology subnet
# 当重启OpenVPN时，再次连接的客户端将分配到与上一次分配相同的虚拟IP地址
ifconfig-pool-persist /etc/openvpn/ipp.txt 
# 设置服务器端模式，并提供一个VPN子网，以便于从中为客户端分配IP地址。
# 在此处的示例中，服务器端自身将占用10.8.0.1，其他的将提供客户端使用。
server 17.16.1.0 255.255.255.0
# 推送路由信息到客户端，以允许客户端能够连接到服务器背后的其他私有子网。
# (简而言之，就是允许客户端访问VPN服务器自身所在的其他局域网)
push "route 192.168.1.0 255.255.255.0"
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 223.5.5.5"
push "dhcp-option DNS 223.6.6.6"
client-to-client   #多个终端可以互相访问
keepalive 20 120    ##端每10秒钟ping客户端一次，如果120秒内都没有收到客户端的回复，则表示远程连接已经关闭。
cipher AES-256-CBC    ##选择一个密码加密算法。
comp-lzo    ##连接上启用压缩
#在完成初始化工作之后，降低Open×××守护进程的权限提升安全性能
#该指令仅限于非Windows系统中使用
user nobody
group nobody
duplicate-cn
tls-server
remote-cert-tls client
mode server   ##定义类型
status openvpn-status.log   ##输出一个简短的状态文件，用于显示当前的连接状态，该文件每分钟都会清空并重写一次。
log-append  openvpn.log   ##这是在之前的日志内容后进行追加
max-clients 100   ##允许并发连接的客户端的最大数量
script-security 3
auth-user-pass-verify /etc/openvpn/checkpsw.sh via-env
username-as-common-name
# 持久化选项可以尽量避免访问那些在重启之后由于用户权限降低而无法访问的某些资源。
persist-key
persist-tun
verb 3
```

# 密码验证脚本
```
#!/bin/sh
PASSFILE="/etc/openvpn/psw-file"
LOG_FILE="/var/log/openvpn/openvpn-password.log"
TIME_STAMP=`date "+%Y-%m-%d %T"`
 
if [ ! -r "${PASSFILE}" ]; then
  echo "${TIME_STAMP}: Could not open password file \"${PASSFILE}\" for reading." >> ${LOG_FILE}
  exit 1
fi
 
CORRECT_PASSWORD=`awk '!/^;/&&!/^#/&&$1=="'${username}'"{print $2;exit}' ${PASSFILE}`
 
if [ "${CORRECT_PASSWORD}" = "" ]; then
  echo "${TIME_STAMP}: User does not exist: username=\"${username}\", password=\"${password}\"." >> ${LOG_FILE}
  exit 1
fi
 
if [ "${password}" = "${CORRECT_PASSWORD}" ]; then
  echo "${TIME_STAMP}: Successful authentication: username=\"${username}\"." >> ${LOG_FILE}
  exit 0
fi
 
echo "${TIME_STAMP}: Incorrect password: username=\"${username}\", password=\"${password}\"." >> ${LOG_FILE}
exit 1
chmod 755 /etc/openvpn/checkpsw.sh
```

# pwd-file
```
echo "testuser 123" > /etc/openvpn/psw-file
chmod 644 /etc/openvpn/psw-file
```

# sysctl.conf
```
net.ipv4.ip_forward = 1
```

# 防火墙
```
iptables -t nat -A POSTROUTING -d 172.16.1.0/24 -j SNAT --to-source 172.16.1.10
```

# client.ovpn
```
client
dev tun
proto udp
remote 192.168.0.107 1194
resolv-retry infinite
nobind
auth-user-pass
auth-nocache
persist-key
persist-tun
tls-client
remote-cert-tls server
auth SHA512
cipher AES-256-CBC
comp-lzo
setenv opt block-outside-dns
key-direction 1
verb 3

ca ca.crt
cert client.crt
key client.key
或者：
<ca>
   客户端ca.crt内容
</ca>
<cert>
   客户端client.crt内容
</cert>
<key>
   客户端client.key内容
</key>
```


# 连接
```
1 将client.crt,client.key,ca.crt,ca.key 复制到主机
2 安装openvpn https://www.techspot.com/downloads/5182-openvpn.html
3 在openvpn的安装目录的config目录里创建一个文件
4 将client.ovpn,client.crt,client.key,ca.crt,ca.key放在里面
5 运行openvpn，连接client
注：
  如果一切配置都没问题,但无法连接,则需关闭本机的防火墙
```
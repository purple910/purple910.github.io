---
title: "Linux Apache源码安装"
date: 2019-11-26T16:45:18+08:00
draft: true
---


1 下载安装包
```
apr-1.7.0.tar.gz
apr-util-1.6.1.tar.gz
pcre-8.43.tar.gz
httpd-2.4.41.tar.gz
https://github.com/purple910/Linux
```
2 解压
```
tar -zxf apr-1.7.0.tar.gz
tar -zxf apr-util-1.6.1.tar.gz
tar -zxf pcre-8.43.tar.gz
tar -zxf httpd-2.4.41.tar.gz
```
3 添加httpd对于apr,apr-util,pcre的依赖
```
cp -r apr-1.7.0 httpd-2.4.41/srclib/apr
cp -r util-1.6.1 httpd-2.4.41/srclib/apr-util
cp -r pcre-8.43 httpd-2.4.41/srclib/pcre
```
4 安装apr
```
cd apr-1.7.0
gedit configure(将 $RM "$cfgfile" 注释掉)
./configure --prefix=/usr/local/src/apr
make && make install
```
5 安装apr-util
```
cd .././apr-util-1.6.1
./configure –prefix=/usr/local/src/apr-util –with-apr=/usr/local/src/apr
make && make install
(如果报错 缺少expat.h)
yum install -y expat-devel.x86_64
```
6 安装prce
```
cd .././ pcre-8.43
./configure –prefix=/usr/local/src/pcre
make && make install
```
7 安装httpd
```
cd .././ httpd-2.4.41
./configure --with-included-apr --sysconfdir=/etc/httpd --prefix=/usr/local/src/apache2.4 --with-apr=/usr/local/src/apr --with-apr-util=/usr/local/src/apr-util --with-pcre=/usr/local/src/pcre --enable-so --enable-unixd --enable-rewrite
make && make install
```
8 关闭防火墙
```
server firewall stop
```
9 编辑httpd的配置文件
```
vim /etc/httpd/conf/httpd.conf
#ServerName www.example.com:80
ServerName 172.0.0.1:80
```
10 运行httpd
```
server httpd start
AH00558: httpd: Could not reliably determine the server's fully qualified domain name,using localhost.localdomain. Set the 'ServerName' directive globally to suppress this message
```
## 添加apache的快捷方式
```
cp /usr/local/src/apache2.4/bin/apachectl  /etc/init.d/httpd
ln -s /etc/init.d/httpd /etc/rc.d/S85httpd
 vim /etc/rc.d/init.d/httpd
# chkconfig: 345 85 15
# description: Activates/Deactivates Apache Web Server
```
## 添加密码
1 修改httpd.conf
```
vim /etc/httpd/conf/httpd.conf
<Virtualhost *:80>
	ServerName	www2.jiance.com
	DocumentRoot	/var/www/html2
	<Directory "/var/www/html2">
		AuthName	server-password
		AuthType	basic
		AuthUserfile	/etc/httpd/conf/.htpasswd
		Require	valid-user
	</Directory>
</Virtualhost>
```
2 添加用户
```
htpasswd -mc /etc/httpd/conf/.htpasswd 用户
```
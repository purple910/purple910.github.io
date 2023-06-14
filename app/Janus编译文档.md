# Janus编译文档

## 1.工具安装

```
sudo apt-get install git
// 一般都有
sudo apt-get install make
sudo apt-get install nginx
// 一般都有
sudo apt-get install python
sudo apt-get install net-tools
```

## 2.依赖安装

```
sudo apt install -y libgnutls28-dev libnice-dev libgstreamer1.0-dev meson python3-pip libice-dev libwebsocket-dev libconfig-dev 	libjansson-dev gengetopt libmicrohttpd-dev .....
# 缺少其他再安装
```

```
# 卸载系统自带libsrtp，因为自带一般未编译ssl
apt purge -y libsrtp2-dev libsrtp2-1

# 手动编译libsrtp-2.2.0
wget https://github.com/cisco/libsrtp/archive/v2.2.0.tar.gz
tar xfv v2.2.0.tar.gz
cd libsrtp-2.2.0
./configure --prefix=/usr --enable-openssl
make shared_library && sudo make install
```

## 3.编译janus

```
git clone https://github.com/meetecho/janus-gateway.git
cd janus-gateway/
./autogen.sh 
./configure --prefix=/opt/janus --enable-websockets --enable-http
make
sudo make install
make configs
```

## 4.ssl私有证书生成

```
openssl genrsa -out privkey.pem 2048
openssl req -new -x509 -key privkey.pem -out server.pem -days 365
# 要求输入的根据提示输入，完成后生成server.pem和privkey.pem
```

## 5.修改janus配置

vim /opt/janus/etc/janus/janus.transport.http.jcfg

```
general: {
        #events = true                                  # Whether to notify event handlers about transport events (default=true)
        json = "indented"                               # Whether the JSON messages should be indented (default),
                                                        # plain (no indentation) or compact (no indentation and no spaces)
        base_path = "/janus"                            # Base path to bind to in the web server (plain HTTP only)
        http = false                                    # Whether to enable the plain HTTP interface
        port = 8088                                     # Web server HTTP port
        #interface = "eth0"                             # Whether we should bind this server to a specific interface only
        #ip = "192.168.0.1"                             # Whether we should bind this server to a specific IP address (v4 or v6) only
        # 这个地方需要开启
        https = true                                    # Whether to enable HTTPS (default=false)
        secure_port = 8089                              # Web server HTTPS port, if enabled
        #secure_interface = "eth0"                      # Whether we should bind this server to a specific interface only
        #secure_ip = "192.168.0.1"                      # Whether we should bind this server to a specific IP address (v4 or v6) only
        #acl = "127.,192.168.0."                        # Only allow requests coming from this comma separated list of addresses
}
 
certificates: {
        # 配置4中生成的证书
        cert_pem = "路径/server.pem"
        cert_key = "路径/privkey.pem"
        #cert_pwd = "secretpassphrase"
        #ciphers = "PFS:-VERS-TLS1.0:-VERS-TLS1.1:-3DES-CBC:-ARCFOUR-128"
}
```

## 6.启动janus

```
nohup /opt/janus/bin/janus &
```

## 7.配置nginx

vim /etc/nginx/sites-available/default或 vim/etc/nginx/ngonx.config

```
    server {
        listen 0.0.0.0:443 ssl;
        listen [::]:443 ssl;
        location / {
            root /opt/janus/share/janus/demos;
            try_files $uri $uri/ /index.html;
            index index.htm index.html;
        }
        # 4中生成的证书的路径
        ssl_certificate /home/swx/cert/server.pem;
        ssl_certificate_key /home/swx/cert/privkey.pem;
    }
```

## 8.访问demo

```
https://ip
```



## 9.bug记录

> [ERR] [dtls.c:janus_dtls_srtp_incoming_msg:923] [6228751724242325] Oops, error creating inbound SRTP session for component 1 in stream 1??

```
此问题是libsrtp库问题，卸载原有系统的libsrtp库并手动编译；注意，编译时必须将openssl模块编入
```




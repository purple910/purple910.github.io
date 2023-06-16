# 使用nginx配置多个反向代理





## 方案1、使用多端口代理

> 这种方式操作起来最简单！

```nginx
   server {
        listen       8080;
        server_name  localhost;
        location / {
            proxy_pass http://192.168.163.165:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
   }
   server {
        listen       8081;
        server_name  localhost;
        location / {
            proxy_pass http://192.168.163.164:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
   }
   server {
        listen       8082;
        server_name  localhost;
        location / {
            proxy_pass http://192.168.163.163:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
   }
```



## 方案2、使用域名代理

> 这种方式可以只开放一个端口，通过访问域名来进行过滤。
>
> 注：不过现在使用域名需要备案。。。

```nginx
   server {
        listen       8080;
        server_name  a.example.com;
        location / {
            proxy_pass http://192.168.163.165:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
   }
   server {
        listen       8080;
        server_name  a.example.com;
        location / {
            proxy_pass http://192.168.163.164:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
   }
   server {
        listen       8080;
        server_name  a.example.com;
        location / {
            proxy_pass http://192.168.163.163:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
   }
```



## 方案3、使用一个端口+前缀代理（可能存在问题）



### 3.1、前端项目是Vue的hash模式，且前端与后端共用一个地址

```nginx
      location ^~ /a/ {
            rewrite_by_lua_block {
                local x=ngx.shared.sdata
                x:set(ngx.var.cookie_uid,"a")
            }
	  
            proxy_pass http://192.168.200.103:8880/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
```



### 3.2、前端项目是Vue的hash模式，且前端与后端不共用一个地址

```nginx
        location  ^~ /b_serve/ {            
            sub_filter '192.168.163.160:123456/' '$http_host/b_serve/';
            sub_filter_once off;
            subs_filter_types  *;
            proxy_set_header Accept-Encoding "";
	
            proxy_pass http://192.168.200.160:123456/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location  ^~ /b/ {
            sub_filter '192.168.163.160:123456/' '$http_host/b_serve/';
            sub_filter_once off;
            subs_filter_types  *;
            proxy_set_header Accept-Encoding "";
	         
            proxy_pass http://192.168.163.165:9134/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
```



### 3.3、前端项目不是Vue的hash模式，且前端与后端共用一个地址

```nginx
      location ^~ /b/ {
            # 修改响应体信息
            sub_filter '"/'  '"/b/';
            sub_filter "'/"  "'/b/";
            sub_filter_once off;
            sub_filter_types *;
            proxy_set_header Accept-Encoding "";
	  
            proxy_pass http://192.168.163.103:8880/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
```



### 3.4、 前端项目不是Vue的hash模式，且前端与后端不共用一个地址

```nginx
        location  ^~ /b_serve/ {
            sub_filter '192.168.163.160:123456/' '$http_host/b_serve/';
            sub_filter_once off;
            subs_filter_types  *;
            proxy_set_header Accept-Encoding "";
	
            proxy_pass http://192.168.200.160:25846/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location  ^~ /b/ {
            sub_filter '192.168.163.160:123456/' '$http_host/b_serve/';
            sub_filter '"/'  '"/b/';
            sub_filter "'/"  "'/b/";
            sub_filter_once off;
            subs_filter_types  *;
            proxy_set_header Accept-Encoding "";
	         
            proxy_pass http://192.168.200.165:9134/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

```



## 方案3的环境配置

> 当前示例中的部署服务器是Centos。
>
> 以下只是个人配置！！！



### 1、安装DNS服务

> 安装DNS服务，用于nginx进行域解析。



### 2、安装luajit

> 需要nginx使用ngx模块，该模块需要luajit。

#### 2.1 源码编译

```shell
git clone https://github.com/openresty/luajit2

cd luajit2
make && make install
```

#### 2.2 环境配置

```shell
export LUAJIT_LIB=/usr/local/lib
export LUAJIT_INC=/usr/local/include/luajit-2.1
echo "/usr/local/lib" >> /etc/ld.so.conf
ldconfig
```



### 3、安装nginx



#### 3.1 源码编译

```shell
Mkdir -p /data/soft/nginx
cd /data/soft/nginx

wget https://github.com/openresty/lua-nginx-module/archive/v0.10.9rc7.tar.gz
tar -xzvf v0.10.9rc7.tar.gz

wget https://github.com/simpl/ngx_devel_kit/archive/v0.3.0.tar.gz
tar -xzvf v0.3.0.tar.gz

wget http://nginx.org/download/nginx-1.17.5.tar.gz
tar -xzvf nginx-1.17.5.tar.gz

get clone https://github.com/yaoweibin/ngx_http_substitutions_filter_module/

cd /data/soft/nginx/nginx-1.17.5

./configure --prefix=/usr/local/nginx --with-http_ssl_module --with-http_flv_module --with-http_stub_status_module --with-http_gzip_static_module --with-http_realip_module --with-pcre --add-module=/data/soft/nginx/lua-nginx-module-0.10.9rc7 --add-module=/data/soft/nginx/ngx_devel_kit-0.3.0 --with-stream --with-http_sub_module --add-module=/data/soft/nginx/ngx_http_substitutions_filter_module

make && make install 
```



#### 3.2 nginx配置

```nginx
worker_processes  1;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Headers X-Requested-With;
    add_header Access-Control-Allow-Methods GET,POST,OPTIONS;
    
    lua_shared_dict sdata 36m; # 定义计数共享空间

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;
    
    server {
        listen       8899;
        server_name  www.demo.com;
        resolver www.demo.com; # 在DNS服务中自定义的域名
	
        userid         on;  # 用户实例
      	userid_name    uid;
        
		# 前端项目不是Vue的hash模式，且前端与后端共用一个地址
        location ^~ /a/ {
        	# 用于当前用户本次记录系统
            rewrite_by_lua_block {
                local x=ngx.shared.sdata
                x:set(ngx.var.cookie_uid,"a")
            }
			
			# 进行响应体替换，为请求推荐前缀 如果是相对路径可能存在问题
            sub_filter '"/'  '"/a/';
            sub_filter "'/"  "'/a/";
            sub_filter_once off;
            sub_filter_types *;
            proxy_set_header Accept-Encoding "";

	  
            proxy_pass http://192.168.136.103:8880/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # 前端项目不是Vue的hash模式，且前端与后端不共用一个地址
        location  ^~ /b_serve/ {
            rewrite_by_lua_block {
                local x=ngx.shared.sdata
                x:set(ngx.var.cookie_uid,"b_serve")
            }
            
            # 替换响应体的后端地址
            sub_filter '192.168.136.160:123456/' '$http_host/b_serve/';
            sub_filter_once off;
            subs_filter_types  *;
            proxy_set_header Accept-Encoding "";
	
            proxy_pass http://192.168.136.160:123456/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location  ^~ /b/ {
            rewrite_by_lua_block {
                local x=ngx.shared.sdata
                x:set(ngx.var.cookie_uid,"b")
            }

            sub_filter '192.168.136.160:123456/' '$http_host/b_serve/';
            sub_filter_once off;
            subs_filter_types  *;
            proxy_set_header Accept-Encoding "";
	         
            proxy_pass http://192.168.136.165:9134/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

		# 前端项目是Vue的hash模式，且前端与后端共用一个地址
        location  ^~ /c/ {
            rewrite_by_lua_block {
                local x=ngx.shared.sdata
                x:set(ngx.var.cookie_uid,"gjjs")
            }

            proxy_pass http://192.168.136.168:9191/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        
        # 前端项目是Vue的hash模式，且前端与后端不共用一个地址
        location  ^~ /d_serve/ {
            rewrite_by_lua_block {
                local x=ngx.shared.sdata
                x:set(ngx.var.cookie_uid,"d_serve")
            }
            
            sub_filter '192.168.136.160:25846/' '$http_host/d_serve/';
            sub_filter_once off;
            subs_filter_types  *;
            proxy_set_header Accept-Encoding "";
	
            proxy_pass http://192.168.136.160:25846/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location  ^~ /d/ {
            rewrite_by_lua_block {
                local x=ngx.shared.sdata
                x:set(ngx.var.cookie_uid,"d")
            }

            sub_filter '192.168.136.160:25846/' '$http_host/d_serve/';
            sub_filter_once off;
            subs_filter_types  *;
            proxy_set_header Accept-Encoding "";
	         
            proxy_pass http://192.168.136.165:9134/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

		# 全局拦截，避免出现没有替换到场景
        location / {
            set $app '';            
            set_by_lua_block $app {
      	 	       local x=ngx.shared.sdata
      		       return x:get(ngx.var.cookie_uid)
         	}
            
            proxy_pass http://www.demo.com:8899/$app$request_uri;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }


    }

}
```






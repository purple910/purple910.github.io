# iframe 里面引入soanrqube页面



## 直接引用
```
<iframe id="iframe" src="http://192.168.2.102:9000" width="1500" height="1000"></iframe>
```

## 结果加载失败
```
Refused to display 'http://192.168.2.102:9000/' in a frame because it set 'X-Frame-Options' to 'sameorigin'.
```

## 解决方法 
### 使用 ngnix 配置代理，过滤 X-Frame-Options （ngnix.conf）
``` 
server {
        listen       80;
        server_name  localhost;

	location / {
	    proxy_pass http://192.168.2.102:9000;
	    proxy_hide_header X-Frame-Options;
	    add_header Access-Control-Allow-Origin *;
	    add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
	    add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
	
	    add_header X-Frame-Options ALLOWALL;	
	}
}
```

### iframe 引入
```
 <iframe id="iframe" src="http://192.168.1.167" width="1500" height="1000"></iframe>
```
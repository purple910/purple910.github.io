# 公司共享开发资源说明

## 1. maven 仓库

### 地址 
`http://192.168.7.197:8081/`   

### 项目使用
 `此处以gradle为例子`
```groovy
repositories {
    maven { url "http://192.168.7.197:8081/repository/maven-public/" }
    maven { url "http://192.168.7.197:8081/repository/maven-snapshots/" }
}
```

## 2. npm 仓库

### 地址 
`http://192.168.7.197:8081/`   

### 项目使用

1. 将 包管理工具的registry指向私服

```bash
npm config set registry http://192.168.7.197:8081/repository/npm-group/
or
yarn config set registry http://192.168.7.197:8081/repository/npm-group/
```

2. 依赖安装
> 与正常npm或者yarn使用一致
```bash
npm install xxx
or
yarn add xxx
```

## docker 仓库
### 地址
`http://192.168.7.197:8081/`   

### 项目使用
!> 注意： 拉取镜像使用`5000`端口，推送镜像使用`5002`端口
#### 1. docker添加信任仓库地址
```bash 
vi /etc/docker/daemon.json

{
  ...
  "insecure-registries": ["192.168.7.197:5001"，"192.168.7.197:5002"， "192.168.7.197:5000"]
}
```
#### 2. 重启docker
```bash
systemctl daemon-reload && systemctl restart docker
```
#### 3. 发布镜像
1.  登录到docker仓库 
```bash
# 登录
docker login -u admin -p admin123 192.168.7.197:5002
# 推送到私服
docker tag nginx:latest 192.168.7.197:5002/nginx:latest
```
#### 2. 拉取镜像 [支持匿名]
```bash
docker pull 192.168.7.197:5000/nginx:latest
```
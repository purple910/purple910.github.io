# 公司共享开发资源说明
[最新同步地址](http://192.168.9.164/)
## 安装证书
> 由于仓库是以https提供的，使用的自签证书，需要安装证书后才能使用

<!-- select:start -->
<!-- select-menu-labels: 操作系统 -->

#### --centos 7--

下载[证书](http://192.168.9.164/repo.crt)到/etc/pki/ca-trust/source/anchors/repo.crt     
执行update-ca-trust
#### --ubuntu--

下载[证书](http://192.168.9.164/repo.crt)到/usr/local/share/ca-certificates/extra    
执行update-ca-certificates

<!-- select:end -->

## 使用仓库
<!-- select:start -->
<!-- select-menu-labels: 操作系统,可用架构,版本 -->

### --Ubuntu,ARM64,20.04 LTS--

```bash
# 替换/etc/apt/sources.list
deb https://192.168.9.164/ubuntu-ports/ focal main restricted universe multiverse
deb https://192.168.9.164/ubuntu-ports/ focal-updates main restricted universe multiverse
deb https://192.168.9.164/ubuntu-ports/ focal-backports main restricted universe multiverse
deb https://192.168.9.164/ubuntu-ports/ focal-security main restricted universe multiverse
```

### --Ubuntu,ARM64,22.04 LTS--

```bash
# 替换/etc/apt/sources.list
deb https://192.168.9.164/ubuntu-ports/ jammy main restricted universe multiverse
deb https://192.168.9.164/ubuntu-ports/ jammy-updates main restricted universe multiverse
deb https://192.168.9.164/ubuntu-ports/ jammy-backports main restricted universe multiverse
deb https://192.168.9.164/ubuntu-ports/ jammy-security main restricted universe multiverse
```

### --CentOS 7,x86_64,7.9.2009--

```bash
# 替换/etc/yum.repos.d/CentOS-Base.repo
[base]
name=CentOS-$releasever - Base
baseurl=https://192.168.9.164/centos7/os/$basearch/

[updates]
name=CentOS-$releasever - Updates
baseurl=https://192.168.9.164/centos7/updates/$basearch/

[extras]
name=CentOS-$releasever - Extras
baseurl=https://192.168.9.164/centos7/extras/$basearch/

[centosplus]
name=CentOS-$releasever - Plus
baseurl=https://192.168.9.164/centos7/centosplus/$basearch/
enabled=0

# 替换/etc/yum.repos.d/epel.repo
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
baseurl=https://192.168.9.164/centos7/epel/$basearch
enabled=1
```

### --CentOS 7,ARM64,7.9.2009--

```bash
# 替换/etc/yum.repos.d/CentOS-Base.repo
[base]
name=CentOS-$releasever - Base
baseurl=https://192.168.9.164/centos7/os/$basearch/

[updates]
name=CentOS-$releasever - Updates
baseurl=https://192.168.9.164/centos7/updates/$basearch/

[extras]
name=CentOS-$releasever - Extras
baseurl=https://192.168.9.164/centos7/extras/$basearch/

[centosplus]
name=CentOS-$releasever - Plus
baseurl=https://192.168.9.164/centos7/centosplus/$basearch/
enabled=0

# 替换/etc/yum.repos.d/epel.repo
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
baseurl=https://192.168.9.164/centos7/epel/$basearch
enabled=1
```

<!-- select:end -->

## Docker、Kubernetes游乐场
平台架构: ARM64
访问地址: http://192.168.9.55

!> 资源有限，尽量不要开多个会话。资源不足时会随机杀掉一个会话
一个会话限制只能创建两个实例, 每个实例2小时有效期 实在需要的话，可以开多个会话


##  maven 仓库

地址 http://192.168.7.197:8081/

项目使用
```groovy
repositories {
    maven { url "http://192.168.7.197:8081/repository/maven-public/" }
    maven { url "http://192.168.7.197:8081/repository/maven-snapshots/" }
}
```

##  npm 仓库

地址 http://192.168.7.197:8081/

项目使用
```bash
npm config set registry http://192.168.7.197:8081/repository/npm-group/
or
yarn config set registry http://192.168.7.197:8081/repository/npm-group/
npm install xxx
or
yarn add xxx
```
## Docker 仓库

可用架构: x86_64、ARM64  
使用方法: 修改下述文件后, 重启Docker即可
```
# 添加到/etc/hosts文件中
192.168.9.164 k8s.gcr.io
192.168.9.164 registry-1.docker.io
192.168.9.164 192.168.9.164 quay.io
# 添加到/etc/docker/daemon.json文件中, 没有的话创建
{
    "registry-mirrors": [
        "https://192.168.9.164"
    ]
}
```
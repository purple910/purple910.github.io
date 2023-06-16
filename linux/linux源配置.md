# linux源配置


## CentOS-7
```
[aliyun-base]
name=CentOS-7 - Base - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/7/os/$basearch/
        http://mirrors.aliyuncs.com/centos/7/os/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/7/os/$basearch/
gpgcheck=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#released updates 
[aliyun-updates]
name=CentOS-7 - Updates - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/7/updates/$basearch/
        http://mirrors.aliyuncs.com/centos/7/updates/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/7/updates/$basearch/
gpgcheck=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#additional packages that may be useful
[aliyun-extras]
name=CentOS-7 - Extras - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/7/extras/$basearch/
        http://mirrors.aliyuncs.com/centos/7/extras/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/7/extras/$basearch/
gpgcheck=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#additional packages that extend functionality of existing packages
[aliyun-centosplus]
name=CentOS-7 - Plus - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/7/centosplus/$basearch/
        http://mirrors.aliyuncs.com/centos/7/centosplus/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/7/centosplus/$basearch/
gpgcheck=0
enabled=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#contrib - packages by Centos Users
[aliyun-contrib]
name=CentOS-7 - Contrib - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/7/contrib/$basearch/
        http://mirrors.aliyuncs.com/centos/7/contrib/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/7/contrib/$basearch/
gpgcheck=0
enabled=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7


[tuna-base] 
name=CentOS-7 - Base 
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/7/os/$basearch/ 
#mirrorlist=http://mirrorlist.centos.org/?release=7&arch=$basearch&repo=os 
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7

#released updates 
[tuna-updates] 
name=CentOS-7 - Updates 
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/7/updates/$basearch/ 
#mirrorlist=http://mirrorlist.centos.org/?release=7&arch=$basearch&repo=updates 
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7 

#additional packages that may be useful 
[tuna-extras] 
name=CentOS-7 - Extras 
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/7/extras/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=7&arch=$basearch&repo=extras 
gpgcheck= 0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7 

#additional packages that extend functionality of existing packages 
[tuna-centosplus] 
name=CentOS-7 - Plus 
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/7/centosplus/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=7&arch=$basearch&repo=centosplus 
gpgcheck=0
enabled=0 
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7

[mirrors.163.com.repo]
name=mirrors.163.com.repo
baseurl=http://mirrors.163.com/centos/7/os/x86_64/
enabled=1
gpgcheck=0
gpgkey=http://mirrors.163.com/centos/7/os/x86_64/RPM-GPG-KEY-CentOS-7s

```

## CentOS-8
```
[rhel-8-baseos-beta-source-rpms]
name = Red Hat Enterprise Linux 8 - BaseOS Beta (Source RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/baseos/source/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-for-x86_64-baseos-beta-rpms]
name = Red Hat Enterprise Linux 8 for x86_64 - BaseOS Beta (RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/baseos/x86_64/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-appstream-beta-source-rpms]
name = Red Hat Enterprise Linux 8 - AppStream Beta (Source RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/appstream/source/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-for-x86_64-appstream-beta-rpms]
name = Red Hat Enterprise Linux 8 for x86_64 - AppStream Beta (RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/appstream/x86_64/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-ha-beta-source-rpms]
name = Red Hat Enterprise Linux 8 - HighAvailability Beta (Source RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/add-ons/ha/source/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-for-x86_64-ha-beta-rpms]
name = Red Hat Enterprise Linux 8 for x86_64 - HighAvailability Beta (RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/add-ons/ha/x86_64/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-rs-beta-source-rpms]
name = Red Hat Enterprise Linux 8 - ResilientStorage Beta (Source RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/add-ons/rs/source/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-for-x86_64-rs-beta-rpms]
name = Red Hat Enterprise Linux 8 for x86_64 - ResilientStorage Beta (RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/add-ons/rs/x86_64/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-rt-beta-source-rpms]
name = Red Hat Enterprise Linux 8 - RT Beta (Source RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/add-ons/rt/source/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhel-8-for-x86_64-rt-beta-rpms]
name = Red Hat Enterprise Linux 8 for x86_64 - RT Beta (RPMs)
baseurl = https://downloads.redhat.com/redhat/rhel/rhel-8-beta/add-ons/rt/x86_64/
enabled = 0
gpgcheck = 1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

```

## debian
```
Linux swx-PC-master 4.19.0-arm64-desktop #1637 SMP Mon Jan 13 15:03:45 CST 2020 aarch64 GNU/Linux
root@swx-PC-master:~# cat /etc/apt/sources.list
## Generated by deepin-installer
deb [by-hash=force] https://packages.chinauos.cn/uos eagle main contrib non-free
deb-src https://packages.chinauos.cn/uos eagle main contrib non-free

deb http://mirrors.aliyun.com/deepin/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/deepin/ bionic main restricted universe multiverse

deb http://mirrors.aliyun.com/deepin/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/deepin/ bionic-security main restricted universe multiverse

deb http://mirrors.aliyun.com/deepin/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/deepin/ bionic-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/deepin/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/deepin/ bionic-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/deepin/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/deepin/ bionic-backports main restricted universe multiverse

deb [by-hash=force] https://mirrors.aliyun.com/deepin/ apricot main contrib non-free
deb [by-hash=force] https://mirrors.tuna.tsinghua.edu.cn/deepin/ apricot main contrib non-free

deb http://mirrors.163.com/debian/ stretch main non-free contrib
deb http://mirrors.163.com/debian/ stretch-updates main non-free contrib
deb http://mirrors.163.com/debian/ stretch-backports main non-free contrib
deb-src http://mirrors.163.com/debian/ stretch main non-free contrib
deb-src http://mirrors.163.com/debian/ stretch-updates main non-free contrib
deb-src http://mirrors.163.com/debian/ stretch-backports main non-free contrib
deb http://mirrors.163.com/debian-security/ stretch/updates main non-free contrib
deb-src http://mirrors.163.com/debian-security/ stretch/updates main non-free contrib

```

# gpasswd
```
1、gpasswd命令是Linux下工作组文件/etc/group和/etc/gshadow的管理工具，用于指定要管理的工作组。
2、选项详解：
      -a : 添加用户到组
      -d : 从组删除用户
      -A：指定管理员
      -M：指定组成员和-A的用途差不多；
      -r：删除密码；
      -R：限制用户登入组，只有组中的成员才可以用newgrp加入该组。
3、实例：
    将userA添加到groupB用户组里面：  
        passwd -a userA groupB
注意：
    添加用户到某一个组可以使用  usermod -G groupB userA 这个命令可以添加一个用户到指定的组，但是以前添加的组就会清空掉。
    所以想要添加一个用户到一个组，同时保留以前添加的组时，请使用gpasswd这个命令来添加操作用户。
```

# acl
```
1、查看是否支持acl
dumpe2fs -h /dev/sda3
2、开启acl支持
mount -o remount, acl [mount point]
3、类型
user::rw-       定义了ACL_USER_OBJ, 说明file owner拥有read and write permission
user:john:rw-   定义了ACL_USER,这样用户john就拥有了对文件的读写权限,实现了我们一开始要达到的目的
group::rw-      定义了ACL_GROUP_OBJ,说明文件的group拥有read and write permission
group:dev:r--   定义了ACL_GROUP,使得dev组拥有了对文件的read permission
mask::rw-       定义了ACL_MASK的权限为read and write
other::r--      定义了ACL_OTHER的权限为read
```

# setfacl
```
1、chmod命令可以把文件权限分为u,g,o三个组,而setfacl可以对每一个文件或目录设置更精确的文件权限。
换句话说，setfacl可以更精确的控制权限的分配。
ACL可以针对单一用户、单一文件或目录来进行r,w,x的权限控制
2、选项详解
-m,       --modify-acl 更改文件的访问控制列表
-M,       --modify-file=file 从文件读取访问控制列表条目更改
-x,       --remove=acl 根据文件中访问控制列表移除条目
-X,       --remove-file=file 从文件读取访问控制列表条目并删除
-b,       --remove-all 删除所有扩展访问控制列表条目
-k,       --remove-default 移除默认访问控制列表
          --set=acl 设定替换当前的文件访问控制列表
          --set-file=file 从文件中读取访问控制列表条目设定
          --mask 重新计算有效权限掩码
-n,       --no-mask 不重新计算有效权限掩码
-d,       --default 应用到默认访问控制列表的操作
-R,       --recursive 递归操作子目录
-L,       --logical 依照系统逻辑，跟随符号链接
-P,       --physical 依照自然逻辑，不跟随符号链接
          --restore=file 恢复访问控制列表，和“getfacl -R”作用相反
          --test 测试模式，并不真正修改访问控制列表属性
3、实例
setfacl -m u:tank:rx test   #给tank用户向test文件增加读和执行的acl规则
setfacl -m u::rwx test   #设置默认用户，读，写，可执行
setfacl -m d:u:tank:r-x text    #设置tank用户的默认权限r-x
setfacl -b test     #清除所有acl
setfacl -x u:tank test    #清除tank用户，对test文件acl规则
```

# getfacl
``` 
getfacl acl_test1 
# file: acl_test1    <==说明档名而已！
# owner: root        <==说明此档案的拥有者，亦即ls -l看到的第三使用者栏位 
# group: root        <==此档案的所属群组，亦即ls -l看到的第四群组栏位 
user::rwx            <==使用者列表栏是空的，代表档案拥有者的权限
user:vbird1:rx      <==针对vbird1的权限设定为rx ，与拥有者并不同！
group::r--           <==针对档案群组的权限设定仅有r 
mask::rx            <==此档案预设的有效权限(mask) 
other::r--           <==其他人拥有的权限啰！
```


# rpm
```
rpm -ivh package.rpm 
安装一个rpm包 
rpm -ivh --nodeeps package.rpm 
安装一个rpm包而忽略依赖关系警告 
rpm -U package.rpm 
更新一个rpm包但不改变其配置文件 
rpm -F package.rpm 
更新一个确定已经安装的rpm包 
rpm -e package_name.rpm 
删除一个rpm包 
rpm -qa 
显示系统中所有已经安装的rpm包 
rpm -qa | grep httpd 
显示所有名称中包含 "httpd" 字样的rpm包 
rpm -qi package_name 
获取一个已安装包的特殊信息 
rpm -qg "System Environment/Daemons" 
显示一个组件的rpm包 
rpm -ql package_name 
显示一个已经安装的rpm包提供的文件列表 
rpm -qc package_name 
显示一个已经安装的rpm包提供的配置文件列表 
rpm -q package_name --whatrequires 
显示与一个rpm包存在依赖关系的列表 
rpm -q package_name --whatprovides 
显示一个rpm包所占的体积 
rpm -q package_name --scripts 
显示在安装/删除期间所执行的脚本l 
rpm -q package_name --changelog 
显示一个rpm包的修改历史 
rpm -qf /etc/httpd/conf/httpd.conf 
确认所给的文件由哪个rpm包所提供 
rpm -qp package.rpm -l 
显示由一个尚未安装的rpm包提供的文件列表 
rpm --import /media/cdrom/RPM-GPG-KEY 
导入公钥数字证书 
rpm --checksig package.rpm 
确认一个rpm包的完整性 
rpm -qa gpg-pubkey 
确认已安装的所有rpm包的完整性 
rpm -V package_name 
检查文件尺寸、 许可、类型、所有者、群组、MD5检查以及最后修改时间 
rpm -Va 
检查系统中所有已安装的rpm包- 小心使用 
rpm -Vp package.rpm 
确认一个rpm包还未安装 
rpm2cpio package.rpm | cpio --extract --make-directories *bin* 
从一个rpm包运行可执行文件 
rpm -ivh /usr/src/redhat/RPMS/`arch`/package.rpm 
从一个rpm源码安装一个构建好的包 
rpmbuild --rebuild package_name.src.rpm 
从一个rpm源码构建一个 rpm 包 
```


# sed
```
sed 's/stringa1/stringa2/g' example.txt 
将example.txt文件中的 "string1" 替换成 "string2" 
sed '/^$/d' example.txt 
从example.txt文件中删除所有空白行 
sed '/ *#/d; /^$/d' example.txt 
从example.txt文件中删除所有注释和空白行 
echo 'esempio' | tr '[:lower:]' '[:upper:]' 
合并上下单元格内容 
sed -e '1d' result.txt 
从文件example.txt 中排除第一行 
sed -n '/stringa1/p' 
查看只包含词汇 "string1"的行 
sed -e 's/ *$//' example.txt 
删除每一行最后的空白字符 
sed -e 's/stringa1//g' example.txt 
从文档中只删除词汇 "string1" 并保留剩余全部 
sed -n '1,5p;5q' example.txt 
查看从第一行到第5行内容 
sed -n '5p;5q' example.txt 
查看第5行 
sed -e 's/00*/0/g' example.txt 
用单个零替换多个零 
```



# 字符设置和文件格式转换 
```
dos2unix filedos.txt fileunix.txt 将一个文本文件的格式从MSDOS转换成UNIX 
unix2dos fileunix.txt filedos.txt 将一个文本文件的格式从UNIX转换成MSDOS 
recode ..HTML < page.txt > page.html 将一个文本文件转换成html 
recode -l | more 显示所有允许的转换格式 
```



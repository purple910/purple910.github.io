# maven的配置



## 下载maven
```
https://maven.apache.org/download.cgi
```

## 配置环境变量
```
1 创建系统变量名 M2_HOME 变量值 D:\Apache\apache-maven-3.6.3
2 在path里添加变量 %M2_HOME%\bin
3 在cmd里输入mvn -v,测试环境是否配好
```

## 创建本地仓库地址
我自己的是在D:\Apache\apache-maven-3.6.3\repository

## 配置settings.xml (D:\Apache\apache-maven-3.6.3\conf\settings.xml)
1 配置本地仓库地址
```
<localRepository>D:\Apache\apache-maven-3.6.3\repository</localRepository>
```
2 配置远程仓库地址
```
<mirror>
    <id>alimaven</id>
    <name>aliyun maven</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    <mirrorOf>*</mirrorOf>
</mirror>
<mirror>
    <id>alimaven</id>
    <mirrorOf>*</mirrorOf>
    <url>https://maven.aliyun.com/repository/central</url>
</mirror>
<mirror>
    <id>alimaven</id>
    <mirrorOf>central</mirrorOf>
    <name>aliyun maven</name>
    <url>http://maven.aliyun.com/nexus/content/repositories/central/</url>
</mirror>
<mirror>
    <id>alimaven</id>
    <name>aliyun maven</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    <mirrorOf>central</mirrorOf>
</mirror>
<mirror>
    <id>central</id>
    <name>Maven Repository Switchboard</name>
    <url>http://repo1.maven.org/maven2/</url>
    <mirrorOf>central</mirrorOf>
</mirror>
<mirror>
    <id>repo2</id>
    <mirrorOf>central</mirrorOf>
    <name>Human Readable Name for this Mirror.</name>
    <url>http://repo2.maven.org/maven2/</url>
</mirror>
<mirror>
    <id>ibiblio</id>
    <mirrorOf>central</mirrorOf>
    <name>Human Readable Name for this Mirror.</name>
    <url>http://mirrors.ibiblio.org/pub/mirrors/maven2/</url>
</mirror>
<mirror>
    <id>jboss-public-repository-group</id>
    <mirrorOf>central</mirrorOf>
    <name>JBoss Public Repository Group</name>
    <url>http://repository.jboss.org/nexus/content/groups/public</url>
</mirror>
<mirror>
    <id>google-maven-central</id>
    <name>Google Maven Central</name>
    <url>https://maven-central.storage.googleapis.com</url>
    <mirrorOf>central</mirrorOf>
</mirror>
<!-- 中央仓库在中国的镜像 -->
<mirror>
    <id>maven.net.cn</id>
    <name>oneof the central mirrors in china</name>
    <url>http://maven.net.cn/content/groups/public/</url>
    <mirrorOf>central</mirrorOf>
</mirror>
```
3 配置代理
```
<proxy>
    <id>optional</id>
    <active>true</active>
    <protocol>http</protocol>
    <host>地址</host>
    <port>端口</port>
    <nonProxyHosts>D:\Apache\apache-maven-3.6.3\repository(本地仓库地址|不用代理的地址)</nonProxyHosts>
</proxy>
```

## 将jar打包到本地仓库里
```
mvn install:install-file -DgroupId=com.oracle -DartifactId=ojdbc6 -Dversion=11.2.0.1.0 -Dfile=ojdbc6-11.2.0.1.0.jar -Dpackaging=jar
```

## 在pom.xml去除依赖
去除spring的默认日志
1
![](https://img2020.cnblogs.com/blog/1863149/202012/1863149-20201214142507012-1564440630.png)
2 
![](https://img2020.cnblogs.com/blog/1863149/202012/1863149-20201214142733552-1786516365.png)
![](https://img2020.cnblogs.com/blog/1863149/202012/1863149-20201214142751139-1962559726.png)
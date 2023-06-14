# gradle的配置

## 下载gradle
```
https://gradle.org/releases/
```

## 配置环境变量
```
1 添加系统变量
GRADLE_HOME D:\Apache\gradle-6.7.1
GRADLE_USER_HOME D:\Apache\apache-maven-3.6.3\repository(可以是本地maven仓库地址,也可以不是)
```
2 添加path
```
%GRADLE_HOME%\bin
```
3 运行cmd输入gradle -v,测试环境是否配好

## 在idea配置gradle
![](https://img2020.cnblogs.com/blog/1863149/202012/1863149-20201214141755505-684471417.png)

## build.gradle的基本配置
1 配置仓库
```
repositories {
    mavenLocal()    // 本地仓库
    maven { url 'http://maven.aliyun.com/nexus/content/groups/public/' }    // 阿里云仓库
    mavenCentral()  // 中心仓库
}
```
2 去除jar里的依赖
![](https://img2020.cnblogs.com/blog/1863149/202012/1863149-20201214143814806-1406660921.png)

### 我的错误
![](https://img2020.cnblogs.com/blog/1863149/202012/1863149-20201214143943427-2025396765.png)
### 我的解决方法
![](https://img2020.cnblogs.com/blog/1863149/202012/1863149-20201214144038076-1040494977.png)
注: 我自己是在内网,所以要配代理去外网. 我之前用自动代理不行,后来换成手动代理,就可以了

### 我的错误
![](https://img2020.cnblogs.com/blog/1863149/202012/1863149-20201214144502964-1701430913.png)
### 我的解决方法
1 更改gradle的版本
2 更改gradle使用本地的gradle
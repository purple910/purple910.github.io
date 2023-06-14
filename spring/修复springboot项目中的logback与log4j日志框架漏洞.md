# 修复spring boot项目中的logback与log4j日志框架漏洞



## 依赖版本使用顺序
遍历所有依赖库来指定依赖库版本 > 手动指定依赖库版本 > 全局配置依赖库版本 > 包管理工具中依赖可以版本 > 自定义jar中依赖库版本

## 解决方案
### 方案1.手动引入其依赖并设置其版本号
```
implementation group: 'ch.qos.logback', name: 'logback-classic', version: '1.2.10'
implementation group: 'ch.qos.logback', name: 'logback-core', version: '1.2.10'
implementation group: 'org.apache.logging.log4j', name: 'log4j-api', version: '2.17.1'
implementation group: 'org.apache.logging.log4j', name: 'log4j-core', version: '2.17.1'
```

### 方案2.配置全局的依赖版本号，需要在每个项目中的主配置文件添加（推荐）
```
ext['logback.version']='1.2.10'
ext['log4j2.version']='2.17.1'
```

### 方案3. 升级包管理工具
```
classpath 'org.springframework.boot:spring-boot-gradle-plugin:2.6.3'
```

### 方案4.不使用包管理工具，并在基础框架中升级依赖版本号

### 方案5遍历所有依赖库，通过判断 requested.group 和 requested.name 来指定使用的版本（推荐）
```
subprojects {
    project.configurations.all {
        resolutionStrategy.eachDependency { DependencyResolveDetails details ->
            def requested = details.requested
            if (requested.group == 'org.apache.logging.log4j') {
                details.useVersion '2.17.0'
            }
            if (requested.group == 'ch.qos.logback') {
                details.useVersion '1.2.10'
            }
        }
    }
}
```
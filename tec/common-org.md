# 组织机构使用手册



## 前言

由于在检察业务项目中，组织机构，用户权限，功能组件，日志管理，数据字典等的模块，基本上都是一样的。所以我们将这些模块提取出来做出一个通用模块，可以减少项目组的开发成本，提高开发效率。





## 1. 组织机构引入说明



> 依赖引入

```groovy
implementation 'com.tfswx:zzjg:0.5.13-proj'
```



## 2. 组织机构配置说明

```properties
# 服务端口
server.port=8888
spring.application.name=zzjg-serve


# dm数据库
spring.datasource.driver-class-name=
spring.datasource.url=
spring.datasource.username=
spring.datasource.password=
mybatis.mapper-locations=classpath*:mapper/*.xml,classpath*:mapper/tyyw/*.xml
mybatis.configuration.shrink-whitespaces-in-sql=true


# swagger配置
application.swagger.title=你们好
application.swagger.group-name=组织机构
application.swagger.description=组织机构的接口
knife4j.setting.enableDynamicParameter=true


# 系统配置
application.platform=custom
application.datasource.list=default,tyyw
application.tls.enabled=false
logging.level.com.zaxxer.hikari=debug
spring.main.allow-bean-definition-overriding=true


#日志定时删除 每日00:00:00清除
rz-task=00 00 00 * * ?
# 日志物理删除(月)
rz-disk-rm=9
# 日志逻辑删除(月)
rz-logic-rm=6


# 登录失败锁定时间1h
login-locking=3600000
# redis地址
spring.redis.host=192.168.1.117
# token秘钥
application.authorize.secret=123456
# token有效期
application.authorize.timeout=386400000
spring.resources.static-locations=classpath:/META-INF/resources/,classpath:/resources/,classpath:/static/,classpath:/public/


## 文件存储
storage.service-type=LOCALHOST
storage.tmpFileCleanTime=24
storage.temDirectory=/opt/zlpc/temp
storage.directory=/opt/zlpc/file


# 同步统一业务组织机构的版本
synchronize.version=2.0
synchronize.encryption=true
# 同步数据的服务器地址2.0
synchronize.ip=http://192.168.2.227:8088
# 同步数据的服务器地址1.5
spring.datasource.tyyw.driver-class-name=oracle.jdbc.driver.OracleDriver
spring.datasource.tyyw.url=jdbc:oracle:thin:@192.168.1.197:1521/sd.net
spring.datasource.tyyw.username=tyyw
spring.datasource.tyyw.password=tyyw
# 定时确认工作任务 每天23:50:00
synchronize-task=00 00 23 ? * 5
# 同步单位部门
synchronize-dwbm=100000
synchronize-dwmc=高检
# 是否同步密码
synchronize-pwd=true


# 初始化密码
init-user-pwd=ACB60BFA502A4F271D9B592B22D1BEFF1368C8FADF3476FEEFC1FE3B6DB9A71D
# 是否允许密码为空
init-user-empty=true
# 初始化用户权限
init-user-gn=
# 初始化组件权限
init-user-zj=


# 是否进行验证码校验
login-captchaOnOff=false
# 验证码类型 math 数组计算 char 字符验证
login-captchaType=char
```



## 3. 日志模板配置

### 3.1 创建czrz.properties

> 可以自定义日志模板，不过需要以`log-`开头

```properties
# 标准格式
log-update=用户[{}]修改{},请求方法:{},操作url:{},操作参数:{}
log-add=   用户[{}]添加{},请求方法:{},操作url:{},操作参数:{}
log-delete=用户[{}]删除{},请求方法:{},操作url:{},操作参数:{}
# 自定义格式
log-组织机构数据同步=单位{dwbm}同步数据
log-搭建=搭建方案
log-结束=结束
```



### 3.2 日志接口使用

```java
    /**
     *
     * @param logModel 日志模板
     * @param operModel 日志分类
     * @param operDBTables 操作表
     * @param requestParam 入参
     */
    public static void info(String logModel, String operModel, String operDBTables, Object requestParam) 
    // LogUtil.info("log-delete", "组件定义-复制", "T_QX_XT_JSZJPZ, T_QX_XT_RYZJPZ", inputDTO);
        
        
    /**
     * 
     * @param logModel 日志模板 
     * @param operModel 日志分类
     * @param operDBTables 操作表
     * @param glzybh 关联资源编号（主键）
     * @param requestParam 入参
     */
    public static void info(String logModel, String operModel, String operDBTables, String glzybh, Object requestParam)
	// LogUtil.info("log-add", "人员管理", "T_ZZJG_XT_RYBM, T_ZZJG_XT_RYJSFP", user.getRybm(), inputDTO);
        
    /**
     *
     * @param logModel 日志模板
     * @param operModel 日志分类
     * @param operDBTables 操作表
     * @param glzybh 关联资源编号（主键）
     * @param requestParam 入参
     * @param remark 备注
     * @param isCustom  是否用入参中参数替换日志模板中的参数(日志模板中参数名要与入参中需要替换的参数名一样)
     */
    @SneakyThrows
    public static void info(String logModel, String operModel, String operDBTables, String glzybh, Object requestParam, String remark, Boolean isCustom)
    LogUtil.info("log-组织机构数据同步", "手动进行组织机构数据同步", "T_ZZJG_XT_RYBM, T_ZZJG_XT_BMBM, T_ZZJG_XT_RYBM, T_ZZJG_XT_DWBM, T_ZZJG_XT_JSBM, T_ZZJG_XT_RYJSFP", inputDTO.getDwbm(), inputDTO, "", true);

```



## 4.登录回调

> 1. 继承LoginCallbackService
> 2. 实现callback(RybmLoginOutputDTO outputDTO)方法
> 3. 自定义登录回调操作



## 5.组织机构使用简解

### 5.1 功能数据准备

> 在数据中运行`组织机构数据准备.SQL`，初始化组织机构表结构

### 5.2 初始化组织机构

> 运行项目，在swagger中执行/zzjg/dwbm/initZzjg接口，同步统一业务的组织机构数据（默认为每个单位创建一个`超级管理员`用户，2.0的密码为`Abc12345`，1.5的密码为`11111111`）

### 5.3 用户登录

> 使用超级管理员登录系统

### 5.4 功能组件的添加

> 进入功能管理页面，添加功能与组件

> > **注：添加功能时，需要注意使用范围的选择（选择省院，则省院才能做用户权限界面看见该功能；选择市院，则市院才能做用户权限界面看见该功能；选择基层院，则基层院才能做用户权限界面看见该功能）；当前单位只能在功能管理页面看见本单位添加的功能，可以看见所有的功能分类**。



### 5.5 组织机构的添加

> 进入组织机构页面，可以添加部门，角色，人员信息



### 5.6 用户权限的操作

> 进入用户权限页面，对用户或者角色添加功能权限或者组件权限

> > **注：如果发现某个功能在添加功能权限时没有显示出来，请优化查看该功能是否当前院适用**



### 5.7 数据字典

>进入数据字典页面，可以配置项目中通过的数据，方便统一管理
































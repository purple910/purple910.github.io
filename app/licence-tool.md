

# 统一授权管理平台



## 前言

​       因公司打造产品越来越多，对于各种形态的产品均需做相应的授权管理，以达到统一授权标准，统一授权方式，统一授权管理的目的。并且鉴于我司的产品主要是离线使用，无法使用在线更新、在线授权校验等手段，因此必须保证本平台生成的离线授权码易于输入、分发，并且无法被轻易破解篡改，本平台在此背景下应运而生。

​        为满足公司各个部门在软件授权方面的技术需求，同时也为了节省项目的开发成本，公司现有的技术储备已经有能力开发出达到业内其他厂商提供的软件授权产品的各种技术指标。

​        本平台会提供了统一授权管理平台与软件授权开发包。统一授权管理平台支持授权产品类型管理、授权产品管理、以及授权信息管理。软件授权开发包则提供了机器码生成与授权校验等功能。



## 1.依赖引入

```groovy
// 统一授权包（机器码生成，授权校验，授权证书生成，授权证书安装，授权证书校验）
implementation 'com.tfswx.license-platform:machine-id-generator:1.6'
```

>**注：由于在国产化服务器上出现过内存大小的跳动，从而导致先前授权的授权码失效问题。需要将授权包升级到1.6版本**

在1.6版本以前的服务端机器码组成：CPUID,CPU核数,内存大小,磁盘序列号,物理地址,串口序列号
在1.6版本后的服务端机器码组成：CPUID,CPU核数、主板序列号、系统的UUID




## 2.机器码

### 2.1 机器码组成

> CPUID,CPU核数、主板序列号、系统的UUID



### 2.2 生成机器码

```java
/**
 * 客户端生成机器码：机器码参数包含CPUID,CPU核数
 * @return
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String machineId = com.tfswx.license.platform.GeneratorUtil.generatorMachineIdClient();


/**
 * 服务端生成机器码：机器码参数包含CPUID,CPU核数,内存大小,磁盘序列号,物理地址,串口序列号
 * @return
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String machineId = com.tfswx.license.platform.GeneratorUtil.generatorMachineIdServer();

```



## 3. 授权生成方式

### 3.1 统一授权管理平台

> [同方统一授权管理平台](http://192.168.9.90:8080/#/login)
>
> 用户密码：admin/tf888888



### 3.2 授权码（紧急情况使用）

```java
/**
 * 生成授权码
 * @param machineId 机器码
 * @param licenseEndDate 有效期（2022-12-12）
 * @return 授权码
 * @throws RuntimeException
 */
String license = com.tfswx.license.platform.GeneratorUtil.generator(String machineId, String licenseEndDate);
```



### 3.3 授权证书（紧急情况使用）

```java
/**
 * 生成证书
 * @param queryResult 扩展参数
 * @param licensePath 授权证书地址
 * @return
 */
com.tfswx.license.platform.createCert(LicenseQueryResult queryResult, String licensePath);
```



## 4. 校验方式 

### 4.1 校验授权码

```java
/**
 * 校验客户端授权码
 * @param rawLicense 授权码
 * @return 有效期（2022-03-06）
 * @throws LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String endDate = com.tfswx.license.platform.LicenseUtil.getLicenseEndDateClient(String rawLicense);


/**
 * 校验服务端授权码
 * @param rawLicense 授权码
 * @return 有效期（2022-03-06）
 * @throws LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String endDate = com.tfswx.license.platform.LicenseUtil.getLicenseEndDateServer(String rawLicense);

```



### 4.2 校验单授权证书

> **注：在项目中只会有一个授权证书**

#### 4.2.1 安装授权证书

```java
/**
 * 安装授权证书
 * @param licensePath 授权证书地址
 * @return 是否安装成功
 */
Boolean state = com.tfswx.license.platform.installCert(String licensePath);
```



#### 4.2.2 校验授权证书

```java
/**
 * 校验客户端授权证书有效期与授权码的有效期
 * @return 是否有效
 * @throws LicenseUtil.LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
Boolean state = com.tfswx.license.platform.verifyCertLicenseClient();

/**
 * 校验服务端授权证书有效期与授权码的有效期
 * @return 是否有效
 * @throws LicenseUtil.LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
Boolean state = com.tfswx.license.platform.verifyCertLicenseServer();
```



### 4.3 校验多授权证书

> **注：在项目中存在多个授权证书，例如不同的单位，它的授权信息不一样。**

#### 4.3.1 安装授权证书

```java
/**
 * 安装授权证书
 * @param licensePath 授权证书地址
 * @param key 当前证书唯一标识(也可以用licensePath作为唯一标识)
 * @return 是否安装成功
 */
Boolean state = com.tfswx.license.platform.installCert(String licensePath, String key);
```



#### 4.3.2 校验授权证书

```java
/**
 * 校验客户端授权证书有效期与授权码的有效期
 * @param key 当前证书唯一标识
 * @return 是否有效
 * @throws LicenseUtil.LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
Boolean state = com.tfswx.license.platform.verifyCertLicenseClient(String key);

/**
 * 校验服务端授权证书有效期与授权码的有效期
 * @param key 当前证书唯一标识
 * @return 是否有效
 * @throws LicenseUtil.LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
Boolean state = com.tfswx.license.platform.verifyCertLicenseServer(String key);
```



## 5. 数据提取

> **注：如果直接提取授权证书的扩展信息，并没有自动校验授权证书中授权码是否可用，需要手动校验！**

### 5.1 获取授权码中的数据

```java
/**
 * 获取授权码有效期
 * @param rawLicense 授权码
 * @return 有效期（2022-03-06）
 * @throws LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String endDate = com.tfswx.license.platform.LicenseUtil.getLicenseEndDateClient(String rawLicense);


/**
 * 校验服务端授权码
 * @param rawLicense 授权码
 * @return 有效期（2022-03-06）
 * @throws LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String endDate = com.tfswx.license.platform.LicenseUtil.getLicenseEndDateServer(String rawLicense);

```



### 5.2 获取单授权证书中数据

```java
/**
 * 获取客户端授权码证书中授权码的有效期
 * @return 有效期（2022-05-26）
 * @throws LicenseUtil.LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String endDate = com.tfswx.license.platform.verifyCertLicenseClientEndDate()

/**
 * 获取服务端授权码证书中授权码的有效期
 * @return 有效期（2022-05-26）
 * @throws LicenseUtil.LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String endDate = com.tfswx.license.platform.verifyCertLicenseServerEndDate()


/**
 * 获取授权码证书中授权次数
 * @return 授权次数
 */
Integer number = com.tfswx.license.platform.getVerifyCertNumber()

/**
 * 获取证书中扩展数据
 * @return LicenseQueryResult
 */
LicenseQueryResult result = com.tfswx.license.platform.getVerifyCertData()

/**
 * 获取证书中授权单位列表
 * @return list
 */
List<Unit> list = com.tfswx.license.platform.getVerifyCertUnit()
```



### 5.3 获取多授权证书中数据

```java
/**
 * 获取客户端授权码证书中授权码的有效期
 * @param key 当前证书唯一标识
 * @return 有效期（2022-05-26）
 * @throws LicenseUtil.LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String endDate = com.tfswx.license.platform.verifyCertLicenseClientEndDate(String key)

/**
 * 获取服务端授权码证书中授权码的有效期
 * @param key 当前证书唯一标识
 * @return 有效期（2022-05-26）
 * @throws LicenseUtil.LicenseException
 * @throws IOException
 * @throws NoSuchAlgorithmException
 */
String endDate = com.tfswx.license.platform.verifyCertLicenseServerEndDate(String key)


/**
 * 获取授权码证书中授权次数
 * @param key 当前证书唯一标识
 * @return 授权次数
 */
Integer number = com.tfswx.license.platform.getVerifyCertNumber(String key)

/**
 * 获取证书中扩展数据
 * @param key 当前证书唯一标识
 * @return LicenseQueryResult
 */
LicenseQueryResult result = com.tfswx.license.platform.getVerifyCertData(String key)

/**
 * 获取证书中授权单位列表
 * @param key 当前证书唯一标识
 * @return list
 */
List<Unit> list = com.tfswx.license.platform.getVerifyCertUnit(String key)
```



### 5.4 直接通过证书获取证书中的数据

```java
/**
 * 获取证书中数据
 *
 * @param licensePath 证书路径
 * @return
 */
LicenseQueryResult result = com.tfswx.license.platform.CertUtil.getCertData(String licensePath);

/**
 * 获取证书中数据
 *
 * @param licenseFile 证书
 * @return
 */
LicenseQueryResult result = com.tfswx.license.platform.CertUtil.getCertData(File licenseFile);
```



## 6. springboot项目中使用单授权证书（示例）

### 6.1 授权证书路径配置

```properties
license.licensePath=license.lic
```



### 6.2 在项目启动时安装单证书

```java
/**
 * 在项目启动时安装证书,避免服务重启后需要在次手动安装证书
 *
 * @author administer
 */
@Component
public class LicenseCheckListener implements ApplicationListener<ContextRefreshedEvent> {

    /**
     * 证书生成路径
     */
    @Value("${license.licensePath}")
    private String licensePath;

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        ApplicationContext context = event.getApplicationContext().getParent();
        if (context == null) {
            if (new File(licensePath).exists()) {
                CertUtil.installCert(licensePath);
            }
        }
    }
}
```



### 6.3 拦截器校验证书是否合法

```java
/**
 * 拦截器校验证书是否合法
 * 当前示例只是校验了授权证书中授权码是否有效，如果需要控制到授权单位，则需要手动实现
 * @author administer
 */
@Component
public class LicenseCheckInterceptor extends HandlerInterceptorAdapter {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 校验证书是否有效
        boolean verifyResult = CertUtil.verifyCertLicense();
        if (verifyResult) {
            return true;
        } else {
            throw new RuntimeException("您的证书无效，请核查服务器是否取得授权或重新申请证书！");
        }
    }

}
```



### 6.4 添加安装授权证书接口与获取授权证书信息接口

```java
@RestController("/")
public class CertController {

    @Value("${license.licensePath}")
    private String licensePath;

    @ApiOperation(value = "安装授权证书")
    @PostMapping("install")
    public Boolean install(MultipartFile file) {
        try {
            // 文件记录
            if (file != null) {
                file.transferTo(Paths.get(licensePath));
                Boolean cert = CertUtil.installCert(licensePath);
                System.out.println(cert);
                return cert;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    @ApiOperation(value = "获取数据")
    @PostMapping("getData")
    public Boolean verify() {
        try {
            LicenseQueryResult data = CertUtil.getVerifyCertData();
            System.out.println(data);
        } catch (LicenseUtil.LicenseException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return true;
    }
}
```



## 备注

### LicenseQueryResult类字段注解

```java
/**
 * 授权地区
 */
private String district;
/**
 * 授权单位
 */
private List<Unit> unit;

/**
 * 授权类型
 */
private String licenseType;
/**
 * 申请时间
 */
private Date applicationDate;

/**
 * 有效期
 */
private Date licenseEndDate;
/**
 * 申请人
 */
private String applicant;
/**
 * 审批人
 */
private String approver;
/**
 * 备注
 */
private String comment;
/**
 * 机器码
 */
private String machineId;
/**
 * 授权码
 */
private String license;
/**
 * 授权次数
 */
private String number;

/**
 * 扩展信息
 */
private Object extra;
```



### Unit类 字段注释

```java
/**
 * 单位序号
 */
private String xh;
/**
 * 父单位名称
 */
private String PNodeText;
/**
 * 文档简称
 */
private String dwjc;
/**
 * 单位级别
 */
private String dwjb;
/**
 * 单位名称
 */
private String NodeText;
/**
 * 单位类别
 */
private String dwlb;
/**
 *单位属性
 */
private String dwsx;
/**
 * 单位编码
 */
private String NodeId;
/**
 * 父单位编码
 */
private String PNodeId;
/**
 * 单位全称
 */
private String dwqc;
```






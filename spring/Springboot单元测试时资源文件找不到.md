# Springboot单元测试时资源文件找不到



## 错误表述
```
Caused by: java.io.FileNotFoundException: Could not open ServletContext resource [/swagger.properties]
	at org.springframework.web.context.support.ServletContextResource.getInputStream(ServletContextResource.java:159)
	at org.springframework.core.io.support.EncodedResource.getInputStream(EncodedResource.java:159)
	at org.springframework.core.io.support.PropertiesLoaderUtils.fillProperties(PropertiesLoaderUtils.java:110)
	at org.springframework.core.io.support.PropertiesLoaderUtils.fillProperties(PropertiesLoaderUtils.java:81)
	at org.springframework.core.io.support.PropertiesLoaderUtils.loadProperties(PropertiesLoaderUtils.java:67)
	at org.springframework.core.io.support.ResourcePropertySource.<init>(ResourcePropertySource.java:67)
	at org.springframework.core.io.support.DefaultPropertySourceFactory.createPropertySource(DefaultPropertySourceFactory.java:37)
	at org.springframework.context.annotation.ConfigurationClassParser.processPropertySource(ConfigurationClassParser.java:463)
	at org.springframework.context.annotation.ConfigurationClassParser.doProcessConfigurationClass(ConfigurationClassParser.java:280)
	at org.springframework.context.annotation.ConfigurationClassParser.processConfigurationClass(ConfigurationClassParser.java:250)
	at org.springframework.context.annotation.ConfigurationClassParser.processImports(ConfigurationClassParser.java:600)
	... 89 more
```

## 错误产生代码-SpringBootTestContextBootstrapper：
```
	protected String determineResourceBasePath(MergedContextConfiguration configuration) {
		return MergedAnnotations.from(configuration.getTestClass(), SearchStrategy.TYPE_HIERARCHY)
				.get(WebAppConfiguration.class).getValue(MergedAnnotation.VALUE, String.class)
				.orElse("src/main/webapp");
	}
```
> 可以默认情况下，WebApplicationContext的基本资源路径将设置为"src/main/webapp"，但是可以通过提供@WebAppConfiguration批注的替代路径来覆盖此设置

## 处理方案：
#### 一：直接在`main`文件夹下创建一个`webapp`文件夹，在`webapp`文件夹中创建`swagger.properties`文件
#### 二：直接在测试类上添加`@WebAppConfiguration("classpath:/")`,自定义资源路径
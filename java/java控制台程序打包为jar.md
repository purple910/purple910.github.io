# java控制台程序打包为jar



## 1. 创建maven空项目,不需要选择Create from archetype.
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210119091244910-673856207.jpg)

## 创建一个Main方法作为程序的入口.

## 2. 修改pom.xml
```
<plugins>
    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
        <configuration>
            <source>8</source>
            <target>8</target>
        </configuration>
    </plugin>
    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-shade-plugin</artifactId>
        <version>3.2.0</version>
        <executions>
            <execution>
                <phase>package</phase>
                <goals>
                    <goal>shade</goal>
                </goals>
                <configuration>
                    <transformers>
                        <transformer
                                implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                            <!-- 主类的位置，例如上图文件，主类配置应为： -->
                            <mainClass>com.example.demo.Main</mainClass>
                        </transformer>
                    </transformers>
                </configuration>
            </execution>
        </executions>
    </plugin>
</plugins>
```
## 3. 点击Maven工具栏,再点击package,进行打包.

## 4. 如果有资源文件
### 在类中使用
```
File file = new File(Main.class.getClassLoader().getResource("test.txt").getFile());
InputStream inputStream = Main.class.getClassLoader().getResourceAsStream("test.txt");
```
### 在pom.xml里面配置资源文件
```
<resources>
    <resource>
        <directory>src/main/resources</directory>
        <includes>
            <include>*.*</include>
        </includes>
        <filtering>false</filtering>
    </resource>
</resources>
```
## 5. 可以配置jar包名
```
<finalName>test</finalName>
```
## 6. 如果有编码文件
```
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
```

#### 最后的pom.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>demo</artifactId>
    <version>1.0-SNAPSHOT</version>
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    <dependencies>

    </dependencies>

    <build>
        <finalName>test</finalName>
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <includes>
                    <include>*.*</include>
                </includes>
                <filtering>false</filtering>
            </resource>
        </resources>

        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>8</source>
                    <target>8</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.2.0</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <transformers>
                                <transformer
                                        implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <!-- 主类的位置，例如上图文件，主类配置应为： -->
                                    <mainClass>com.example.demo.Main</mainClass>
                                </transformer>
                            </transformers>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>
```
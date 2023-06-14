# idea 配置自定义模板

## 定义类注释
#### 1.在File -> Settings -> Editor -> File and Code Templates -> Includes
这里配置后,会在所有的java文件的头部添加注释,但是如果在创建文件时就引入其他类的话,那么注释会在引入的类上面.
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118131008179-1664325370.jpg)

#### 2.在File -> Settings -> Editor -> File and Code Templates -> Files
这里配置后,表示只会在创建该类文件时才会有注释.
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118131451345-808343404.jpg)

#### 3.在File -> Settings -> Editor -> Live Templates
1. 新建一个Template Group,如果不新建的话则默认为user组里.
2. 新建一个Live Template
3. 配置Abbreviation为/**(是模板名,用于调用模板的)
4.配置Template Test为
```
/**
 * @author:: fate
 * @description: 
 * @date: $date$  $time$
 **/
```
5.设置应用场景为java的comment就可以了.
6.点击EDIT VARIABLES
7.配置参数,可以在Expression中选择参数,可以设置默认值(如果是调用当前其他参数,则将其放在被调用的下面;如果为常量则需要用双引号),Skip if Def是判断是否需要跳过(勾上,则直接跳过;不勾,则在创建注释后把光标放在哪里;用可以通过调整参数的先后顺序来控制光标的移动顺序).
8.在类上,输入/**,按tab键即可(亦可以修改为其他键)
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118133413916-1571297783.jpg)
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118133442289-1052311846.jpg)
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118133522142-771946119.jpg)

#### 3.在File -> Settings -> Editor -> Live Templates
这种与上面那种相似.不过使用的是idea里面默认的注释方法 /*+模板名.
修改Abbreviation为class(可以随意)
修改Template Text
```
*
 * @author: fate
 * @description: 
 * @date: $date$  $time$
 **/
```
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118133959756-478144654.jpg)


## 自定义方法注释
1. 创建新的Live Template
2. Abbreviation为me
3. 应用场景为java的comment就可以了.
4. Template text
```
*
 * @description: $describle$ $param$ $return$
 */
```
5. 配置return与param参数
return:
```
groovyScript("if(\"${_1}\".length() == 2) {return '';} else {def result=''; def returns=\"${_1}\"; if(returns != 'void'){result+='\\n * @return: ' + returns}; return result;}", methodReturnType());
```
param:
```
groovyScript("if(\"${_1}\".length() == 2) {return '';} else {def result=''; def params=\"${_1}\".replaceAll('[\\\\[|\\\\]|\\\\s]', '').split(',').toList();for(i = 0; i < params.size(); i++) {if(i<(params.size()-1)){result+='\\n' + ' * @param ' + params[i] + ' : '}else{result+='\\n * @param ' + params[i] + ' : '}}; return result;}", methodParameters()); 
```
6. 在方法上面输入/*me,然后按tab键即可.
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118134713303-1067294872.jpg)

## 自定方法简写
注意的p1是直接引用的param参数的值,所以要把p1放在param下面,勾选上Skip.
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118135417073-276510261.jpg)
![](https://img2020.cnblogs.com/blog/1863149/202101/1863149-20210118134952541-1443888361.jpg)
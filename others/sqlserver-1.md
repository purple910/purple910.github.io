---
title: "SQLServer"
date: 2019-07-17T14:24:55+08:00
draft: true
---

## 去除数据库登录界面的所有用户信息
```
C:\Users\asus\AppData\Roaming\Microsoft\SQL Server Management Studio\14.0\SqlStudio.bin
```

## 查询姓名中第二个字与第三个字相同:
```
select * from Student s2 where SUBSTRING(s2.sname,2,1)=SUBSTRING(s2.sname,3,1)
```

## 用户授权
1 创建用户
```
create login names with password='pwd' , default_database=test;
create user names for login names with default_schema=dbo;
```
2 增删改查授权<br>
```
grant select,insert,UPDATE,DELETE on 表 to names
```
3 创建表
```
grant create table to names 
GRANT ALTER ON SCHEMA::dbo TO names;
```
4 存储过程授权
```
GRANT EXECUTE ON 存储过程名 TO username
```
5 禁止对表授权
```
DENY UPDATE ON 表 TO username CASCADE;
```
6 回收权限
```
REVOKE DELETE ON 表 FROM username
```
7 删除表
```
truncate table a
delete from dbo.a
drop table a
```
8 修改列
```
alter table a add sa nvarchar(10) not null
Alter Table a Add Constraint PK_Course_Cno Primary Key(id)
ALTER TABLE a ALTER COLUMN id int
ALTER TABLE a DROP CONSTRAINT PK_a
alter table a drop column sa
```
9 创建一个简单的登录，登录名为：newlogin；登录密码：123456；默认数据库：master，默认数据库也可以不指定。
```
EXEC sp_addlogin 'newlogin','123456','master'
```
10 创建用户

* 创建一个简单的用户，如果不指定用户名，则添加到当前数据库登录名中，如果不指定角色，则该用户默认属于public角色。下为添加newlogin登录名。
```
EXEC sp_adduser 'newlogin'
```
* 创建一个带用户名的用户，用户可以与登录名相同（同上一种类似），也可以不同，但要设定当前登录名，用户角色可选，默认为public。下为将用户newuser添加到newlogin登录名中。
```
EXEC sp_adduser 'newlogin','newuser'
```
* 创建角色
```
EXEC sp_addrole 'newrole'
```
* 下为将用户下为将用户newuser添加到newlogin登录名中。并指定newrole角色。
```
EXEC sp_adduser 'newlogin','newuser','newrole'
```
* 为角色newrole赋予jobs表的所有权限
```
GRANT ALL ON jobs TO newrole
```
* 为角色newrole赋予sales表的查、改权限
```
GRANT SELECT,UPDATE ON sales TO newrole
```
* 禁止角色newrole使用employees表的插入权限
```
DENY INSERT ON employees TO newrole
```
* 另一种创建用户和赋予角色的方式
* 为登录newlogin在数据库中添加安全账户newuser
```
EXEC sp_grantdbaccess 'newlogin','newuser'
```
* 添加newuser为角色newrole的成员
```
EXEC sp_addrolemember 'newrole','newuser'
```
* 数据库用户、角色、登录的删除操作
* 删除当前数据库用户
```
EXEC sp_revokedbaccess 'newuser';
```
* 删除数据库登录
```
EXEC sp_droplogin 'newlogin'
```
* 删除数据库角色
```
EXEC sp_droprole 'newrole'
```
* 从数据库角色(newrole)中删除用户(newuser)
```
EXEC sp_droprolemember 'newrole', 'newuser'
```
* 用SQL代码新建登录、用户.创建带密码的mylogin登录名，MUST_CHANGE 选项需要用户首次连接服务器时更改此密码。
```
CREATE LOGIN mylogin WITH PASSWORD = '123456' MUST_CHANGE;
```
* 创建映射到凭据的登录名。以下示例将创建mylogin登录名。此登录名将映射到mycredential凭据。
```
CREATE LOGIN mylogin WITH PASSWORD = '123456',
CREDENTIAL = mycredential;
```
* 从Windows 域帐户创建登录名.如果从Windows 域帐户映射登录名，则登录名必须用方括号([ ]) 括起来。
```
CREATE LOGIN [jack\xiangzhao] FROM WINDOWS;
```
* 如果指定用户名，则不使用默认登录名作为该数据库用户
```
CREATE USER myuser FOR LOGIN mylogin
```
* 以下示例将创建用户myuser拥有的数据库角色myrole
```
CREATE ROLE myrole AUTHORIZATION myuser;
```
* 以下示例将创建db_role固定数据库角色拥有的数据库角色myrole
```
CREATE ROLE myrole AUTHORIZATION db_role
```

## 规则
1 创建雇佣日期规则 hire_date_rule
```
CREATE RULE hire_date_rule
AS @hire_date>='1980-01-01' and @hire_date<=getdate()
```
2 创建性别规则sex_rule
```
CREATE RULE sex_rule
AS @sex in ('男','女')
```
3 -创建评分规则grade_rule
```
CREATE RULE grade_rule
AS @value between 1 and 100
```
4 创建字符规则my_character_rule
```
Create rule my_character_rule
As @value like '[a-z]%[0-9]' 
```
5 sp_helptext 查看规则,查看规则hire_date_rule的文本信息
```
EXECUTE sp_helptext hire_date_rule
```
6 sp_bindrule绑定规则

* 将规则hire_date_rule绑定到employee表的hire_date列上
```
EXEC sp_bindrule hire_date_rule, 'employee.hire_date'
```
* 定义用户定义数据类型pat_char，将规则my_character_rule绑定到pat_var上
```
EXEC sp_addtype pat_char,'varchar(10)','NOT NULL'
EXEC sp_bindrule my_character_rule, pat_char, 'futureonly';
```
7 sp_unbindrule 解除规则的绑定
* 解除绑定在employee表的hire_date列和用户定义数据类型pat_char上的规则
```
EXEC sp_unbindrule 'employee.hire_date';
* DROP RULE语句删除当前数据库中的一个或多个规则
DROP RULE sex_rule,hire_date_rule 
```

## 分页
```
select * from (
select * ,ROW_NUMBER() over(order by sid) as rowcindex --增加索引
from Student) as t
where t.rowcindex between 1 and 3;
```
## 分裂与合并
```
select s.sid,s.sname,
max(case c.cname when '语文' then sc.score end) as '语文',
min(case c.cname when '数学' then sc.score end) as '数学',
sum(case c.cname when '英语' then sc.score end) as '英语',
max(case c.cname when '化学' then sc.score else 0 end) as '化学'
from (Student as s inner join SC as sc on s.sid=sc.sid
inner join Course as c on c.cid=sc.cid)
group by s.sid,s.sname;
```


## T-sql
1 全局变量
```
select @@VERSION --数据库版本
insert into Course values('',''); select @@IDENTITY --获取最近insert语句的标识
print @@servername --服务器名称
print @@rowcount--返回受影响的行数
```

2 选择语句
```
declare @id int
set @id =10
if @id>5
begin
    print 'ok'
end
else
begin
    print 'no'
end
```
3 循环语句
```
declare @id int
set @id=1
while @id<10
begin 
	print @id
	set @id=@id+1
end
```
4 异常
```
begin try
	delete from SC--不能成功
end try
begin catch
	print @@error --判断错误信息 0对
end catch
```
5 事务:回滚函数
```
begin try
	begin transaction --开启事务
	--错误SQL
	commit tran --提交事务
end try
begin catch
	rollback tran --回退事务
end catch
```
6 锁:同步
```
begin tran --锁上
	 --修改操作
rollback tran --开锁 commit tran
```


---
title: "连接 Sqlserver"
date: 2019-07-18T19:51:15+08:00
draft: true
---

# java连接sqlserver
```
1 创建 Dynamic Web Project项目
    在WebContent/WEB-INF/lib中添加sqljdbc42.jar
2 在class文件里连接数据库
    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
	String url = "jdbc:sqlserver://localhost:1433;databaseName = text";
	String a = "sa";
	String b = "admin";
	Connection conn=DriverManager.getConnection(url,"sa","admin"); 
    PreparedStatement pstat = conn.prepareStatement(sql);
    ResultSet rs = pstat.executeQuery();
    ---------------------------------------------------------
    Statement stat = conn.createStatement();
    ResultSet rs = stat.executeQuery(sql);
```


# Spring中连接sqlserver
```
1 添加sqljdbc.jarjiabao
    <dependency>
        <groupId>com.microsoft.sqlserver</groupId>
        <artifactId>sqljdbc4</artifactId>
        <version>4.2</version>
    </dependency>
2 在配置文件中连接数据库(application.yml)
    spring:
        datasource:
            url: jdbc:sqlserver://localhost:1433;DatabaseName=practice
            driver-class-name: com.microsoft.sqlserver.jdbc.SQLServerDriver
            username: sa
            password: admin
3 操作数据库
    @Autowired
    JdbcTemplate jdbcTemplate;
    public List<StudentBean> getStudentByRubric(String id){
            List<StudentBean> user = jdbcTemplate.query("select * from Student where rid ='"+id+"'",
                    new BeanPropertyRowMapper<StudentBean>(StudentBean.class));
            return user;
        }
4 idea中有数据库插件可以将Microsoft SQL Server Management Studio 17中需要操作的数据库导入idea
    Database->new->Data Source->Microsoft SQL Server->Port(1433),Instance(数据库名)->Test Connection
```

# C#连接sqlserver
```
1 加载数据库
    工具->连接数据库->Microsoft SQL Server (SqlClient)->服务器名(登录Microsoft SQL Server Management Studio使得服务器名称)->其他操作
2 连接数据库    
    using System.Data.SqlClient;
    string url = 服务器资源管理器->数据连接->属性->连接字符串
    SqlConnection conn = new SqlConnection(url)
3 操作数据库
    string sql = "select * from table";
    SqlCommand cmd = new SqlCommand(sql, conn)
    conn.Open();
    cmd.CommandType = CommandType.Text;
    SqlDataReader re = cmd.ExecuteReader();
    ---------------------------------------------------------------
    cmd.CommandType = CommandType.Text;
    result = cmd.ExecuteNonQuery();
```

# QT连接数据库
```
1 创建ODBC
    打开ODBC数据资源管理程序->添加->SQL Server->服务器(登录SSMS的服务器名称)->选择登陆的类型->选择要添加的数据库
2 连接ODBC
    QSqlDatabase db = QSqlDatabase::addDatabase("QODBC");
    QString dsn = QString::fromLocal8Bit(创建SQL Server ODBC的名称);
    db.setHostName("127.0.0.1");
    db.setDatabaseName(dsn);
    db.setUserName("sa");
    db.setPassword("admin");
    db.open();
3 操作数据库
    QSqlQuery query(db);
    query.exec("select * from Student");
    db.close();
```
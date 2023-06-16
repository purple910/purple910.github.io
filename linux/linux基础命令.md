
# 控制进程和守护服务
```
//查看进程是否在运行
systemctl status rsyslog
//查看进程是否开机启动
systemctl is-enable rsyslog.service
//如果不是
systemctl enable rsyslog
```

# 网络配置
```
//查看网络设备
nmcli device status
//查看连接列表
nmcli connection show
//查看接口配置
ip addr show [ens33]
//新建网络连接
nmcli connection add con-name ens160 type ethernet ifname 网关 ipv4.addresses 192.168.0.5/24 gw4 192.168.1.254 ipv4.dns 8.8.8.8
//更换连接
nmcli connection up ens160
//停止网络接口
nmcli device disable ens160
//修改网络连接
nmcli connection modify ens160 ipv4.addresses "192.168.1.2/24 192.168.1.254"
//添加dns
nmcli connection modify ens160 +ipv4.dns 192.168.1.1
//更改主机名
hostnamectl localhost
//配置网关别名
echo "192.168.0.254  www.fate.com">>/etc/hosts
```


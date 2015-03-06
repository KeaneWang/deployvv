# deployvv
这是一个简单粗暴的部署更新系统

## 目标环境
服务器：centos 6.x
客户端：ubuntu 14.04

## 依赖
* python 2.x
* git

## 编写目的
由于我们这边需要服务器处理的数据量比较大，所以需要把数据分散到各个服务器进行存储和处理。处理服务器跑着结构相同的数据库和处理程序，但是它们可能会根据业务罗辑进行改变，为了避免每次业务罗辑修改，我需要手动修改各个服务器，开发此简单粗暴的部署更新系统

## 功能说明
当需要更新所有服务器上的内容时，只需将内容提交到某服务器能访问到的git server，并执行client/client.py，服务器就会自动git pull代码，并执行内部的update.sh，完成更新部署。
每台服务器运行该系统会开启一个tcp server，监听某个端口。client/client.py会向各个服务器发送更新指令。二者之间的通信是经过简单加密的。

## 安装配置
### 安装依赖软件

* Ubuntu 14.04
    ```
    sudo apt-get install git python-pip
    sudo pip install rsa
    ```

* CentOS 6.x
    ```
   cd /tmp
   wget --no-check-certificate https://pypi.python.org/packages/source/p/pip/pip-6.0.8.tar.gz#md5=2332e6f97e75ded3bddde0ced01dbda3
    tar zxvf pip-6.0.8.tar.gz
    cd pip-6.0.8
    python setup.py install
    pip install rsa
    yum install -y git
    ```

### 首次配置
1. 自己建立一个外网能够访问的私有git仓库，比如在git.oschina.net上
2. 执行```python bin/generatekey.py```，生成公钥、私钥
3. 将全部内容提交到你建立的git仓库
4. 将目标服务器的公钥配置到你建立的git仓库，以便它们有权限往下pull内容
5. 配置conf/deploy.json，配置服务器需要监听的端口号
6. 在目标服务器上执行(root权限)
    ```
    cd /opt
    git clone xxx
    cd deployvv
    chmod +x bin/install.sh
    ./bin/install.sh
    ```
    如果没有提示错误，说明程序正常运行
7. 在客户端，配置client/server_list.json，将目标服务器的IP和监听端口号填写好

### 执行更新
首先将内容push，然后执行```python client/client.py```,完成更新

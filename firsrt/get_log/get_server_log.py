#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/15/星期二 9:25
# @Author  : JingQi
# @File    : get_server_log
# @Software: PyCharm


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ssh_grep_simple.py
------------------
密码登录服务器 -> 执行 cat xx.log | grep xxx > xxx.txt -> 把 txt 拉回本地。

用法：先把下面【配置区】填好（留空的运行时会问你），然后执行：
    D:/install/py39/python.exe ssh_grep_simple.py
"""

import getpass
import os
import shlex
import sys
import time
from datetime import datetime
import paramiko

# ====================== 配置区（一般只需要改这里） ======================
HOST = "8.139.7.122"             # 服务器地址，例：192.168.1.100
PORT = 22             # SSH 端口
USER = "dbConn"             # 账号，例：root
PASSWORD = "hzyr@2025"        # 密码；留空则运行时用 getpass 输入（不落在文件里，更安全）
REMOTE_LOG = "/disk1/log/zhcbpt-dock/zhcbpt-dock_stdout.2026-09-15.log"       # 远端日志绝对路径，例：/var/log/app/app.log
KEYWORD = "{}".format(sys.argv[1])          # 过滤关键字，例：ERROR
GREP_OPTS = ""        # grep 附加参数，留空即可；要行号写 "-n"，忽略大小写写 "-i"
REMOTE_OUT = ""       # 远端临时结果文件名，留空自动用 /tmp/grep_<时间戳>.txt
LOCAL_OUT = "{0}\\{1}-{2}.txt".format(os.getcwd(),sys.argv[1],str(datetime.now().strftime("%Y%m%d%H%M%S")))        # 本地保存路径，留空 = 脚本同目录、同名
DELETE_REMOTE = True  # 拉取成功后是否删掉远端临时文件
TIMEOUT = 30          # 连接超时（秒）
# ======================================================================


def ask(label, value, secret=False, default=""):
    """配置项为空就现场问用户。"""
    if value:
        return value
    if secret:
        return getpass.getpass("请输入%s: " % label)
    tip = " [%s]" % default if default else ""
    return input("请输入%s%s: " % (label, tip)).strip() or default


def main():
    host = ask("服务器地址", HOST)
    user = ask("账号", USER)
    password = ask("密码", PASSWORD, secret=True)
    remote_log = ask("远端日志绝对路径", REMOTE_LOG)
    keyword = ask("过滤关键字", sys.argv[1])
    port = int(PORT)

    remote_out = REMOTE_OUT or "/tmp/grep_%s.txt" % time.strftime("%Y%m%d_%H%M%S")
    local_out = LOCAL_OUT or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.path.basename(remote_out)
    )

    # ---- 1. 密码登录 ----
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("[1/4] 连接 %s@%s:%s ..." % (user, host, port))
    try:
        cli.connect(hostname=host, port=port, username=user,
                    password=password, timeout=TIMEOUT)
    except paramiko.AuthenticationException:
        print("[错误] 账号或密码不对（也可能是该账号不允许 SSH 登录）")
        return 1
    except Exception as e:
        print("[错误] 连接失败：%s" % e)
        return 1
    print("连接成功")

    try:
        # ---- 先确认日志文件在 ----
        _, out, _ = cli.exec_command(
            "test -f %s && echo OK || echo NO" % shlex.quote(remote_log), timeout=TIMEOUT)
        if out.read().decode("utf-8", "replace").strip() != "OK":
            print("[错误] 远端找不到这个文件：%s" % remote_log)
            return 1

        # ---- 2. 执行 cat xx.log | grep xxx > xxx.txt ----
        cmd = "cat %s | grep %s %s > %s" % (
            shlex.quote(remote_log), GREP_OPTS, shlex.quote(keyword), shlex.quote(remote_out))
        print("[2/4] 远端执行： %s" % cmd)
        stdin, stdout, stderr = cli.exec_command(cmd)
        stdin.close()
        code = stdout.channel.recv_exit_status()
        err = stderr.read().decode("utf-8", "replace").strip()
        if err:
            print("      远端提示： %s" % err)
        if code == 1:
            print("      [提示] 没匹配到关键字，TXT 是空的（换个关键字或加 GREP_OPTS=\"-i\" 再试）")
        elif code > 1:
            print("[错误] 远端命令执行失败（退出码 %d）" % code)
            return 1

        # ---- 3. 把 txt 拉取到本地 ----
        print("[3/4] 拉取到本地： %s" % local_out)
        sftp = cli.open_sftp()
        try:
            sftp.get(remote_out, local_out)
        finally:
            sftp.close()

        if DELETE_REMOTE:
            cli.exec_command("rm -f %s" % shlex.quote(remote_out))[1].channel.recv_exit_status()
            print("      已删除远端临时文件 %s" % remote_out)
    finally:
        cli.close()

    # ---- 4. 结果 ----
    with open(local_out, "rb") as fp:
        n_lines = sum(1 for _ in fp)
    print("[4/4] 完成： %s（%d 行，%d 字节）"
          % (local_out, n_lines, os.path.getsize(local_out)))
    print(" 注：文件按原样二进制下载，若打开是乱码说明远端日志不是 UTF-8 编码。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

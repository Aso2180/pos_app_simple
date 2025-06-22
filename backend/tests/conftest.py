import os
import shutil
import subprocess
import tempfile
import time
import pwd
import pathlib

import pytest
import pymysql


@pytest.fixture(scope="session")
def mysql_fixture(tmp_path_factory):
    data_dir = pathlib.Path(tempfile.mkdtemp(prefix="mysql_data_", dir="/tmp"))
    socket_path = data_dir / "mysql.sock"
    pid_file = data_dir / "mysqld.pid"

    mysql_user = pwd.getpwnam("mysql")
    os.chown(data_dir, mysql_user.pw_uid, mysql_user.pw_gid)

    subprocess.run(
        [
            "mariadb-install-db",
            f"--datadir={data_dir}",
            "--user=mysql",
            "--auth-root-authentication-method=normal",
        ],
        check=True,
    )

    proc = subprocess.Popen(
        [
            "mariadbd",
            f"--datadir={data_dir}",
            f"--socket={socket_path}",
            "--skip-networking",
            "--user=mysql",
            f"--pid-file={pid_file}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    for _ in range(100):
        if proc.poll() is not None:
            out, err = proc.communicate()
            raise RuntimeError(
                "mariadbd failed to start",
                out.decode(),
                err.decode(),
            )
        try:
            conn = pymysql.connect(user="root", unix_socket=str(socket_path))
            conn.close()
            break
        except Exception:
            time.sleep(0.1)
    else:
        proc.terminate()
        proc.wait()
        raise RuntimeError("mariadbd did not start in time")

    conn = pymysql.connect(user="root", unix_socket=str(socket_path), autocommit=True)
    conn.user = b"root"
    conn.unix_socket = str(socket_path)

    yield conn

    with conn.cursor() as cur:
        cur.execute("SHOW DATABASES LIKE 'pos_app_test'")
        if cur.fetchone():
            cur.execute("DROP DATABASE pos_app_test")
    conn.close()
    proc.terminate()
    proc.wait()
    shutil.rmtree(data_dir, ignore_errors=True)


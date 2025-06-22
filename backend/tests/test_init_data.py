import importlib
import pathlib
import sys
from pytest_mysql.factories import mysql, mysql_proc

mysql_proc_fixture = mysql_proc()
mysql_fixture = mysql("mysql_proc_fixture", dbname="pos_app_test")

def test_init_data(mysql_fixture, monkeypatch):
    # Ensure backend package is importable
    backend_dir = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(backend_dir))
    user = mysql_fixture.user.decode() if isinstance(mysql_fixture.user, bytes) else mysql_fixture.user
    url = (
        f"mysql+pymysql://{user}@localhost/pos_app_test?"
        f"unix_socket={mysql_fixture.unix_socket}"
    )
    monkeypatch.setenv("DATABASE_URL", url)
    import app.db as db
    import app.models as models
    import app.init_data as init_data
    importlib.reload(db)
    importlib.reload(models)
    importlib.reload(init_data)
    monkeypatch.setattr(db, "CA_CERT", "/etc/ssl/certs/ca-certificates.crt", raising=False)
    monkeypatch.setattr(init_data, "CA_CERT", "/etc/ssl/certs/ca-certificates.crt", raising=False)

    def _create_db():
        with mysql_fixture.cursor() as cur:
            cur.execute(
                "CREATE DATABASE IF NOT EXISTS pos_app_test CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
            )

    monkeypatch.setattr(init_data, "create_database_if_not_exists", _create_db)

    init_data.main()

    with mysql_fixture.cursor() as cur:
        cur.execute("SHOW TABLES")
        tables = {row[0] for row in cur.fetchall()}
    for t in ["prd_mst", "trd", "trd_dtl"]:
        assert t in tables

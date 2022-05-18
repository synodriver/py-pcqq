import sqlite3

class SqliteDB:
    def __init__(self, path: str) -> None:
        db = sqlite3.connect(path)
        cu = db.cursor()

        self.close = db.close
        self.commit = db.commit
        self.execute = cu.execute
        self.fetchone = cu.fetchone
        self.fetchall = cu.fetchall

    def create(self, table_name: str, *args) -> bool:
        try:
            self.execute("create table %s %s" % (
                table_name, str(args).replace("'", "")
            ))
            self.commit()
            return True
        except:
            return False

    def insert(self, table_name: str, *args):
        '''调用本方法后需手动调用commit方法'''
        args = [f"'{arg}'" if isinstance(arg, str) else str(arg) for arg in args]
        self.execute(f'insert into {table_name} values ({", ".join(args)})')

    def select(self, table_name: str, **params) -> list:
        self.execute("select * from %s where %s" % (
            table_name, " and ".join(
                [f"{key}={params[key]}" for key in params])
        ))
        return self.fetchall()

    def exist(self, table_name: str, **params) -> bool:
        return bool(self.select(table_name, **params))

    def update(self, table_name: str, *args, **params):
        args = " ".join(args)
        params = " ".join([f"{key}={params[key]}" for key in params])
        self.execute(f"update {table_name} set {args} where {params}")
        self.commit()

    def delete(self, table_name: str, **params):
        self.execute(
            f'select * from {table_name} where {" ".join([f"{key}={params[key]}" for key in params])}'
        )

        self.commit()

    def count(self, table_name: str) -> int:
        try:
            self.execute(f"select count(*) from {table_name}")
            return self.fetchone()[0]
        except sqlite3.OperationalError:
            return -1
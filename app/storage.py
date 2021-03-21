import asyncpg
from app.user import User


class UserStorage:
    users_list = list()
    conn = None

    async def set_conn(self, user, host, port, password, database):
        self.conn = await asyncpg.connect(user=user,
                                          host=host,
                                          port=port,
                                          database=database,
                                          password=password
                                          )
        users = await self._fetch_all()
        self.users_list = list(user["id"] for user in users)

    def __getitem__(self, item):
        return self.get(item)

    def __contains__(self, key_value):
        return key_value in self.users_list

    async def items(self):
        raw_users = await self._fetch_all()
        users = list()
        for raw_user in raw_users:
            user = User(raw_user["nickname"], raw_user['login'], is_admin=raw_user["is_admin"],
                        subscription=raw_user["subscription"],
                        imporved=raw_user["improved"], banned=raw_user['banned']
                        )
            users.append((raw_user["id"], user))
        return users

    async def get(self, key):
        raw_user = await self._fetch_one(key)
        for tmp_user in raw_user:
            user = User(tmp_user["nickname"], tmp_user['login'], is_admin=tmp_user["is_admin"],
                        subscription=tmp_user["subscription"],
                        imporved=tmp_user["improved"], banned=tmp_user['banned']
                        )
            return user

    async def update(self, key_value):
        for key, value in key_value.items():
            if key in self.users_list:
                await self._change(key, user=value)
                return
            await self._set(key, user=value)
            self.users_list.append(key)

    async def _fetch_all(self):
        result = await self.conn.fetch('''select * from users''')
        return result

    async def _fetch_one(self, id_user):
        result = await self.conn.fetch(f'''select * from users where id={id_user}''')
        return result

    async def _set(self, key, user):
        await self.conn.execute(
            f'''insert into users values({key}, '{user.nickname}', '{user.login}', {user.is_admin}, {user.subscription},''' + \
            f'''{user.improved}, {user.banned})'''
        )

    async def _change(self, key, user):
        await self.conn.execute(
            f'''update users set nickname='{user.nickname}',''' + \
            f'''login ='{user.login}',''' + \
            f'''is_admin={user.is_admin},''' + \
            f'''subscription={user.subscription},''' + \
            f'''improved={user.improved},''' + \
            f'''banned={user.banned} ''' + \
            f'''where id={key}'''
        )

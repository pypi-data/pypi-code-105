import uuid

from rethinkdb import r

from .config import RethinkDBConfig


class RethinkDBClient:
    _connection = None

    def __init__(self, config: RethinkDBConfig):
        self._config = config

    async def init(self):
        r.set_loop_type('asyncio')
        self._connection = await r.connect(
            host=self._config.host,
            port=self._config.port,
            password=self._config.password,
        )

        db_list = await r.db_list().run(self._connection)
        for db in self._config.db:
            if db not in db_list:
                await r.db_create(db).run(self._connection)

    async def init_table(self, db, table, indexes):
        table_list = await r.db(db).table_list().run(self._connection)
        if table not in table_list:
            await r.db(db).table_create(table).run(self._connection)

        index_list = await r.db(db).table(table).index_list().run(self._connection)
        for index in indexes:
            if index not in index_list:
                await r.db(db).table(table).index_create(index).run(self._connection)
                await r.db(db).table(table).index_wait(index).run(self._connection)

    async def save(self, obj, object_space, object_type):
        await self.init_table(object_space, object_type, obj.Internal.indexes)

        if not obj.object_id:
            obj.object_id = str(uuid.uuid4())

            await r.db(object_space).table(object_type).insert(obj.data).run(self._connection)
            return

        data = obj.data
        data.pop('created_at')
        
        await r.db(
            object_space
        ).table(
            object_type
        ).filter(
            {'object_id': obj.object_id}
        ).limit(1).update(data).run(self._connection)

    async def delete(self, obj, object_space, object_type):
        await self.init_table(object_space, object_type, obj.Internal.indexes)

        await r.db(
            object_space
        ).table(
            object_type
        ).filter(
            {'object_id': obj.object_id}
        ).limit(1).delete().run(self._connection)

    async def get(self, obj_cls, object_space, object_type, object_id):
        await self.init_table(object_space, object_type, obj_cls.Internal.indexes)

        result = await r.db(
            object_space
        ).table(
            object_type
        ).filter(
            {'object_id': object_id}
        ).limit(1).run(self._connection)

        items = [item async for item in result]
        if len(items) < 1:
            return None

        return obj_cls(**items[0])

    async def find(self, obj_cls, object_space, object_type, filter):
        if filter.order_direction == 'asc':
            order_by_expr = r.asc(filter.order_by)
        else:
            order_by_expr = r.desc(filter.order_by)

        result = await r.db(
            object_space
        ).table(
            object_type
        ).order_by(
            index=order_by_expr
        ).filter(
            filter.fields
        ).skip(
            filter.page_size*filter.page_no
        ).limit(
            filter.page_size
        ).run(self._connection)

        items = [item async for item in result]
        return [obj_cls(**item) for item in items]

    def __str__(self):
        return f'RethinkDB client [{self._config.host}:{self._config.port}]'

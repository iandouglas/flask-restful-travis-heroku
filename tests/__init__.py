from sqlalchemy import MetaData, ForeignKeyConstraint, Table
from sqlalchemy.engine import reflection
from sqlalchemy.sql.ddl import DropConstraint, DropTable


def assert_payload_field_type_value(obj, payload, field, data_type, value):  # pragma: no cover
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)
    obj.assertEqual(value, payload[field])


def assert_payload_field_type(obj, payload, field, data_type):  # pragma: no cover
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)


def db_drop_everything(db):   # pragma: no cover
    # source: https://www.mbeckler.org/blog/?p=218
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = db.engine.connect()
    trans = conn.begin()
    inspector = reflection.Inspector.from_engine(db.engine)
    metadata = MetaData()
    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((), (), name=fk['name'])
            )
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)
    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))
    for table in tbs:
        conn.execute(DropTable(table))
    trans.commit()

from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine

engine = create_engine('sqlite:///database.db')
meta = MetaData()
conn = engine.connect()
tags = Table(
    'tags', meta,
    Column('name', String, primary_key=True),
    Column('content', String),
    Column('creatortag', String),
    Column('creatorid', Integer),
    Column('createdat', String),
    Column('guild', Integer)
)
muted_roles = Table(
    'muted_roles', meta,
    Column('id', Integer),
    Column('guild', Integer)
)
muted_members = Table(
    'muted_members', meta,
    Column('id', Integer),
    Column('guild', Integer),
    Column('unmute_after', Integer)
)

meta.create_all(engine)

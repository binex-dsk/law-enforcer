from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, create_engine

engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})
meta = MetaData()
conn = engine.connect()
tags = Table(
    'tags', meta,
    Column('name', String),
    Column('content', String),
    Column('creatortag', String),
    Column('creatorid', Integer),
    Column('createdat', String),
    Column('guild', Integer, unique=True)
)
server_config = Table(
    'server_config', meta,
    Column('ban_delete_days', Integer, default=1),
    Column('ban_dm', Boolean, default=True),
    Column('ban_dm_message', String, default='{MEM}, you have been **banned** from {GUILD} by {MOD}.\nReason: {REASON}'),
    Column('unban_dm', Boolean, default=True),
    Column('unban_dm_message', String, default='{MEM}, you have been **unbanned** from {GUILD} by {MOD}.\nReason: {REASON}'),
    Column('kick_dm', Boolean, default=True),
    Column('kick_dm_message', String, default='{MEM}, you have been **kicked** from {GUILD} by {MOD}.\nReason: {REASON}\n{INV}'),
    Column('kick_dm_invite', Boolean, default=True),
    Column('kick_dm_inv_message', String, default='I have created a one-time-use invite for you to join back with: {INV}'),
    Column('mute_dm', Boolean, default=True),
    Column('mute_dm_message', String, default='{MEM}, you\'ve been muted in {GUILD} by {MOD} for {TIME} hours.\nReason: {REASON}'),
    Column('unmute_dm', Boolean, default=True),
    Column('unmute_dm_message', String, default='{MEM}, you\'ve been unmuted in {GUILD} by {MOD}.\nReason: {REASON}'),
    Column('mute_evasion_time', Integer, default=12),
    Column('mute_evasion', Boolean, default=True),
    Column('punish_mute_evasion', Boolean, default=True),
    Column('tag_require_command', Boolean, default=True),
    Column('tag_search_all', Boolean, default=False),
    Column('clear_delete_pinned', Boolean, default=False),
    Column('allow_all_addtag', Boolean, default=False),
    Column('disabled_cmds', String, default=''),
    Column('guild', Integer, unique=True)
)
muted_roles = Table(
    'muted_roles', meta,
    Column('id', Integer),
    Column('guild', Integer, unique=True)
)
muted_members = Table(
    'muted_members', meta,
    Column('id', Integer),
    Column('guild', Integer),
    Column('unmute_after', Integer)
)

meta.create_all(engine)

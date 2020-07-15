# pylint: disable=unused-variable
from tables import conn
def exists(table, values): # I could do this way better but this works
    selection = table.select()
    selection = (selection.where(table.c[list(values.keys())[i]] == list(values.values())[i]) for i in enumerate(values))

    result = conn.execute(selection)
    rowlen = 0
    for _ in result:
        rowlen += 1
    return rowlen != 0

def insert(table, values):
    try:
        conn.execute(table.insert(), [
            values
        ])
    except:
        raise Exception('Table does not exist.')

def delete(table, values):
    fetched = fetch(table, values)
    if not fetched:
        raise Exception('Row not found.')

    del_select = table.delete()
    del_select = (del_select.where(table.c[list(values.keys())[i]] == list(values.values())[i]) for i in enumerate(values))
    return conn.execute(del_select)

def fetch(table, values):
    if not exists(table, values):
        return None
    selection = table.select()
    selection = (selection.where(table.c[list(values.keys())[i]] == list(values.values())[i]) for i in enumerate(values))
    return conn.execute(selection)

def update(table, checkVals, newVals):
    fetched = fetch(table, checkVals)
    if not fetched:
        raise Exception('Row not found.')
    upd = table.update()
    upd = (upd.where(table.c[list(checkVals.keys())[i]] == list(checkVals.values())[i]) for i in enumerate(checkVals))

    upd = (upd.values({table.c[list(newVals.keys())[i]]: list(newVals.values())[i]}) for i in enumerate(newVals))
    return conn.execute(upd)

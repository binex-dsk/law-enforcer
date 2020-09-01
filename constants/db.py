from tables import conn
def exists(table, values): # I could do this way better but this works
    """Checks if a row exists in a table.

    Params:
        table (sqlalchemy.Table): The table to check.

        values (dict): Values to check for existence.
    Return value: Whether the table exists or not (bool)."""
    selection = table.select()
    for i, _ in enumerate(values):
        selection = selection.where(table.c[list(values.keys())[i]] == list(values.values())[i])

    result = conn.execute(selection)
    rowlen = 0
    for _ in result:
        rowlen += 1
    return rowlen != 0

def insert(table, values):
    """Insert values into a table.

    Params:
        table (sqlalchemy.Table): The table to insert into.

        values (dict): The values to insert into the table.
    Return value: None or sqlalchemy.ResultProxy object.

    Throws an error if the table does not exist."""
    #try:
    return conn.execute(table.insert(), [
        values
    ])
    """except Exception as e:
        print(e)
        raise Exception('Table not found.')"""

def delete(table, values):
    """Deletes a value from a table.

    Params:
        table (sqlalchemy.Table): The table to delete from.

        values (dict): The search value to delete.
    Return value: None or sqlalchemy.ResultProxy object.

    Throws an error if the row does not exist."""
    fetched = fetch(table, values)
    if not fetched:
        raise Exception('Row not found.')

    del_select = table.delete()
    for i, _ in enumerate(values):
        del_select = del_select.where(table.c[list(values.keys())[i]] == list(values.values())[i])
    return conn.execute(del_select)

def fetch(table, values):
    """Fetches a row from a table.

    Params:
        table (sqlalchemy.Table): The table to fetch a row from.

        values (dict): The values to search for.
    Return value: None or sqlalchemy.ResultProxy object."""
    
    if not exists(table, values):
        return None
    selection = table.select()
    for i, _ in enumerate(values):
        selection = selection.where(table.c[list(values.keys())[i]] == list(values.values())[i])
    return conn.execute(selection)

def update(table, checkVals, newVals):
    """Updates values in a row in a table.

    Params:
        table (sqlalchemy.Table): The table to update a row from.

        checkVals (dict): Values to find a row for.

        newVals (dict): Values to update in that row.
    Return value: None or sqlalchemy.ResultProxy object.

    Throws an error if the row doesn't exist."""
    fetched = fetch(table, checkVals)
    if not fetched:
        raise Exception('Row not found.')
    upd = table.update()
    for i, _ in enumerate(checkVals):
        upd = upd.where(table.c[list(checkVals.keys())[i]] == list(checkVals.values())[i])

    for i, _ in enumerate(newVals):
        upd = upd.values({table.c[list(newVals.keys())[i]]: list(newVals.values())[i]})
    return conn.execute(upd)
    
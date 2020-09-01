# pylint: disable=unused-variable
import random, ast, discord
from constants import db
from tables import tags, server_config

names = ['eval']
owner_only = True
no_docs = True
reqargs = ['args', 'msg', 'client', 'g', 'c', 'm']

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

async def run(**env):
    for _, a in enumerate(env):
        globals().update({a: env.get(a)})

    if not len(args) > 0:
        return await c.send('You must include code to eval!')

    # the following code is modified from
    # https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9. go check that one out
    try:
        fn_name = '_eval_expr'

        cmd = ' '.join(args).strip('` ').replace('“', '"')\
        .replace('”', '"') # for mobile smart quotes

        emb = discord.Embed()
        emb.add_field(name='Eval', value=f'```py\n{cmd}```', inline=False)
        emb.color = random.randint(0, 16777215)

        # add a layer of indentation
        cmd = '\n'.join(f'    {i}' for i in cmd.splitlines())

        # wrap in async def body
        body = f'async def {fn_name}():\n{cmd}'

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)
        eenv = env
        eenv.update({
            'db': db,
            'tags': tags,
            'server_config': server_config
        })
        # eval the code
        exec(compile(parsed, filename='<ast>', mode='exec'), eenv)

        result = (await eval(f'{fn_name}()', env))
        await c.send(embed=emb.add_field(name='Returns', value=f'```py\n{result}```', inline=False))
    except Exception as err:
        emb.color = discord.Colour.red()
        await c.send(embed=emb.add_field(name='Error', value=f'```py\n{err}```', inline=False))

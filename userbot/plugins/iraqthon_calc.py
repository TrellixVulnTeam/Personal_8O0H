#Hello. These files are all private to Source Iraq Thun. 
#In short, there are files registered for Source, another group. 
#You do not need to write a file from the beginning for the sake of rights, 
#and there are complete files. Thank you for installing Iraq Thun. 
#Our channel is here: https://t.me/Bomber
import io
import sys
import asyncio
import inspect
import traceback
from .. import CMD_HELP
from telethon import events, errors, functions, types
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

@borg.on(admin_cmd(pattern="calc (.*)"))
async def _(car):
    cmd = car.text.split(" ", maxsplit=1)[1]
    event = await edit_or_reply(car ,"Calculating ...")
    reply_to_id = car.message.id
    if event.reply_to_msg_id:
        reply_to_id = car.reply_to_msg_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    san = f"print({cmd})"
    try:
        await aexec(san, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Sorry I cant find result for the given equation"
    final_output = "**EQUATION**: `{}` \n\n **SOLUTION**: \n`{}` \n".format(cmd, evaluation)
    await event.edit(final_output)

async def aexec(code, event):
    exec(
        f'async def __aexec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](event)

CMD_HELP.update({"calc": 
      "**SYNTAX : **`.calc` your equation :\
      \n**USAGE : **solves the given maths equation by bodmass rule. "
}) 

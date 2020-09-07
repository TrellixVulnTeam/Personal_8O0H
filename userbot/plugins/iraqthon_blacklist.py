#Hello. These files are all private to Source Iraq Thun. 
#In short, there are files registered for Source, another group. 
#You do not need to write a file from the beginning for the sake of rights, 
#and there are complete files. Thank you for installing Iraq Thun. 
#Our channel is here: https://t.me/Bomber

"""Filters
Available Commands:
.addblacklist
.listblacklist
.rmblacklist"""

import re
import asyncio
from .. import CMD_HELP
from telethon import events, utils
from telethon.tl import types, functions
import userbot.plugins.sql_helper.blacklist_sql as sql
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

@borg.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    # TODO: exempt admins from locks
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception as e:
                await event.reply("I do not have DELETE permission in this chat")
                sql.rm_from_blacklist(event.chat_id, snip.lower())
            break

@borg.on(admin_cmd(pattern="addblacklist ((.|\n)*)"))
@borg.on(sudo_cmd(pattern="addblacklist ((.|\n)*)",allow_sudo = True))
async def on_add_black_list(event):
    text = event.pattern_match.group(1)
    to_blacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await edit_or_reply(event ,"Added {} triggers to the blacklist in the current chat".format(len(to_blacklist)))

@borg.on(admin_cmd(pattern="rmblacklist ((.|\n)*)"))
@borg.on(sudo_cmd(pattern="rmblacklist ((.|\n)*)",allow_sudo = True))
async def on_delete_blacklist(event):
    text = event.pattern_match.group(1)
    to_unblacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(event.chat_id, trigger.lower()):
            successful += 1
    await edit_or_reply(event ,f"Removed {successful} / {len(to_unblacklist)} from the blacklist")
    
@borg.on(admin_cmd(pattern="listblacklist$"))
@borg.on(sudo_cmd(pattern="listblacklist$",allow_sudo = True))
async def on_view_blacklist(event):
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "Blacklists in the Current Chat:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "No BlackLists. Start Saving using `.addblacklist`"
    if len(OUT_STR) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="BlackLists in the Current Chat",
                reply_to=event
            )
            await event.delete()
    else:
        await edit_or_reply(event , OUT_STR)
    
CMD_HELP.update({
    "blacklist":
    "**SYNTAX : **`.addblacklist` <word/words>\
    \n**USAGE : **The given word or words will be added to blacklist in that specific chat if any user sends then the message deletes.\
    \n\n**SYNTAX : **`.rmblacklist` <word/words>\
    \n**USAGE : **The given word or words will be removed from blacklist in that specific chat\
    \n\n**SYNTAX : **`.listblacklist`\
    \n**USAGE : **Shows you the list of blacklist words in that specific chat\
    \n\n**NOTE : 8**f you are adding more than one word at time via this then remember that new word must be given in new line that is not [hi hello] . it must be as\
    [hi \n hello]"
})
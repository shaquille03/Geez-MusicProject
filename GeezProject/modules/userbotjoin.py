# Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from GeezProject.helpers.decorators import authorized_users_only, errors
from GeezProject.services.callsmusic.callsmusic import client as USER
from GeezProject.config import SUDO_USERS

@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Tambahkan saya sebagai admin grup Anda terlebih dahulu</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "GeezProject"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} sudah ada di obrolan Anda</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>⛑ Flood Wait Error ⛑\n{user.first_name} tidak dapat bergabung dengan grup Anda karena banyaknya permintaan bergabung untuk userbot! Pastikan pengguna tidak dibanned dalam grup."
            "\n\nAtau tambahkan Assistant bot secara manual ke Grup Anda dan coba lagi.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} berhasil bergabung dengan obrolan Anda</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>Pengguna tidak dapat meninggalkan grup Anda! Mungkin menunggu floodwaits."
            "\n\nAtau keluarkan saya secara manual dari ke Grup Anda</b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("**Asisten Meninggalkan semua obrolan**")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
    
    
@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Apakah obrolan terhubung?")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Tambahkan saya sebagai admin saluran Anda terlebih dahulu</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "GeezProject"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} sudah ada di channel anda</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>⛑ Flood Wait Error ⛑\n{user.first_name} tidak dapat bergabung dengan grup Anda karena banyaknya permintaan bergabung untuk userbot! Pastikan pengguna tidak dibanned dalam grup."
            "\n\nAtau tambahkan Assistant bot secara manual ke Grup Anda dan coba lagi.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} sudah bergabung dengan obrolan Anda</b>",
    )
    

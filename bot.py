import os
import time
import asyncio
import datetime
import re
from base64 import standard_b64encode, standard_b64decode
#from config import Config
#from keep_alive import keep_alive
from pyrogram.errors import FloodWait
from pyrogram import Client,__version__, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
Client = Client(
    "multibots",
    bot_token = "7422590172:AAGtz-B1EW6WChkk37kTqWRlE6w8isFcXl4",
    api_id = 18860540,
    api_hash = "22dd2ad1706199438ab3474e85c9afab"
    )


async def get_file_size(msg:Message):
    if msg.video:
        size = msg.video.file_size
    elif msg.document:
        size = msg.document.file_size
    elif msg.audio:
        size = msg.audio.file_size
    else:
        size = None
    if size is not None:
        if size < 1024:
            file_size = f"[{size} B]"
        elif size < (1024**2):
            file_size = f"[{str(round(size/1024, 2))} KiB] "
        elif size < (1024**3):
            file_size = f"[{str(round(size/(1024**2), 2))} MiB] "
        elif size < (1024**4):
            file_size = f"[{str(round(size/(1024**3), 2))} GiB] "
    else:
        file_size = ""
    return file_size



def str_to_b64(__str: str) -> str:
    str_bytes = __str.encode('ascii')
    bytes_b64 = standard_b64encode(str_bytes)
    b64 = bytes_b64.decode('ascii')
    return b64


def b64_to_str(b64: str) -> str:
    bytes_b64 = b64.encode('ascii')
    bytes_str = standard_b64decode(bytes_b64)
    __str = bytes_str.decode('ascii')
    return __str



@Client.on_message(filters.command("start") & filters.private|filters.group)
async def star(bot,update):
    #msg = await bot.get_messages(-1001953021632,38)
    #print(msg)
    # m = getattr(msg,msg.media.value,None)
    # print(m.file_id)
    # print(type(msg.media))
    # print(m.thumbs[0].file_id)
    # print(type(msg.document))
    #await update.reply_text(msg)
    # text = await bot.send_message(update.from_user.id, "counting")
    # empty=0
    # total = 0
    # document = 0
    # video = 0
    # total_messages = (range(1,11443))
    # try:
        
    #     for i in range(1371-1 ,len(total_messages), 200):
    #         channel_posts = AsyncIter(await bot.get_messages(-1001777759879, total_messages[i:i+200]))
    #         async for message in channel_posts:
    #             if message.video:
    #                 video+=1
    #                 total+=1
    #             elif message.document:
    #                 document+=1
    #                 total+=1
    #             else:
    #                 empty+=1
                
    #             if total % 10 == 0:
    #                 msg = f"Batch forwarding in Process !\n\nTotal: {total}\nvideo: {video}\ndocument: {document}\nEmpty :{empty}"
    #                 await text.edit((msg))
    # except Exception as e:
    #     print(str(type(e)),(e))
    # finally:
    #     msg = f"Batch Forwarding Completed!\n\nTotal: `{total}`\nvideo: `{video}`\ndocument: `{document}`\nEmpty: `{empty}`"
    #     await text.edit(msg)    
    await update.reply_text("bot_is_live",quote=True,reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('+ADD ME TO YOUR GROUPS', callback_data="check")]]))
@Client.on_callback_query()
async def button(bot:Client, cmd:CallbackQuery):
    cb_data = cmd.data
    if "check" in cb_data:
        await cmd.answer(url=f"https://t.me/dc4botz01_bot?start=send_")
        #await chiku(bot,cmd.message)


async def chiku(bot:Client,msg:Message):
    await msg.edit("done")
    return print(msg,msg.reply_to_message)

@Client.on_message(filters.command("raw") & filters.private|filters.group)
async def raw(bot,update):
    if not update.reply_to_message:
        return await update.reply_text("reply any message to get raw detail of that")
    try:
        print(update)
    except Exception as e:
        await update.reply_text(e)

@Client.on_message(filters.private & filters.command("batch"))
async def batch(bot,update):
    if not update.reply_to_message:
        return await update.reply_text("reply to formate like --- from_channel_id(without-100)|photo_send_channel(with -100)|start_msg_id|to_msg_id")

    try:
        FROM_CHANNEL = int(update.reply_to_message.text.split("|")[0])
    except ValueError:
        return await update.reply_text("don't send me text in place of channel_id or group_id\nsend me only channel id or group id in intiger like- -1007725455")
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting channel or group id error - {e}")
    
    try:
        photo_send_channel = int(update.reply_to_message.text.split("|")[1])
    except ValueError:
        return await update.reply_text("don't send me text in place of channel_id or group_id\nsend me only channel id or group id in intiger like- -1007725455")
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting channel or group id error - {e}")
    
    
    
    try:
        FROM_MSG_ID = int(update.reply_to_message.text.split("|")[2])
    except ValueError:
        return await update.reply_text("don't send me text in place of mesaage_id \nsend me only mesaage_id in intiger like - 76")
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting FROM_MSG_ID error - {e}")

    try:
        TO_MSG_ID = int(update.reply_to_message.text.split("|")[3])
    except ValueError:
        return await update.reply_text("don't send me text in place of mesaage_id \nsend me only mesaage_id in intiger like - 76")
    except Exception as e:
        return  await update.reply_text(f"somthing went wrong to getting TO_MSG_ID error - {e}")

    try:
        start_time = datetime.datetime.now()
        txt = await update.reply_text(text="Batch File saving Started!")
        count = 0
        success = 0
        total = 0
        #text_msg_edited = 0
        vid_doc_aud_msg = 0
        unknown_msg_type = {'total_msg':0,'msg_ids':[]}
        empty = 0
        total_messages = (range(1,TO_MSG_ID))
        thumb_id = ""
        default_thumbs = "AgACAgEAAxkBAAMdZ61UvEL1el8goDjtZPrPo0OC8zsAAk2wMRsoQnFFuDpuOm0RYgsACAEAAwIAA3MABx4E"
        
        add_detail = ""
        
        
        for i in range(FROM_MSG_ID-1 ,len(total_messages), 200):
            channel_posts = AsyncIter(await bot.get_messages(int(f'-100{FROM_CHANNEL}'), total_messages[i:i+200]))
            async for message in channel_posts:
                msg = f"batch editing in process!\ntotal : {total}\nunknown_msg_type : {unknown_msg_type}\nempty : {empty}\nvid_doc_aud_msg : {vid_doc_aud_msg}\nsuccess : {success}"
                try:
                    await txt.edit(msg)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await txt.edit(msg)
                    
                except Exception as e:
                    pass
                    #return await bot.send_message(update.from_user.id,f"problem\n{e}\n{str(type(e))}")
                    
                    
                message_ids = []
                media_caption = ""
                if message.empty or message.service:
                    empty+=1
                    total+=1
                    continue
                elif message.video or message.document or message.audio:
                    vid_doc_aud_msg+=1
                    total+=1
                    continue
                elif (message.text) and ('BaTCh_LInK' or 'SiNGle_LInk' in message.text):
                    
                    
                    
                    if 'SiNGle_LInk' in message.text:
                        try:
                            next_msg = await bot.get_messages(int(f'-100{FROM_CHANNEL}'),message.id+1)
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            next_msg = await bot.get_messages(int(f'-100{FROM_CHANNEL}'),message.id+1)
                        except Exception as e:
                            return await bot.send_message(update.from_user.id,f"problem during get next_msg\n{e}")
                        if (not next_msg.text) or (next_msg.video or next_msg.document or next_msg.audio):
                            return await bot.send_message(update.from_user.id,f"there is not link message after single_link message\nplz adjust all mesaages according to given formate")
                        if next_msg.empty or next_msg.service:
                            return await bot.send_message(update.from_user.id,f"there is empty or service type message after immediate single_link message\nplz adjust all mesaages according to given formate ")
                        
                        if (next_msg.text) and (not "Open Link" in next_msg.text):
                            return await bot.send_message(update.from_user.id,f"there is not private file link message after single_link message\nplz adjust all mesaages according to given formate")
                        try:
                            
                            mesg = await bot.get_messages(int(f'-100{FROM_CHANNEL}'),message.id-1)
                        except FloodWait as e:
                            await asyncio.sleep(e.value) 
                            mesg = await bot.get_messages(int(f'-100{FROM_CHANNEL}'),message.id-1)
                        except Exception as e:
                            return await bot.send_message(update.from_user.id,f"problem during get before_100_msgs\n{e}")
                    
                        if mesg.video or mesg.document or mesg.audio:
                            before_100_mesg2 = AsyncIter(await bot.get_messages(int(f'-100{FROM_CHANNEL}'),range(mesg.id-1,mesg.id-101,-1)))
                            async for mesg2 in before_100_mesg2:
                                if mesg2.video or mesg2.document or mesg2.audio:
                                    return await bot.send_message(update.from_user.id,f"video/document/audio found\nmessage don't  give in correct sequence in FROM_CHANNEL\nmessage_id:{message.id}")
                                
                                elif (mesg2.text) and ('BATCH_SAVE' or 'PRIVATE_FILE' in mesg2.text):
                                    
                                    message_ids.append(mesg.id)
                                    media_size = await get_file_size(mesg)
                                    media_caption+=f"**👉{mesg.caption} {media_size}**" if mesg.caption else ""
                                    if mesg.video:
                                        thumb_id+=mesg.video.thumbs[0].file_id
                                    elif mesg.document and mesg.document.thumbs:
                                        thumb_id+=mesg.document.thumbs[0].file_id
                                    elif mesg.audio and mesg.audio.thumbs:
                                        thumb_id+=mesg.audio.thumbs[0].file_id
                                    else:
                                        thumb_id = default_thumbs
                                    break
                                elif mesg2.empty or mesg2.service:
                                    
                                    continue
                                else:
                                    return await bot.send_message(update.from_user.id,f"mess don't  give in correct sequence in FROM_CHANNEL\nmessage_id:{message.id}")
                        elif mesg.empty or mesg.service:
                            return  await bot.send_message(update.from_user.id,f"mesg is empty before single link\nmessage_id:{message.id}")
                        
                        else:
                            return await bot.send_message(update.from_user.id,f"messo don't  give in correct sequence in FROM_CHANNEL\nmessage_id:{message.id}")
                        if len(message_ids)==0:
                            return await bot.send_message(update.from_user.id,f"message_ids list len is zero\n{message.id}")
                        elif len(message_ids)==1:
                            try:
                                await txt.edit("Editing Link....")
                                try:
                                    
                                    await bot.edit_message_text(int(f'-100{FROM_CHANNEL}'),message.id,f"#SiNGle_LInk|{message_ids[0]}")
                                    
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                    await bot.edit_message_text(int(f'-100{FROM_CHANNEL}'),message.id,f"#SiNGle_LInk|{message_ids[0]}")
                                    
                                try:
                                    await bot.edit_message_text(int(f'-100{FROM_CHANNEL}'),message.id+1,f"#PRIVATE_FILE:\n\nGot File Link!\n\nOpen Link - https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}\n\nwithout shorted Link - https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}")
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                    await bot.edit_message_text(int(f'-100{FROM_CHANNEL}'),message.id+1,f"#PRIVATE_FILE:\n\nGot File Link!\n\nOpen Link - https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}\n\nwithout shorted Link - https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}")
                            except Exception as e:
                                return await bot.send_message(update.from_user.id,f"something went wrong during edit single_message_text\n{e}")
                            
                            try:
                                if count>=90:
                                    await txt.edit("sleeping for 30 min.......")
                                    await asyncio.sleep(1800)
                                    count=0
                                await txt.edit("sending caption with photo to photo channel")
                                thumb_path = await bot.download_media(thumb_id)
                                media_captions=f"Here is the Permanent Link of your Content: <a href=https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}>Download Link</a>\n\nJust Click on download to get your Content!\n\nyour Content name are:👇\n\n{media_caption}\n\n{add_detail}"
                                if len(media_captions)>1024:
                                    await txt.edit("**media caption is too long (more than 1024 character)\nAdding only 1024 character caption to your media photo...**")
                                    media_captions = media_captions[0:1020]
                                await bot.send_photo(int(photo_send_channel),thumb_path,media_captions)
                                thumb_id=""
                                success+=1
                                count+=1
                            except Exception as e:
                                return await bot.send_message(update.from_user.id,f"something went wrong during send photo with media caption in channel\n{e}")
                        
                        
                        else:
                            return await bot.send_message(update.from_user.id,"something went wrong!")
                    
                    elif 'BaTCh_LInK' in message.text:
                        try:
                            next_msg = await bot.get_messages(int(f'-100{FROM_CHANNEL}'),message.id+1)
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            next_msg = await bot.get_messages(int(f'-100{FROM_CHANNEL}'),message.id+1)
                        except Exception as e:
                            return await bot.send_message(update.from_user.id,f"problem during get next_msg\n{e}")
                        if (not next_msg.text) or (next_msg.video or next_msg.document or next_msg.audio):
                            return await bot.send_message(update.from_user.id,f"there is not link message after batch_link message\nplz adjust all mesaages according to given formate")
                        if next_msg.empty or next_msg.service:
                            return await bot.send_message(update.from_user.id,f"there is empty or service type message after immediate single_link message\nplz adjust all mesaages according to given formate ")
                        
                        if (next_msg.text) and (not "Open Link" in next_msg.text):
                            return await bot.send_message(update.from_user.id,f"there is not batch file link message after batch_link message\nplz adjust all mesaages according to given formate")
                        
                        before_10_batch_mesg = AsyncIter(await bot.get_messages(int(f'-100{FROM_CHANNEL}'),range(message.id-1,message.id-11,-1)))#only can save 10 msg in batch
                        async for messg in before_10_batch_mesg:
                            if messg.service or messg.empty:
                                continue
                            elif messg.video:
                                media_caption+=f"**👉{messg.caption} {await get_file_size(messg)}**\n\n" if messg.caption else "\n"
                                message_ids.append(messg.id)
                                if not thumb_id:
                                    if messg.video.thumbs:
                                        thumb_id+=f"{messg.video.thumbs[0].file_id}"
                                continue
                            elif messg.document:
                                media_caption+=f"**👉{messg.caption} {get_file_size(messg)}**\n\n" if messg.caption else "\n"
                                message_ids.append(messg.id)
                                if not thumb_id:
                                    if messg.document.thumbs:
                                        thumb_id+=f"{messg.document.thumbs[0].file_id}"
                                continue
                            elif messg.audio:
                                media_caption+=f"**👉{messg.caption} {get_file_size(messg)}**\n\n" if messg.caption else "\n"
                                message_ids.append(messg.id)
                                if not thumb_id:
                                    if messg.audio.thumbs:
                                        thumb_id+=f"{messg.audio.thumbs[0].file_id}"
                            
                                continue
                            elif (messg.text) and ("Open Link" in messg.text):
                                break
                            
                            else:
                                return await bot.send_message(update.from_user.id,f"there are another type of message rather than video,document,audio between given batch links")
                        if len(message_ids)>1:
                            try:
                                await txt.edit("Editing Batch Link")
                                try:
                                    message_ids = sorted(message_ids)
                                    await bot.edit_message_text(int(f'-100{FROM_CHANNEL}'),message.id,f"#BaTCh_LInK|{' '.join(str(x) for x in message_ids)}")
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                    await bot.edit_message_text(int(f'-100{FROM_CHANNEL}'),message.id,f"#BaTCh_LInK|{' '.join(str(x) for x in message_ids)}")
                            
                                try:
                                    await bot.edit_message_text(int(f'-100{FROM_CHANNEL}'),message.id+1,f"#BATCH_SAVE:\n\nGot Batch Link!\n\nOpen Link - https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}\n\nwithout shorted Link - https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}")
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                    await bot.edit_message_text(int(f'-100{FROM_CHANNEL}'),message.id+1,f"#BATCH_SAVE:\n\nGot Batch Link!\n\nOpen Link - https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}\n\nwithout shorted Link - https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}")
                            except Exception as e:
                                return await bot.send_message(update.from_user.id,f"something went wrong during edit single_message_text\n{e}")
                            try:
                                if count>=90:
                                    await txt.edit("sleeping for 30 min.......")
                                    await asyncio.sleep(1800)
                                    count=0
                                await txt.edit("sending caption with photo to photo channel")
                                if not thumb_id:
                                    thumb_id = default_thumbs
                                thumb_path = await bot.download_media(thumb_id)
                                media_captions=f"Here is the Permanent Link of your Content: <a href=https://t.me/moviexstore_bot?start=store_{FROM_CHANNEL}_{str_to_b64(str(message.id))}>Download Link</a>\n\nJust Click on download to get your Content!\n\nyour Content name are:👇\n\n{media_caption}\n\n{add_detail}"
                                if len(media_captions)>1024:
                                    await txt.edit("**media caption is too long (more than 1024 character)\nAdding only 1024 character caption to your media photo...**")
                                    media_captions = media_captions[0:1020]
                                await bot.send_photo(int(photo_send_channel),thumb_path,media_captions)
                                thumb_id=""
                                success+=1
                                count+=1
                            except Exception as e:
                                return await bot.send_message(update.from_user.id,f"something went wrong during send photo with media caption in channel\n{e}")
                    
                                
                                
                                
                                
                        else:
                            return await bot.send_message(update.from_user.id,f"len(message_ids) is less than or equal to  1")
                else:
                    
                    unknown_msg_type['total_msg']+1
                    unknown_msg_type['msg_ids'].append(message.id)
                    continue
                # if total % 5 ==0:
                #     msg = f"batch editing in process!\ntotal : {total}\nunknown_msg_type : {unknown_msg_type}\nempty : {empty}\nvid_doc_aud_msg : {vid_doc_aud_msg}\nsuccess : {success}"
                    
                #     try:
                #         await txt.edit(msg)
                #     except FloodWait as e:
                #         await asyncio.sleep(e.value)
                #         await txt.edit(msg)
                    
                #     except Exception as e:
                #         return await bot.send_message(update.from_user.id,f"problem editing txt while totaling\n{e}")
                
    
    
    except Exception as e:
        await bot.send_message(update.from_user.id,f"i don't  know whats is wrong\n{e}")


    finally:
        end_time = datetime.datetime.now()
        t = end_time - start_time
        time_taken = str(datetime.timedelta(seconds=t.seconds))
        msg = f"batch editing is complete!\nTime taken : {time_taken}\n\ntotal : {total}\nunknown_msg_type : {unknown_msg_type}\nempty : {empty}\nvid_doc_aud_msg : {vid_doc_aud_msg}\nsuccess : {success}"
        await txt.edit(msg)


@Client.on_message(filters.private & filters.command("forward"))
async def forward(bot:Client, update:Message):
    if not update.reply_to_message:
        await update.reply_text("**send me channels or group ids wuth -100 and message id from where u want to start forward\nchannels ids and messaage id must be separated by |\nexample - \nfrom_channel_id|start_from_message_id|to_channel_id**")
        return
    try:
        FROM_CHANNEL = int(update.reply_to_message.text.split("|")[0])
        START_FROM = int(update.reply_to_message.text.split("|")[1])
        TO_CHANNEL = int(update.reply_to_message.text.split("|")[2])
    
        try:
            start_time = datetime.datetime.now()
            txt = await update.reply_text(text="Forward Started!")
            text = await bot.send_message(FROM_CHANNEL, ".")
            last_msg_id = text.id
            await text.delete()
            success = 0
            fail = 0
            total = 0
            empty=0
            total_messages = (range(1,last_msg_id))
            for i in range(START_FROM-1 ,len(total_messages), 200):
                channel_posts = AsyncIter(await bot.get_messages(FROM_CHANNEL, total_messages[i:i+200]))
                async for message in channel_posts:
                    if not message.service or message.empty:
                        try:
                            await message.copy(TO_CHANNEL)
                            success+=1
                        except FloodWait as e:
                            msgs = await bot.send_message(update.from_user.id,f"sleeping for {e.value} sec")
                            await asyncio.sleep(e.value)
                            await msgs.delete()
                            await message.copy(TO_CHANNEL)
                            success+=1
                        except Exception as e:
                            return await bot.send_message(update.from_user.id,f"this msg_id {message.id} give error {e}")
                    # if message.video or message.audio or message.document or message.photo:
                    #     try:
                    #         await message.copy(TO_CHANNEL)
                    #         success+=1
                    #         await asyncio.sleep(4)
                    #     except FloodWait as e:
                    #         msgs = await bot.send_message(update.from_user.id,f"sleeping for {e.value} sec")
                    #         await asyncio.sleep(e.value)
                    #         await msgs.delete()
                    #         await message.copy(TO_CHANNEL)
                    #         success+=1
                    #     except Exception as e:
                    #         fail+=1
                    #         await bot.send_message(update.from_user.id,f"this msg_id {message.id} give error {e}")
                    #         await asyncio.sleep(4)
                    else:
                        empty+=1
                    total+=1
                    
                    if total % 5 == 0:
                        msg = f"Batch forwarding in Process !\n\nTotal: {total}\nSuccess: {success}\nFailed: {fail}\nEmpty: {empty}"
                        await txt.edit((msg))
                    #await asyncio.sleep(2)
        
        except FloodWait as e:
            await bot.send_message(update.from_user.id,f"sleeping for {e.value} sec")
            await asyncio.sleep(e.value)
    
    except ValueError:
        return await update.reply_text("don't send me text\nsend me only channel ids and message_id in intiger like --- -1007725455|34|-10037783")
    
    except Exception as e:
        return await update.reply_text(f"{e}")
    
    finally:
        end_time = datetime.datetime.now()
        await asyncio.sleep(4)
        t = end_time - start_time
        time_taken = str(datetime.timedelta(seconds=t.seconds))
        msg = f"Batch Forwarding Completed!\n\nTime Taken - `{time_taken}`\n\nTotal: `{total}`\nSuccess: `{success}`\nFailed: `{fail}`\nEmpty: `{empty}`"
        await txt.edit(msg)    





@Client.on_message(filters.private & filters.command("delete_all"))
async def delete_all(bot, update):
    if not update.reply_to_message:
        return await update.reply_text("send me channel or group id and message_id from where you want to delete all messaage\nchannel or group id must be separatedby |\nexample - \nchannel or group id|message_id")
    try:
        FROM_CHANNEL = int(update.reply_to_message.text.split("|")[0])
        START_FROM = int(update.reply_to_message.text.split("|")[1])
        try:
            start_time = datetime.datetime.now()
            txt = await update.reply_text(text="delete Started!")
            text = await bot.send_message(FROM_CHANNEL, ".")
            last_msg_id = text.id
            await text.delete()
            success = 0
            fail = 0
            total = 0
            empty=0
            total_messages = (range(1,last_msg_id))
            for i in range(START_FROM-1 ,len(total_messages), 200):
                channel_posts = AsyncIter(await bot.get_messages(FROM_CHANNEL, total_messages[i:i+200]))
                async for message in channel_posts:
                    if not message.empty or message.service:
                        try:
                            await bot.delete_messages(FROM_CHANNEL,message.id,revoke=True)
                            #await message.delete(True)
                            success+=1
                            #await asyncio.sleep(1)
                        except FloodWait as e:
                            msg = await bot.send_message(update.from_user.id,f"sleeping for {e.value} sec")
                            await asyncio.sleep(e.value)
                            await message.delete()
                            success+=1
                            await msg.delete()
                        except Exception as e:
                            fail+=1
                            await bot.send_message(update.from_user.id,f"this msg_id {message.id} give error {e}")
                            await asyncio.sleep(1)
                    else:
                        empty+=1
                    total+=1
                    
                    if total % 5 == 0:
                        msg = f"Batch deleteing in Process !\n\nTotal: {total}\nSuccess: {success}\nFailed: {fail}\nEmpty: {empty}"
                        await txt.edit((msg))
                    #await asyncio.sleep(2)
        
        except FloodWait as e:
            await bot.send_message(update.from_user.id,f"sleeping for {e.value} sec")
            await asyncio.sleep(e.value)
    
    except ValueError:
        await update.reply_text("don't send me text\nsend me only channel id or group id in intiger like --- -1007725455")
    
    except Exception as e:
        await txt.reply_text(f"{e}")
    
    finally:
        end_time = datetime.datetime.now()
        await asyncio.sleep(4)
        t = end_time - start_time
        time_taken = str(datetime.timedelta(seconds=t.seconds))
        msg = f"Batch deleteing Completed!\n\nTime Taken - `{time_taken}`\n\nTotal: `{total}`\nSuccess: `{success}`\nFailed: `{fail}`\nEmpty: `{empty}`"
        await txt.edit(msg)    





@Client.on_message(filters.private  & filters.command("edit_caption"))
async def edit_caption(bot,update):
    if not update.reply_to_message:
        return await update.reply_text("if you want edit caption in batch of any any channel or group message the ssend me text in given formate -\nchannel_id or group_id in which you want to edit caption|message_id where you want to start|word that you want to remove from caption(multiple word must be separated by ,)|word that you want to add in place of remove word(multiple word must be separatd by ,\nlike- -10074884|56|bot1,bot2|botz1,botz2\nIn upper example bot1 word is replace by botz1 and bot2 by botz2 if you want bot1 word remove with empty word then write '' in replace of botz1\nso if you understand this example then send me text like that")
    
    try:
        CHANNEL_ID = int(update.reply_to_message.text.split("|")[0])
    except ValueError:
        return await update.reply_text("don't send me text in place of channel_id or group_id\nsend me only channel id or group id in intiger like- -1007725455")
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting channel or group id error - {e}")
    
    try:
        MSG_ID = int(update.reply_to_message.text.split("|")[1])
    except ValueError:
        return await update.reply_text("don't send me text in place of mesaage_id \nsend me only mesaage_id in intiger like - 76")
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting mesaage_id error - {e}")
    
    
    try:
        REMOVE_WORD_LIST = update.reply_to_message.text.split("|")[2].split(',')
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting remove words error - {e}")
    
    try:
        REPLACE_WORD_LIST = update.reply_to_message.text.split("|")[3].split(',')
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting replace words error - {e}")
    if len(REPLACE_WORD_LIST)!=len(REMOVE_WORD_LIST):
        for i in range(0,len(REMOVE_WORD_LIST)-len(REPLACE_WORD_LIST)):
            REPLACE_WORD_LIST.append('')
    
    try:
        
        start_time = datetime.datetime.now()
        txt = await update.reply_text(text="editing Started!")
        text = await bot.send_message(CHANNEL_ID, ".")
        last_msg_id = text.id
        await text.delete()
        success = 0
        fail_msg_id = []
        total = 0
        msg_have_no_caption=0
        failed_msg=0
        total_messages = (range(1,last_msg_id))
        try:
            for i in range(MSG_ID-1 ,len(total_messages), 200):
                channel_posts = AsyncIter(await bot.get_messages(CHANNEL_ID, total_messages[i:i+200]))
                async for message in channel_posts:
                    if not message.caption:
                        try:
                            msg_have_no_caption+=1
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                    if message.caption:
                        cap = message.caption.html
                        caps=message.caption
                        cap_comp = message.caption.html
                        #print(cap)
                        try:
                            for rm , rep  in zip(REMOVE_WORD_LIST,REPLACE_WORD_LIST):
                                new_cap = re.sub(rm,rep,cap)
                                cap=new_cap
                                #print(new_cap)
                            if re.search("@seaofallmovies", caps):
                                pass
                            else:
                                cap = cap + "\n\n💥Join Us Oɴ Tᴇʟᴇɢʀᴀᴍ💥 ❤️ @seaofallmovies❤️"
                            # if "💥Join Us Oɴ Tᴇʟᴇɢʀᴀᴍ💥 ❤️ @seaofallmovies❤️" not in caps:
                            #     cap = cap + "\n\n💥Join Us Oɴ Tᴇʟᴇɢʀᴀᴍ💥 ❤️ @seaofallmovies❤️"
                            if cap!=cap_comp:
                                await bot.edit_message_caption(CHANNEL_ID,message.id,cap)
                            success += 1
                            await asyncio.sleep(2)
                        except FloodWait as e:
                            await bot.send_message(update.from_user.id,f"sleeping for {e.value} sec")
                            await asyncio.sleep(e.value)
                            await bot.edit_message_caption(CHANNEL_ID,message.id,cap)
                            success += 1
                        except Exception as e:
                            failed_msg+=1 
                            fail_msg_id.append(message.id)
                            await bot.send_message(update.from_user.id,f"message_id - {message.id} can't be edit\ngiving error ---- {e}")
                            await asyncio.sleep(3)
                    total+=1
                    if total % 5 == 0:
                        msg = f"Batch editing in Process !\n\nTotal: {total}\nSuccess: {success}\nFailed: {failed_msg}\nMsg_Have_No_Caption: {msg_have_no_caption}\nFail_Msg_Ids: {fail_msg_id}"
                        await txt.edit(msg)
        except Exception as e:
            await bot.send_message(update.from_user.id,f"error during editing caption Error- {e}")
            return
    except Exception as e:
            await bot.send_message(update.from_user.id,f"error during editing caption Error- {e}")
            return


@Client.on_message(filters.private  & filters.command("edit_reply_markup_button"))
async def edit_reply_markup_button(bot,update):
    if not update.reply_to_message:
        return await update.reply_text("if you want edit reply markup button in batch of any channel or group message the send me text in given formate -\nchannel_id or group_id in which you want to edit caption|message_id where you want to start\nlike -1003774|45")
    
    try:
        CHANNEL_ID = int(update.reply_to_message.text.split("|")[0])
    except ValueError:
        return await update.reply_text("don't send me text in place of channel_id or group_id\nsend me only channel id or group id in intiger like- -1007725455")
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting channel or group id error - {e}")
    
    try:
        MSG_ID = int(update.reply_to_message.text.split("|")[1])
    except ValueError:
        return await update.reply_text("don't send me text in place of mesaage_id \nsend me only mesaage_id in intiger like - 76")
    except Exception as e:
        return await update.reply_text(f"somthing went wrong to getting mesaage_id error - {e}")
    
    
    try:
        
        start_time = datetime.datetime.now()
        txt = await update.reply_text(text="editing Started!")
        text = await bot.send_message(CHANNEL_ID, ".")
        last_msg_id = text.id
        await text.delete()
        success = 0
        fail_msg_id = []
        total = 0
        has_two_reply_makrup=0
        msg_have_no_reply_markup=0
        failed_msg=0
        total_messages = (range(1,last_msg_id))
        try:
            for i in range(MSG_ID-1 ,len(total_messages), 200):
                channel_posts = AsyncIter(await bot.get_messages(CHANNEL_ID, total_messages[i:i+200]))
                async for message in channel_posts:
                    if not message.reply_markup:
                        try:
                            msg_have_no_reply_markup+=1
                        except FloodWait as e:
                            await bot.send_message(update.from_user.id,f"sleeping for {e.value} sec")
                            await asyncio.sleep(e.value)
                    if message.reply_markup:
                        if "Got Batch Link" in message.text:
                            #print(message.reply_markup.inline_keyboard[0][0].url)
                            if (message.reply_markup.inline_keyboard) and (len(message.reply_markup.inline_keyboard)<2):
                                try:
                                    link =  message.reply_markup.inline_keyboard[0][0].url.split("?",1)
                                    link[1] = link[1].replace("storebot","storedb0")
                                    link = "?".join(link)
                                    await message.edit_text(f"{message.text}\n\nOpen Link - {link}")
                                    success += 1
                                    await asyncio.sleep(3)
                                except FloodWait as e:
                                    await bot.send_message(update.from_user.id,f"sleeping for {e.value} sec")
                                    await asyncio.sleep(e.value)
                                    await message.edit_message_reply_markup(CHANNEL_ID,message.id,InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=link)]]))
                                    success += 1
                                except Exception as e:
                                    failed_msg+=1 
                                    fail_msg_id.append(message.id)
                                    await bot.send_message(update.from_user.id,f"message_id - {message.id} can't be edit\ngiving error ---- {e}")
                                    await asyncio.sleep(3)
                            else:
                                if (message.reply_markup.inline_keyboard) and (len(message.reply_markup.inline_keyboard)>1):
                                    has_two_reply_makrup+=1
                    total+=1
                    if total % 5 == 0:
                        msg = f"Batch editing in Process !\n\nTotal: {total}\nSuccess: {success}\nFailed: {failed_msg}\nmsg_have_no_reply_markup: {msg_have_no_reply_markup}\nFail_Msg_Ids: {fail_msg_id}\nhas_two_reply_makrup: {has_two_reply_makrup}"
                        await txt.edit(msg)
        except Exception as e:
            await bot.send_message(update.from_user.id,f"error during editing caption Error- {e}")
            return
    except Exception as e:
            await bot.send_message(update.from_user.id,f"error during editing caption Error- {e}")
            return
    finally:
        end_time = datetime.datetime.now()
        await asyncio.sleep(4)
        t = end_time - start_time
        time_taken = str(datetime.timedelta(seconds=t.seconds))
        msg = f"Batch editing Completed!\n\nTime Taken - `{time_taken}`\n\nTotal: `{total}`\nSuccess: `{success}`\nFailed: `{failed_msg}`\nmsg_have_no_reply_markup: `{msg_have_no_reply_markup}`\nFail_Msg_Ids: `{fail_msg_id}`\nhas_two_reply_makrup: `{has_two_reply_makrup}`"
        await txt.edit(msg)    



class AsyncIter:    
    def __init__(self, items):    
        self.items = items    

    async def __aiter__(self):    
        for item in self.items:    
            yield item  

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration as e:
            raise StopAsyncIteration from e
#keep_alive()
Client.run()

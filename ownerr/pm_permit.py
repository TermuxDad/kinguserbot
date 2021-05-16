from kingbot import kingbot, setbot , vr, Adminsettings
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton , InlineQuery ,Message, CallbackQuery, InlineQueryResultPhoto, User
from pyrogram import filters 
import re
from sql_helper.permit import givepermit, checkpermit, blockuser, getwarns, allallowed, allblocked, inwarns
@kingbot.on_message(~filters.user(Adminsettings) & filters.private & ~filters.bot)
async def pm_chker(_ , message):
  if checkpermit(message.chat.id):
        return
  else:
    gw= await getwarns(message.chat.id)
    if isinstance(gw , str):
      sb= await setbot.get_me()
      un= sb.username
      result= kingbot.get_inline_bot_results(un , f"pmsg_{message.user.id}")
      mg = kingbot.send_inline_bot_result(message.chat.id , result.query_id , result.results[0].id)
      ow=await kingbot.get_me()
      use= await kingbot.get_users(message.user.id)
      keyboard= InlineKeyboardMarkup([  # First row
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "Approve",
                        callback_data=f"aprv_{message.user.id}"
                    ),
                    InlineKeyboardButton(  # Opens a web URL
                        "Decline",
                        callback_data=f"decine_{message.user.id}"
                    ),
                ])
      setbot.send_message(ow.id, f"{use.mention()} Has requested to contact you", reply_markup= keyboard )
    else:
      sb= await setbot.get_me()
      un= sb.username
      result= kingbot.get_inline_bot_results(un , f"pmsg_{message.user.id}")
      mg = kingbot.send_inline_bot_result(message.chat.id , result.query_id , result.results[0].id)
async def infilter(_,__, inline_query):
    if re.match(r"pmsg_", inline_query.query):
        return True

innfi = filters.create(infilter)
@setbot.on_inline_query(innfi & filters.user(Adminsettings))
async def pmsg_gen(_ , inline_query):
  st= inline_query.query
  id = int(st.split("_",1)[1])
  gww = await getwarns(id)
  await addwarns(id)
  keboard= InlineKeyboardMarkup(
                  [  [
                        InlineKeyboardButton(
                            "Request something",
                            callback_data= "re_q1"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Get help",
                            callback_data= "re_q2"
                        ),
                        InlineKeyboardButton(
                            "Spam or insult",
                            callback_data= "re_q3"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "You are a friend",
                            callback_data= "re_q4"
                        )
                    ]])
  if isinstance(gww, str):
    cptn= f"You are accessing Pm permit of king userbot\n My master is currently busy so choose one of the below options and don't spam\n You have only 1 warning"
  else:
    cptn=f"You are accessing Pm permit of king userbot\n My master is currently busy so choose one of the below options and don't spam\n You have only {gww} warning"
  await inline_query.answer(
        results=[
            InlineQueryResultPhoto(
                photo_url= "https://telegra.ph/file/7cb1a085a337c18fdfd42.jpg",
                title="pm",
                caption=cptn,
                reply_markup=keboard,
            ),
        ]
    )
async def incbq(_,__, cbq: CallbackQuery):
    if re.match(r"aprv", cbq.data):
        return True
    if re.match(r"decine", cbq.data):
        return True

inncbq = filters.create(incbq)
@setbot.on_callback_query(inncbq & filters.user(Adminsettings), group =3)
async def appblk(_ , cbq):
    dt=cbq.data
    mth= dt.split("_",1)[0]
    idd= int(dt.split("_",1)[1])
    if mth == "aprv":
      await givepermit(idd)
      await setbot.edit_inline_text(cbq.inline_message_id ,"The user has been approved")
      await kingbot.send_message(idd , "Welcome!! my master has remotely approved you🥳🥳🥳")
      cbq.answer()
      return
    if mtb == "decine":
       await blockuser(idd)
       await setbot.edit_inline_text(cbq.inline_message_id, "The user has been blocked")
       await kingbot.send_message(idd,"Sed!! My master decided to send you to hell☠️☠️")
       await kingbot.block_user(idd)
       cbq.answer()
       return
async def incq(_,__, cbq):
    if re.match(r"re_", cbq.data):
        return True

inncq= filters.create(incq)
@setbot.on_callback_query(inncq , group=3)
async def fny(_, cbq):
    idd= cbq.from_user
    mth= cbq.data
    if mth =="re_q1":
      await cbq.edit_inline_text(cbq.inline_message_id,"Your!! Request has been registered")
      await cbq.answer()
      return
    if mth =="re_q2":
      await cbq.edit_inline_text(cbq.inline_message_id, "My master is very kind!!!\n he will surely help you")
      await cbq.answer()
      return
    if mth =="re_q3":
      await cbq.edit_inline_text(cbq.inline_message_id,"Do not dare to do that\n Blocking you")
      await kingbot.block_user(idd)
      await cbq.answer()
      return
    if mth =="re_q4":
      await cbq.edit_inline_text(cbq.inline_message_id,"Nice to meet you. Let me notify the Master")
      await cbq.answer()
      return
@kingbot.on_message(filters.command("app", vr.get("HNDLR")) & filters.user(Adminsettings) & filters.private)
async def refet(_, message):
  if message.chat.id in Adminsettings:
     await message.edit_text("The user is same as me how can I do such tricks here")
  else:
    await message.edit_text("the user has been approved!!")
    await givepermit(message.chat.id)
     
@kingbot.on_message(filters.command("app", vr.get("HNDLR")) & filters.user(Adminsettings) & filters.private)
async def refet(_, message):
  if message.chat.id in Adminsettings:
     await message.edit_text("The user is same as me how can I do such tricks here")
  else:
    await message.edit_text("the user has been blocked!!")
    await blockuser(message.chat.id)
    await kingbot.block_user(message.chat.id)
    
@kingbot.on_message(filters.command("allpermitted", vr.get("HNDLR")) & filters.user(Adminsettings))
async def rfet(_, message):
  dtt = await allallowed()
  strr ="Following are the users allowed"
  for x in dtt:
    usr= kingbot.get_users(x)
    strr+=f"\n {usr.mention()}"
  message.edit_text(strr)
@kingbot.on_message(filters.command("allblocked", vr.get("HNDLR")) & filters.user(Adminsettings))
async def rfet(_, message):
  dtt = await allblocked()
  strr ="Following are the users blocked"
  for x in dtt:
    usr= kingbot.get_users(x)
    strr+=f"\n {usr.mention()}"
  message.edit_text(strr)
@kingbot.on_message(filters.command("nonpermitted", vr.get("HNDLR")) & filters.user(Adminsettings))
async def rfet(_, message):
  dtt = await inwarns()
  strr ="Following are the users not allowed"
  for x in dtt:
    usr= kingbot.get_users(x)
    strr+=f"\n {usr.mention()}"
  message.edit_text(strr)

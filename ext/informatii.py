import discord
from discord.ext import commands
import datetime
import asyncio
emote = "<:point:558362088586608640>"
class Informatii(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='userinfo')
    @commands.guild_only()
    async def userinfo(self, ctx, *, member: discord.Member=None):
        if not member:
            member = ctx.author
        overwrite = ['ADD_REACTIONS', 'ATTACH_FILES', 'CHANGE_NICKNAME', 'CONNECT', 'CREATE_INSTANT_INVITE', 'EMBED_LINKS', 'EXTERNAL_EMOJIS', 'MENTION_EVERYONE', 'READ_MESSAGE_HISTORY', 'READ_MESSAGES', 'SEND_MESSAGES', 'SEND_TTS_MESSAGES', 'SPEAK', 'USE_VOICE_ACTIVATION']
        perms = ' | '.join(perm for perm, value in member.guild_permissions if value and perm.upper() not in overwrite )
        if member.guild_permissions.administrator:
            perms = "administrator"
        created = datetime.datetime.now() - member.created_at
        joined  = datetime.datetime.now() - member.joined_at
        roles =  str([role.name for role in member.roles]).replace(",", " | ").replace("'", '').replace("@everyone | ", '').replace("]", '').replace("[", '')
        all_text = f"""**❱❱ Informatii ca user: **
⚫ Profil: **{member.mention}#{member.discriminator}**\n⚫ Prezenta: **{str(member.status)}**\n⚫ Creat acum: **{created.days} zile** ({'{0:%d-%m-%Y}'.format(member.created_at)})\n⚫ Jucandu-se: **{member.activity or "Nimic"}**\n⚫ ID : **{member.id}**

**❱❱ Informatii ca membru:**
⚫ Nickname: **{member.nick or "No nickname"}**\n⚫ Intrat pe acest server acum: **{joined.days} zile** ({'{0:%d-%m-%Y}'.format(member.joined_at)})

**❱❱ Role-uri[{len(member.roles) - 1}]: **
``{roles}``

**❱❱ Permisii extra: **
``{perms.upper() or "No extra permissions"}``
"""
        embed = discord.Embed(colour=member.colour, description= f"{all_text}")
        embed.set_thumbnail(url = member.avatar_url)

        await ctx.send(content=None, embed=embed)

    @commands.command(name='serverinfo', aliases=['ginfo'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        created = datetime.datetime.now() - guild.created_at
        roles =  str([role.name for role in guild.roles]).replace(",", " | ").replace("'", '').replace("@everyone | ", '').replace("]", '').replace("[", '')
        all_text = f"""**❱❱ Detalii despre membrii: **
⚫ Total : **{len(guild.members)} membrii**\n⚫ Owner : **{guild.owner.mention}**

**❱❱ Detalii despre camere: **
⚫ Total: **{len(ctx.guild.channels)} camere**
⚫ Text : **{len(ctx.guild.text_channels)} camere**, Voice : **{len(ctx.guild.voice_channels)} camere**

**❱❱ Alte detalii: **
⚫ Nume: **{guild.name}**
⚫ ID: **{guild.id}**
⚫ Regiune: **{str(guild.region).upper()}**
⚫ Creat acum: **{created.days} zile** ({'{0:%Y-%m-%d}'.format(guild.created_at)})

**❱❱ Role-uri[{len(guild.roles) - 1}]: **
``{roles}``


"""
        embed = discord.Embed(colour=0x36393f, description= f"{all_text}")
        embed.set_thumbnail(url = guild.icon_url)

        await ctx.send(content=None, embed=embed)

    @commands.command(name = "memberstats")
    @commands.guild_only()
    async def membercount(self, ctx):
      onmoji= "<:online:556828508521758721>"
      dmoji= "<:dnd:556828236177211423>"
      imoji= "<:idle:556828419099459603>"
      omoji= "<:offline:556828341295120394>"

      guild = ctx.guild
      onlinelist = []
      dndlist = []
      idlelist = []
      offlinelist = []
      for x in guild.members:
        if str(x.status) == "online":
          onlinelist.append(x)
        elif str(x.status) == "dnd":
          dndlist.append(x)
        elif str(x.status) == "idle":
          idlelist.append(x)
        elif str(x.status) == "offline":
          offlinelist.append(x)

      online = len(onlinelist)
      dnd = len(dndlist)
      idle = len(idlelist)
      offline = len(offlinelist)

      dates = []
      last, last1, last2 = "", "", ""
      for x in guild.members:
          dates.append(x.joined_at)
      try:
        oldest = min(dates)
        youngest = max(dates)
        a = dates.copy()
        a.remove(oldest)
        a.remove(youngest)
        oldest1 = min(a)
        youngest1 = max(a)
        b = a.copy()
        b.remove(oldest1)
        b.remove(youngest1)
        oldest2 = min(b)
        youngest2 = max(b)
      except ValueError:
        return await ctx.send("Frate, macar 6 membrii, stii cum zic?")
      first, second, third = "", "", ""
      for x in guild.members:
        if x.joined_at == oldest:
          first = f"{str(x.mention)}"
        if x.joined_at == oldest1:
          second = f"{str(x.mention)}"
        if x.joined_at == oldest2:
          third = f"{str(x.mention)}"
        if x.joined_at == youngest:
          last = f"{str(x.mention)}"
        if x.joined_at == youngest1:
          last1 = f"{str(x.mention)}"
        if x.joined_at == youngest2:
          last2 = f"{str(x.mention)}"
        
      all_text = f"""Totalul - {len(guild.members)} membri\n\n**❱❱ Dupa status:** \n{onmoji} -  {online} membrii online\n{dmoji} -  {dnd} membrii ocupati\n{imoji} -  {idle} membrii inactivi\n{omoji} -   {offline} membrii offline\n\n**❱❱ Dupa data:**\nCei mai vechi membrii: {"{} | {} | {}".format(first, second, third)}\nCei mai noi membrii: {"{} | {} | {}".format(last, last1, last2)}"""

      em = discord.Embed(colour=0x36393f, description= f"{all_text}")
      em.set_thumbnail(url = guild.icon_url)
      await ctx.send(content = None, embed = em)

    @commands.command(name='invite', aliases=['inv'])
    @commands.guild_only()
    async def invite(self, ctx):
        await ctx.message.add_reaction("👌")
        await ctx.author.send("Thanks for inviting me!\ninca se lucreaza, keep calm")

    @commands.command(name='secret', aliases=['shh'])
    @commands.guild_only()
    async def secret(self, ctx):
        await ctx.message.add_reaction("👌")
        await ctx.author.send("There's nothing lol")

    @commands.command(name="help")
    async def help(self, ctx):
        em = discord.Embed(colour=0x36393f, description = "Commands")
        em.set_author(name=self.bot.user.name, icon_url= self.bot.user.avatar_url)
        em.set_thumbnail(url = self.bot.user.avatar_url)
        cogs = self.bot.cogs
        for i in cogs.copy():
            title = i
            n = ' , '.join(m.name for m in self.bot.commands if m.cog_name == i and m.hidden == False)
            if len(self.bot.get_cog(title).get_commands()) == 0 or n == "": self.bot.cogs.pop(title)
            await asyncio.sleep(0.04)
            em.add_field(name = title.upper(), value = f"`{n}`", inline = False)
        await ctx.send(content=None, embed = em)


    @commands.command(name="ping")
    async def ping(self, ctx):
    	m = await ctx.send("Connecting to nasa.gov...")
    	latency = self.bot.latency * 1000
    	ms = (m.created_at-ctx.message.created_at).total_seconds() * 1000
    	await m.edit(content = f"NASA Server: `{int(ms)}ms`. WebSocket is: `{int(latency)}ms`")
    
def setup(bot):
    bot.add_cog(Informatii(bot))

import discord
from discord.ext import commands
import datetime
import asyncio
import traceback
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import copy
from typing import Union
reject = "❌"
accept = "✅"
warning = "⚠"

class Moderare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()
        
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'
        

    @commands.command(name='ban')
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member=None, *, reason:str = None):

        if not ctx.message.guild.me.guild_permissions.ban_members:
            return await ctx.send(f"{reject} Member Role is more higher then mine, please move it.")
        if not member:
            return await ctx.send(f"{reject} No member, please mention someone.")
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.send(f"{reject} You don't have access, please contact ownership for administrative role!")
        if reason is None:
            return await ctx.send(f"{reject} I can't ban him without a reason.")

        if member.id == ctx.author.id:
            return

        try:
            await ctx.guild.ban(discord.Object(id=member.id), reason = f"{ctx.author} banned him with reason : {reason}")
            await ctx.send(f"**Goodbye, `{member}`. You got banned.**")
        except discord.errors.Forbidden:
            await ctx.send(f"{warning} Member Role is more higher then mine, please move it.")

    @commands.command(name='unban')
    @commands.guild_only()
    async def unban(self, ctx, *,member: str = None):
        if not ctx.message.guild.me.guild_permissions.ban_members:
            return await ctx.send(f"{reject} I can't remove him:(")
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.send(f"{reject} You don't have access, please contact ownership for administrative role!")
        if not member:
            return await ctx.send(f"{reject}No member, please mention someone.")


        if member == ctx.author.id:
            return await ctx.send(f"{reject} You are idiot or ?")

        else:
            try:
                await ctx.guild.unban(discord.Object(id=member), reason=f"{ctx.author} unbanned him.")
                await ctx.send(f"**{accept} Alright <@{member}>, i removed him from banned**")
            except discord.errors.NotFound:
                return await ctx.send(f"{reject} Mentioned Person isn't banned.")
            except discord.errors.Forbidden:
                return await ctx.send(f"{reject} You are idiot or ?")          
            except discord.errors.HTTPException:
                return await ctx.send(f"{reject} This isn't a good ID.")


    @commands.command(name='purge')
    @commands.guild_only()
    async def purge(self, ctx, messages:int=None):

        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send(f"{reject} N-ai acces, fraiere")

        if messages is None:
            return await ctx.send(f"{reject} Cate mesaje frt?")
        messages += 1  

        if(messages > 200):
            return await ctx.send(f"{reject} Hoooo nebunule, maxim 200")

        try:
            await ctx.message.delete()
            await ctx.channel.purge(limit=messages)
            messages = messages - 1
            await ctx.send(f"**{accept} Mi-am sters lacrimile si `{messages}` mesaje**")
        except discord.Forbidden:
            return await ctx.send(f'{warning} N-am acces frt')
        except discord.HTTPException as e:
            return await ctx.send(f'{warning} Eroare d-aia urata:\n {e}')



#_________________________________hidden________________________________________________
    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Moderare(bot))

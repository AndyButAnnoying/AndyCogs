#Originally from Phen-Cogs https://github.com/phenom4n4n/phen-cogs/blob/master/lock/converters.py

from typing import Union

import discord
from unidecode import unidecode
from rapidfuzz import process
from discord.ext.commands.converter import RoleConverter
from redbot.core import commands
from redbot.core.commands import BadArgument
from redbot.core.utils.chat_formatting import inline




# original converter from https://github.com/TrustyJAID/Trusty-cogs/blob/master/serverstats/converters.py#L19

class FuzzyRole(RoleConverter):
    """
    This will accept role ID's, mentions, and perform a fuzzy search for
    roles within the guild and return a list of role objects
    matching partial names
    Guidance code on how to do this from:
    https://github.com/Rapptz/discord.py/blob/rewrite/discord/ext/commands/converter.py#L85
    https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/mod/mod.py#L24
    """

    def __init__(self, response: bool = True):
        self.response = response
        super().__init__() 

    async def convert(self, ctx: commands.Context, argument: str) -> list:
        if argument.lower() == "none":
            return None
        argument = argument.split(";;")
        sorted_results = []
        result = []
        guild = ctx.guild
        for arg in argument:
            args = args.lstrip("<@&").rstrip(">")
            if str(arg).isdigit():
                arg = guild.get_role(int(arg))
                if not arg:
                    continue 
                sorted_results.append(arg)
                continue
                
            else:
                for r in process.extract(
                    arg,
                    {r: unidecode(r.name) for r in guild.roles},
                    limit=None,
                    score_cutoff=75,
                ):
                    result.append((r[2], r[1]))
                if not result:
                    return "e"
                return result
                sorted_result = sorted(result, key=lambda r: r[1], reverse=True)
                return sorted_result
                sorted_results.append(sorted_result[0][0])
        
        if len(sorted_results) == 0:
            return None
            
        return sorted_results
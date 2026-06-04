import random

import discord
from discord.ext import bridge, commands


class Dice(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Comments

    @commands.command()
    async def d4(self, ctx: commands.Context):
        randomnum = random.randint(1, 4)
        await ctx.send(str(randomnum) + ":game_die:")

    @commands.command()
    async def d6(self, ctx: commands.Context):
        randomnum = random.randint(1, 6)
        await ctx.send(str(randomnum) + ":game_die:")

    @commands.command()
    async def d10(self, ctx: commands.Context):
        randomnum = random.randint(1, 10)
        await ctx.send(str(randomnum) + ":game_die:")

    @commands.command()
    async def d12(self, ctx: commands.Context):
        randomnum = random.randint(1, 12)
        await ctx.send(str(randomnum) + ":game_die:")

    @commands.command()
    async def d20(self, ctx: commands.Context):
        randomnum = random.randint(1, 20)
        await ctx.send(str(randomnum) + ":game_die:")
        if randomnum == 20:
            await ctx.reply("Congratulations")

    @commands.command()
    async def d100(self, ctx: commands.Context):
        randomnum = random.randint(1, 100)
        await ctx.send(str(randomnum) + ":game_die:")
        if randomnum == 100:
            await ctx.reply("Congratulations, but really, why?")

    @bridge.bridge_command(name="alldice", description="Rolls all the dice")
    async def alldice(self, ctx: discord.ApplicationContext):
        randomd4 = random.randint(1, 4)
        randomd6 = random.randint(1, 6)
        randomd10 = random.randint(1, 10)
        randomd12 = random.randint(1, 12)
        randomd20 = random.randint(1, 20)
        randomd100 = random.randint(1, 100)

        await ctx.respond(
            f"D4: {str(randomd4)}:game_die: \nD6: {str(randomd6)}:game_die:\nD10: {str(randomd10)}:game_die: \nD12: {str(randomd12)}:game_die:\nD20: {str(randomd20)}:game_die:\nD100:{str(randomd100)}:game_die:"
        )

        if (
            randomd4 == 4
            and randomd6 == 6
            and randomd10 == 10
            and randomd12 == 12
            and randomd20 == 20
            and randomd100 == 100
        ):
            await ctx.send(f"What the actual fuck @everyone. {ctx.author} has done it")


def setup(client):
    print("Set up Dice")
    client.add_cog(Dice(client))

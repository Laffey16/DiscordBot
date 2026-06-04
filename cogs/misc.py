import html
import os
import random

import discord
import requests
from discord.ext import bridge, commands

import data.aliases as aliases
import extrafunctions
from resources.triviaview import TriviaView


# region GettingAPIStuff
def fox_getter():
    print("getting fox")
    link = "https://randomfox.ca/floof/"
    r = requests.get(link).json()
    foximage = r["image"]
    print("gotten fox")
    return foximage


def joke_getter():
    link = "https://official-joke-api.appspot.com/jokes/random"
    r = requests.get(link).json()
    setupjoke = r["setup"]
    punchline = r["punchline"]
    joke = f"{setupjoke}\n||{punchline}||"
    return joke


def bored_getter():
    link = "https://bored-api.appbrewery.com/random"
    r = requests.get(link).json()
    activity = r["activity"]
    return activity


def dad_joke_getter():
    link = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    r = requests.get(link, headers=headers).json()
    return r["joke"]


def weather_getter(location):
    print(location)
    if isinstance(location, str):
        url = "https://api.openweathermap.org/data/2.5/weather"

        querystring = {
            "q": location,
            "appid": f"{os.environ['OPEN_WEATHER_API_KEY']}",
            "units": "metric",
        }

        response = requests.request("GET", url, params=querystring)
        if response.status_code != 200:
            return f"Request failed.\nStatus Code:{response.status_code}"
        data = response.json()

        try:
            temp = data["main"]["temp"]
            realfeel = data["main"]["feels_like"]
            pressure = data["main"]["pressure"]
            weather = data["weather"][0]["description"]
            windspeed = data["wind"]["speed"]
            winddirection = data["wind"]["deg"]
            humidity = data["main"]["humidity"]
            sunrise = data["sys"]["sunrise"]
            sunset = data["sys"]["sunset"]
        except KeyError:
            return f"Couldn't find weather for {location}"

        weather_report = (
            f"The general weather in {location.capitalize()} is currently {weather}\n"
            f"The temperature is {temp}°C with a humidity "
            f"of {humidity}% due to this it feels like {realfeel}°C.\n"
            f"The wind speed is currently {windspeed}m/s the direction is {extrafunctions.wind_direction_to_text(winddirection)}.\n"
            f"The pressure is currently {pressure} millibars.\n"
            f"The sun will rise at <t:{sunrise}:T>.\n"
            f"While the sun will set at <t:{sunset}:T>."
        )
        return weather_report
    else:
        return "Not a place?"


def fun_fact_getter():
    link = "https://uselessfacts.jsph.pl/random.json?language=en"
    r = requests.get(link)
    if r.status_code != 200:
        return f"Error finding funfact. Statuscode:{r.status_code}"
    return r.json()["text"]


def trivia_getter():
    link = "https://opentdb.com/api.php?amount=1"
    r = requests.get(link).json()
    question = r["results"][0]["question"]
    correct = r["results"][0]["correct_answer"]
    incorrect = r["results"][0]["incorrect_answers"]
    incorrect.append(correct)
    random.shuffle(incorrect)
    question = f"Question: {question}"
    return question, incorrect, correct


def anime_getter(tag: str) -> str:
    link = "https://safebooru.org//index.php?page=dapi&s=post&q=index&json=1"
    tag = tag.lower().strip()

    for name, real_tag in aliases.SERIES_ALIASES.items():
        tag = tag.replace(name, real_tag)

    cleaned = []
    for part in tag.split(","):
        cleaned.append(part.strip().replace(" ", "_"))
    tag = " ".join(cleaned)

    print(tag)
    r = requests.get(link, params={"tags": tag})
    if r.status_code != 200:
        return f"Error finding anime. Status code:{r.status_code}"

    try:
        data = r.json()
    except ValueError:
        return f"No results found for `{tag}`."

    if not data:
        return f"No results found for `{tag}`."

    return random.choice(data)["file_url"]


def anime_random_getter(limit: int = 1):
    limit = max(1, min(limit, 10))
    link = "https://safebooru.org//index.php?page=dapi&s=post&q=index"
    querystring = {"json": 1, "limit": limit, "sort": "random"}

    r = requests.get(link, params=querystring)

    if r.status_code != 200:
        return f"Request failed\nStatus code: {r.status_code}"
    data = r.json()
    print(data)
    imagelist = []
    images = data["post"]
    for i in images:
        imagelist.append(i["file_url"])
    return imagelist


def duck():
    r = requests.get("https://random-d.uk/api/quack")
    if r.status_code == 200:
        data = r.json()
        print(r.url)
        return f"{data['url']}"
    else:
        return f"Something messed up.\nStatus code: {r.status_code}"


def shiba():
    r = requests.get("https://shibe.online/api/shibes")
    if r.status_code == 200:
        data = r.json()
        print(r.url)
        return data[0]
    else:
        return f"Something messed up.\nStatus code: {r.status_code}"


# endregion


# region DiscordCommands
class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(name="foxes", description="Foxes :)")
    async def foxes(self, ctx):
        await ctx.respond(fox_getter())

    @bridge.bridge_command(name="funfact", description="Random funfact.")
    async def funfact(self, ctx):
        await ctx.respond(fun_fact_getter())

    @bridge.bridge_command(name="joke", description="Random joke.Very funny.")
    async def joke(self, ctx):
        await ctx.respond(joke_getter())

    @commands.command()
    async def dadjoke(self, ctx):
        await ctx.respond(dad_joke_getter())

    @bridge.bridge_command(name="trivia", description="Random trivia question.")
    async def trivia(self, ctx: discord.ApplicationContext):
        # Gets the data
        data = trivia_getter()
        correctanswer = html.unescape(data[2])
        answers = html.unescape(data[1])
        question = html.unescape(data[0])

        print(question)
        # Wait for a response to those buttons
        await ctx.respond(
            question,
            view=TriviaView(
                labels=answers, style=discord.ButtonStyle.primary, answer=correctanswer
            ),
        )

    @bridge.bridge_command(name="bored", description="You're bored")
    async def bored(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"How about you:\n{bored_getter()}")

    @bridge.bridge_command(name="weather", description="Gets weather for random place.")
    async def weather(self, ctx: discord.ApplicationContext, location: str):
        await ctx.defer()
        await ctx.respond(weather_getter(location))

    @bridge.bridge_command(
        name="anime", description="Gets a sfw image based off tags. If empty random."
    )
    async def anime(self, ctx: discord.ApplicationContext, *, tag: str = ""):
        print(tag)
        if not tag:
            await ctx.respond(anime_random_getter())
            return
        await ctx.respond(anime_getter(tag))

    @bridge.bridge_command(name="animerandom", description="Gets a random anime image.")
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def animerandom(self, ctx: discord.ApplicationContext, limit: int = 1):
        await ctx.respond("\n".join(anime_random_getter(limit)))

    @bridge.bridge_command(
        name="cuteanimal",
        description="Gets a cute animal pic",
    )
    async def animal_image(self, ctx: discord.ApplicationContext):
        print("Getting animal pic")
        # Random Animal picture
        randomlist = ["duck", "shiba", "fox"]
        random_function_choice = random.choices(randomlist)

        print(random_function_choice[0])

        if random_function_choice[0] == "duck":
            await ctx.respond(duck())
        elif random_function_choice[0] == "shiba":
            await ctx.respond(shiba())
        elif random_function_choice[0] == "fox":
            await ctx.respond(fox_getter())

    # endregion


def setup(client):
    print("Set up Misc")
    client.add_cog(Misc(client))

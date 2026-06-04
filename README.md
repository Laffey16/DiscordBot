# DiscordBot

A small, fun-and-utility Discord bot built with [Pycord](https://pycord.dev/), created for learning and portfolio purposes. It pulls from a handful of free public APIs to serve up jokes, trivia, weather, images,etc.

Commands are implemented as **bridge commands** where possible, meaning most work both as slash commands (`/joke`) and as prefix commands (`!joke`).

## Commands

Bridge commands work as both `/slash` and `!prefix` commands. The default prefix is `!`.

## Tech stack

- **Python** 3.13+
- **[Pycord](https://pycord.dev/)** (`py-cord`) 2.8+
- **requests** for API calls
- **python-dotenv** for configuration
- **[uv](https://docs.astral.sh/uv/)** for dependency management

## Project structure

```
DiscordBot/
├── bot.py              # Entry point: sets up the client, loads cogs, runs the bot
├── extrafunctions.py   # Small helpers (e.g. wind-direction formatting)
├── cogs/
│   ├── dice.py         # Dice-rolling commands
│   └── misc.py         # API-backed fun/utility commands
├── data/
│   └── aliases.py      # Friendly-name → tag aliases for anime search
├── resources/
│   ├── buttons.py
│   └── triviaview.py   # Interactive button view for the trivia command
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # Locked dependency versions
└── .python-version     # Pinned Python version
```

## External APIs

This bot relies on the following free public APIs:

- [randomfox.ca](https://randomfox.ca/) — fox images
- [random-d.uk](https://random-d.uk/) — duck images
- [shibe.online](https://shibe.online/) — shiba images
- [Official Joke API](https://github.com/15Dkatz/official_joke_api) — jokes
- [icanhazdadjoke](https://icanhazdadjoke.com/) — dad jokes
- [Useless Facts](https://uselessfacts.jsph.pl/) — fun facts
- [Open Trivia Database](https://opentdb.com/) — trivia questions
- [Bored API](https://bored-api.appbrewery.com/) — activity suggestions
- [OpenWeatherMap](https://openweathermap.org/) — weather data
- [Safebooru](https://safebooru.org/) — SFW anime images

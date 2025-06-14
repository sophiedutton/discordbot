# discordbot

A simple Discord bot where users can collect bunnies. Uses `discord.py`.

## Setup
1. Install `discord.py`:
   ```sh
   pip install discord.py
   ```
2. Create a Discord bot and copy its token.
3. Set the `DISCORD_TOKEN` environment variable with your token:
   ```sh
   export DISCORD_TOKEN=your_token_here
   ```
4. Run the bot:
   ```sh
   python bot.py
   ```

## Commands
- `!collect` – collect a bunny for yourself.
- `!bunnies` – see how many bunnies you have.
- `!leaderboard` – show top collectors.

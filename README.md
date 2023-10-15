# General Discord Bot

A handy discord bot for running random commands.

# Commands:
!rate - Displays the Current Octopus Agile Rate
!av - Displays the Average rate for the next 12hrs
!on - Turns on the smart plug
!off - Turns off the smart plug
!set - Overrides the smart plug schedule, setting the cheapest average rate
!can - Cancel the schedule

# Note:
The schedule is set to run at 8pm every day by default.
The override will clear this and reset the schedule.

# .env:
Populate the .env with the following:

This guide will help with the Discord bot: https://discord.com/developers/docs/intro

This repo will help with the rest: https://github.com/bignellrp/octopus-home-plug

```
GIT_BRANCH=main
DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
DISCORD_TOKEN=
CHANNEL_ID=
COMMAND_PREFIX=!
DISCORD_REDIRECT_URI=http://...:.../callback
OCTOPUS_API_KEY=
SMART_PLUG_IP=
PASSWORD=
EMAIL=
```
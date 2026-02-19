import hikari
import lightbulb

loader = lightbulb.Loader()


@loader.command
class Ping(
    lightbulb.SlashCommand,
    name="ping",
    description="Check if the bot is online.",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, bot: hikari.GatewayBot) -> None:
        latency = round(bot.heartbeat_latency * 1000)
        await ctx.respond(f"Pong! `{latency}ms`.")

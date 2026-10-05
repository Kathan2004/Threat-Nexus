from datetime import UTC, datetime

import discord

from core.models.domain import Alert, ThreatEvent

CHANNEL_BY_NAME = {
    "critical-alerts",
    "daily-brief",
    "cve-watch",
    "ransomware",
    "malware",
    "apt-tracking",
    "breach-watch",
    "dark-web",
    "intel-feed",
    "analyst-room",
}


class DiscordPublisher:
    def __init__(self, client: discord.Client) -> None:
        self.client = client

    async def publish(self, event: ThreatEvent, alert: Alert) -> Alert:
        embed = self._embed(event)
        for channel_name in alert.channels:
            channel = discord.utils.get(self.client.get_all_channels(), name=channel_name)
            if channel and hasattr(channel, "send"):
                if alert.message_id and hasattr(channel, "fetch_message"):
                    message = await channel.fetch_message(int(alert.message_id))
                    await message.edit(embed=embed)
                else:
                    message = await channel.send(embed=embed)
                    alert.message_id = str(message.id)
                    if hasattr(message, "create_thread"):
                        thread = await message.create_thread(name=event.title[:80])
                        alert.thread_id = str(thread.id)
        alert.published_at = alert.published_at or datetime.now(UTC)
        alert.touch()
        return alert

    def _embed(self, event: ThreatEvent) -> discord.Embed:
        color = {
            "CRITICAL": discord.Color.red(),
            "HIGH": discord.Color.orange(),
            "MEDIUM": discord.Color.gold(),
            "LOW": discord.Color.green(),
        }[event.severity.value]
        embed = discord.Embed(
            title=event.title,
            description=event.enrichment.executive_summary if event.enrichment else event.description,
            color=color,
        )
        embed.add_field(name="Severity", value=event.severity.value, inline=True)
        embed.add_field(name="Confidence", value=f"{event.confidence}%", inline=True)
        embed.add_field(name="Active exploitation", value=str(event.active_exploitation), inline=True)
        if event.enrichment:
            embed.add_field(name="Recommendations", value="\n".join(event.enrichment.recommendations[:5]), inline=False)
        embed.add_field(
            name="Sources",
            value="\n".join(sorted({source.source for source in event.sources})) or "internal",
            inline=False,
        )
        return embed

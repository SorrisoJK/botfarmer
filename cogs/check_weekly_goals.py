import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class CheckWeeklyGoalsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="checar_metas_semanal", description="Checa o progresso de todos os membros nas metas semanais")
    async def checar_metas_semanal(self, interaction: discord.Interaction):
        # Verificar se a configuração existe
        if not os.path.exists("farmers/config.json"):
            await interaction.response.send_message("As configurações não foram definidas ainda. Use o comando /cfgfarmer.", ephemeral=True)
            return

        if not os.path.exists("farmers/progress.json"):
            await interaction.response.send_message("Nenhum progresso foi registrado ainda.", ephemeral=True)
            return

        with open("farmers/config.json", "r") as f:
            config = json.load(f)

        with open("farmers/progress.json", "r") as f:
            progress_data = json.load(f)

        log_channel = self.bot.get_channel(config['log_channel_id'])

        if not log_channel:
            await interaction.response.send_message("O canal de log não foi encontrado. Verifique o ID do canal de log nas configurações.", ephemeral=True)
            return

        # Criar a embed de log
        embed = discord.Embed(title="Relatório Semanal de Metas", color=discord.Color.gold())

        for member_id, progress in progress_data.items():
            member = self.bot.get_user(int(member_id))
            if member:
                embed.add_field(
                    name=f"{member.name}#{member.discriminator}",
                    value=(
                        f"**Produto 1:** {progress.get('produto1', 0)}\n"
                        f"**Produto 2:** {progress.get('produto2', 0)}\n"
                        f"**Produto 3:** {progress.get('produto3', 0)}"
                    ),
                    inline=False
                )

        await log_channel.send(embed=embed)
        await interaction.response.send_message("O relatório semanal foi enviado ao canal de log.", ephemeral=True)

    async def cog_load(self):
        guild_id = 1242127884399673474  # Substitua pelo ID do seu servidor (guild)
        guild = discord.Object(id=guild_id)
        self.bot.tree.add_command(self.checar_metas_semanal, guild=guild)

    async def cog_unload(self):
        guild_id = 1242127884399673474  # Substitua pelo ID do seu servidor (guild)
        guild = discord.Object(id=guild_id)
        self.bot.tree.remove_command(self.checar_metas_semanal.name, guild=guild)

async def setup(bot):
    await bot.add_cog(CheckWeeklyGoalsCog(bot))

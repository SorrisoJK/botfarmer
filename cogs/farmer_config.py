import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class FarmerConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cfgfarmer", description="Configurações para o sistema de Farmer")
    async def cfgfarmer(self, interaction: discord.Interaction):
        modal = FarmerConfigModal()
        await interaction.response.send_modal(modal)

    async def cog_load(self):
        guild_id = 1242127884399673474  # Substitua pelo ID do servidor
        guild = discord.Object(id=guild_id)
        self.bot.tree.add_command(self.cfgfarmer, guild=guild)

    async def cog_unload(self):
        guild_id = 1242127884399673474  # Substitua pelo ID do servidor
        guild = discord.Object(id=guild_id)
        self.bot.tree.remove_command(self.cfgfarmer.name, guild=guild)

class FarmerConfigModal(discord.ui.Modal, title="Configuração de Farmer"):
    thumbnail = discord.ui.TextInput(label="Thumbnail URL", placeholder="Insira a URL da thumbnail")
    log_channel_id = discord.ui.TextInput(label="ID do Canal de Logs", placeholder="Insira o ID do canal de logs", style=discord.TextStyle.short)
    category_id = discord.ui.TextInput(label="ID da Categoria", placeholder="Insira o ID da categoria", style=discord.TextStyle.short)
    role_id = discord.ui.TextInput(label="ID do Cargo", placeholder="Insira o ID do cargo", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        # Verifique se o diretório existe, se não, crie-o
        if not os.path.exists("farmers"):
            os.makedirs("farmers")

        config = {
            "thumbnail": self.thumbnail.value,
            "log_channel_id": int(self.log_channel_id.value),
            "category_id": int(self.category_id.value),
            "role_id": int(self.role_id.value)
        }

        with open("farmers/cfgfarmer.json", "w") as f:
            json.dump(config, f, indent=4)

        await interaction.response.send_message("Configurações salvas com sucesso!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FarmerConfigCog(bot))

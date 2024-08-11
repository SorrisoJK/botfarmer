import discord
from discord import app_commands
from discord.ext import commands
import json
import os  # Importação do módulo os

class ProductRegistrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pfarmer", description="Registra produtos de cada meta")
    async def pfarmer(self, interaction: discord.Interaction):
        modal = ProductRegistrationModal()
        await interaction.response.send_modal(modal)

    async def cog_load(self):
        guild_id = 1242127884399673474  # Substitua pelo ID do servidor
        guild = discord.Object(id=guild_id)
        self.bot.tree.add_command(self.pfarmer, guild=guild)

    async def cog_unload(self):
        guild_id = 1242127884399673474  # Substitua pelo ID do servidor
        guild = discord.Object(id=guild_id)
        self.bot.tree.remove_command(self.pfarmer.name, guild=guild)

class ProductRegistrationModal(discord.ui.Modal, title="Registro de Produtos"):
    produto1 = discord.ui.TextInput(label="Produto 1", placeholder="Nome do Produto 1", required=True)
    produto2 = discord.ui.TextInput(label="Produto 2", placeholder="Nome do Produto 2 (opcional)", required=False)
    produto3 = discord.ui.TextInput(label="Produto 3", placeholder="Nome do Produto 3 (opcional)", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        # Verifique se o diretório existe, se não, crie-o
        if not os.path.exists("farmers"):
            os.makedirs("farmers")

        produtos = {
            "produto1": self.produto1.value,
            "produto2": self.produto2.value if self.produto2.value else None,
            "produto3": self.produto3.value if self.produto3.value else None
        }

        with open("farmers/products.json", "w") as f:
            json.dump(produtos, f, indent=4)

        await interaction.response.send_message("Produtos registrados com sucesso!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ProductRegistrationCog(bot))

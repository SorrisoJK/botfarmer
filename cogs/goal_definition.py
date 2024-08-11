import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class GoalDefinitionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dfmetas", description="Define as metas para os produtos")
    async def dfmetas(self, interaction: discord.Interaction):
        modal = GoalDefinitionModal()
        await interaction.response.send_modal(modal)

    async def cog_load(self):
        guild_id = 1242127884399673474  # Substitua pelo ID do servidor
        guild = discord.Object(id=guild_id)
        self.bot.tree.add_command(self.dfmetas, guild=guild)

    async def cog_unload(self):
        guild_id = 1242127884399673474  # Substitua pelo ID do servidor
        guild = discord.Object(id=guild_id)
        self.bot.tree.remove_command(self.dfmetas.name, guild=guild)

class GoalDefinitionModal(discord.ui.Modal, title="Definição de Metas"):
    meta_produto1 = discord.ui.TextInput(label="Meta Produto 1", placeholder="Insira a meta para o Produto 1", required=True)
    meta_produto2 = discord.ui.TextInput(label="Meta Produto 2", placeholder="Insira a meta para o Produto 2 (opcional)", required=False)
    meta_produto3 = discord.ui.TextInput(label="Meta Produto 3", placeholder="Insira a meta para o Produto 3 (opcional)", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        # Verifique se o diretório existe, se não, crie-o
        if not os.path.exists("farmers"):
            os.makedirs("farmers")

        metas = {
            "meta_produto1": self.meta_produto1.value,
            "meta_produto2": self.meta_produto2.value if self.meta_produto2.value else None,
            "meta_produto3": self.meta_produto3.value if self.meta_produto3.value else None
        }

        with open("farmers/metas.json", "w") as f:
            json.dump(metas, f, indent=4)

        await interaction.response.send_message("Metas definidas com sucesso!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(GoalDefinitionCog(bot))

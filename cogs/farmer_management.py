import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class FarmerProgressModal(discord.ui.Modal):
    def __init__(self, product_name):
        super().__init__(title=f"Adicionar Progresso - {product_name}")

        self.progresso = discord.ui.TextInput(label="Quantidade Adicionada", placeholder="Insira a quantidade", required=True)
        self.data_hora = discord.ui.TextInput(label="Data e Hora", placeholder="Exemplo: 11/08/2024 14:30", required=True)

        self.add_item(self.progresso)
        self.add_item(self.data_hora)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Progresso registrado: {self.progresso.value} unidades em {self.data_hora.value}", ephemeral=True)

class ProductSelectMenu(discord.ui.Select):
    def __init__(self, products):
        options = []
        for product in products:
            if product:
                options.append(discord.SelectOption(label=product, description=f"Registrar progresso para {product}"))

        super().__init__(placeholder="Selecione o produto...", options=options)

    async def callback(self, interaction: discord.Interaction):
        modal = FarmerProgressModal(self.values[0])
        await interaction.response.send_modal(modal)

class FarmerProgressView(discord.ui.View):
    def __init__(self, products):
        super().__init__(timeout=None)
        self.add_item(ProductSelectMenu(products))

class CreateFarmerChannelButton(discord.ui.View):
    def __init__(self, category_id, role_id, thumbnail_url, goals):
        super().__init__(timeout=None)
        self.category_id = category_id
        self.role_id = role_id
        self.thumbnail_url = thumbnail_url
        self.goals = goals

    @discord.ui.button(label="Abrir Canal de Farmer", style=discord.ButtonStyle.primary)
    async def create_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Criar o canal na categoria definida
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=self.category_id)
        role = guild.get_role(self.role_id)

        if not category or not role:
            await interaction.response.send_message("Erro na configuração da categoria ou cargo.", ephemeral=True)
            return

        channel_name = f"farmer-{interaction.user.name}"
        channel = await guild.create_text_channel(channel_name, category=category)

        # Definir permissões para o canal
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(role, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False)

        # Enviar a embed com as metas no canal criado
        embed = discord.Embed(title="Sua meta Semanal 📦", color=discord.Color.green())
        embed.set_thumbnail(url=self.thumbnail_url)
        embed.add_field(name="Produto 1", value=f"Meta: {self.goals['meta_produto1']}\nProgresso: 0000/{self.goals['meta_produto1']}", inline=False)
        
        products = [self.goals['meta_produto1'], self.goals.get('meta_produto2'), self.goals.get('meta_produto3')]
        
        if self.goals['meta_produto2']:
            embed.add_field(name="Produto 2", value=f"Meta: {self.goals['meta_produto2']}\nProgresso: 0000/{self.goals['meta_produto2']}", inline=False)
        
        if self.goals['meta_produto3']:
            embed.add_field(name="Produto 3", value=f"Meta: {self.goals['meta_produto3']}\nProgresso: 0000/{self.goals['meta_produto3']}", inline=False)

        embed.set_footer(text="Você pode continuar farmando após bater a meta para receber um extra 😉")

        view = FarmerProgressView(products)
        await channel.send(embed=embed, view=view)

        await interaction.response.send_message(f"Canal criado com sucesso: {channel.mention}", ephemeral=True)

class FarmerManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="bfarmer", description="Cria um canal pessoal para o farmer")
    async def bfarmer(self, interaction: discord.Interaction):
        # Carregar a configuração
        if not os.path.exists("farmers/config.json"):
            await interaction.response.send_message("As configurações não foram definidas ainda. Use o comando /cfgfarmer.", ephemeral=True)
            return

        if not os.path.exists("farmers/goals.json"):
            await interaction.response.send_message("As metas não foram definidas ainda. Use o comando /dfmetas.", ephemeral=True)
            return

        with open("farmers/config.json", "r") as f:
            config = json.load(f)

        with open("farmers/goals.json", "r") as f:
            goals = json.load(f)

        embed = discord.Embed(title="Metas de farm 📦", color=discord.Color.blue())
        embed.set_thumbnail(url=config['thumbnail'])
        embed.description = "Clique no botão abaixo para abrir seu canal de farmer.\nSeu farm é muito importante e você recebe por ele!"

        view = CreateFarmerChannelButton(config['category_id'], config['role_id'], config['thumbnail'], goals)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(FarmerManagementCog(bot))

import discord
from .utils import get_member_nickname


class QuestionView(discord.ui.View):
    def __init__(self, points, already_answered, question):
        super().__init__()
        self.question = question
        self.points = points
        self.already_answered = []
        self.answered_correctly = already_answered
        for i in range(3):
            self.children[i].label = self.question.answers[i]

    async def validate_answer(self, interaction, correct_answer):
        if interaction.user not in self.points or interaction.user in self.already_answered:
            return
        else:
            self.already_answered.append(interaction.user)
        if self.question.correct_answer == correct_answer:
            self.answered_correctly[interaction.user] = True
            self.points[interaction.user] += 1
        await interaction.response.defer()

    def disable_buttons(self):
        for button in self.children:
            if isinstance(button, discord.ui.Button):
                button.disabled = True

    @discord.ui.button(label="", custom_id="answer1", style=discord.ButtonStyle.red)
    async def answer1(self, interaction, button):
        await self.validate_answer(interaction, 0)

    @discord.ui.button(label="", custom_id="answer2", style=discord.ButtonStyle.red)
    async def answer2(self, interaction, button):
        await self.validate_answer(interaction, 1)

    @discord.ui.button(label="", custom_id="answer3", style=discord.ButtonStyle.red)
    async def answer3(self, interaction, button):
        await self.validate_answer(interaction, 2)


class QuizView(discord.ui.View):
    playing_users = []

    @discord.ui.button(label="JA", style=discord.ButtonStyle.primary)
    async def add_user_to_game(self, interaction, button):
        if interaction.user not in self.playing_users:
            self.playing_users.append(interaction.user)
            await interaction.response.send_message(f"+{get_member_nickname(interaction.user).upper()}")

    def disable_button(self):
        self.children[0].disabled = True


class RankingView(discord.ui.View):
    def __init__(self, time_method, points_method, ctx):
        super().__init__()
        self.ctx = ctx
        self.time_method = time_method
        self.points_method = points_method

    @discord.ui.button(label="Czasu", custom_id="time_button", style=discord.ButtonStyle.secondary,
                       emoji="⏱")
    async def time_callback(self, interaction, button):
        if self.ctx.author.id == interaction.user.id:
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await interaction.response.edit_message(embed=self.time_method(), view=self)

    @discord.ui.button(label="Punktow", custom_id="points_button", style=discord.ButtonStyle.secondary,
                       emoji="💯")
    async def points_callback(self, interaction, button):
        if self.ctx.author.id == interaction.user.id:
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await interaction.response.send_message(embed=self.points_method(), view=self)
import discord


class TriviaView(discord.ui.View):
    alreadypressed = []

    def __init__(
        self,
        labels: list,
        style,
        answer,
    ):
        super().__init__()
        self.label = labels
        self.style = style
        self.answer = answer
        self.alreadypressed = []

        for label in labels:
            button = discord.ui.Button(
                label=label, style=style, row=None, custom_id=label
            )
            button.callback = self.callback
            self.add_item(button)

    # When button pressed
    async def callback(self, interaction):
        # if already pressed
        if interaction.user.id in self.alreadypressed:
            await interaction.response.send_message(
                "You can only answer once.", ephemeral=True
            )
            return

        # if user correct
        if interaction.custom_id == self.answer:
            await interaction.response.send_message(
                f"Congratulations you've got it right {interaction.user.display_name}"
            )
            self.alreadypressed.append(interaction.user.id)
        # if user wrong
        else:
            await interaction.response.send_message(
                f"Sorry you've got it wrong: The actual answer is {self.answer}",
                ephemeral=True,
            )
            self.alreadypressed.append(interaction.user.id)

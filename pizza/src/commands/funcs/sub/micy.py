import discord
from discord import app_commands
import sounddevice as sd
import wave
import winsound, asyncio
from io import BytesIO
import config
from core.logger import logger


class Play(discord.ui.View):
  def __init__(self, buffer: BytesIO, dur):
      self.buffer = buffer 
      self.dur = dur
      super().__init__(timeout=None)
         
  @discord.ui.button(label=f'Playback through playsound', style=discord.ButtonStyle.gray, row=1, disabled=False)
  async def ps(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            embed = discord.Embed(description="Playing...", color=config.embedcolor)
            msg = await interaction.response.send_message(embed=embed, delete_after=self.dur + 1.5)
            sBytes = self.buffer.getvalue()
            await asyncio.to_thread(winsound.PlaySound, sBytes, winsound.SND_MEMORY)
            embed = discord.Embed(description="Playback finished", color=config.embedcolor)
            msgg = await interaction.channel.fetch_message(msg.message_id)
            await msgg.edit(embed=embed)
       except Exception as e:
          await Bot.error(interaction, Bot, e)


@app_commands.command(name="record", description="Record mic audio for givin duration")
async def command(interaction: discord.Interaction, duration: int = 5):
    try:
      if duration > 100 or duration < 0: # around 10mb for 100 seconds maybe?
          embed = discord.Embed(description=f"❌ | Duration can't be less than `0` or bigger than `100` seconds", color=config.embederrorcolor)
          await interaction.response.send_message(embed=embed, ephemeral=True)
          return
          
      rate = 44100
  
      embed = discord.Embed(description=f"Recording... please stand by", color=config.embedcolor)
      msgc = await interaction.response.send_message(embed=embed, delete_after=duration)
      recording = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
      sd.wait()  
      buff = BytesIO()
      with wave.open(buff, 'wb') as wf:
          wf.setnchannels(1)
          wf.setsampwidth(2)  # int16 for 2 bytes
          wf.setframerate(rate)
          wf.writeframes(recording.tobytes())
      buff.seek(0)  
      await interaction.followup.send(file=discord.File(buff, "recording.wav"), view=Play(buff, duration))
    except Exception as e:
      await Bot.error(interaction, Bot, e)
      
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    
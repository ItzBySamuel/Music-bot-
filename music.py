import discord
import youtube_dl
import os
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = '!')

@client.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("No estás conectado a ningun canal de voz", delete_after= 15)
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@client.command()
async def play(ctx, url : str):
    embed = discord.Embed(color= discord.Color.blue())
    embed.add_field(name = "Ahora sonando:", value= f'{url}', inline=False)
    embed.set_footer(icon_url= ctx.author.avatar_url, text= f'{ctx.author.name}')
    await ctx.send(embed=embed, delete_after= 200)
    await ctx.message.delete()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Espera a que la cancion actual termine o utiliza el comando stop ;)", delete_after= 30)
        return



    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def pause(ctx):
    await ctx.send('Cancion parada')
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@client.command()
async def resume(ctx):
    await ctx.send('Cancion en marcha :play_pause:', delete_after= 10)
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@client.command()
async def leave(ctx):
    await ctx.send('Canal dejado :wave:', delete_after= 10)
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command()
async def stop(ctx):
    await ctx.send('Cancion terminada')
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()
    
client.run('token')

import discord
import asyncio
import yt_dlp
import googleapiclient.discovery
import subprocess

# Function to load credentials from file
def read_text_file(filename):
    credentials = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                credentials[key] = value
    except FileNotFoundError:
        print(f"Credentials file not found: {filename}")
    except Exception as e:
        print(f"Error loading credentials: {e}")
    return credentials

# Load credentials
credentials_file_path = 'credentials.txt'
credentials = read_text_file(credentials_file_path)

DISCORD_TOKEN = credentials.get('DISCORD_TOKEN')
YOUTUBE_API_KEY = credentials.get('YOUTUBE_API_KEY')
VOICE_CHANNEL_ID = int(credentials.get('VOICE_CHANNEL_ID', 0))

# Define the path to the commands file
COMMANDS_FILE_PATH = 'commands.txt'

# Path to your YouTube cookies file
COOKIES_FILE_PATH = 'youtube_cookies.txt'


def start_monitor():
    import asyncio
    import os
    import tkinter as tk
    from tkinter import messagebox
    from TikTokLive import TikTokLiveClient
    from TikTokLive.events import CommentEvent, ConnectEvent, FollowEvent
    import threading

    class TikTokApp:
        def __init__(self, root):
            self.root = root
            self.root.title("TikTok Discord Request")
            self.root.geometry("400x300")

            # Remove window decorations
            self.root.overrideredirect(True)

            # Dark mode colors
            self.bg_color = "#2e2e2e"
            self.fg_color = "#ffffff"
            self.button_bg = "#4b4b4b"
            self.button_fg = "#ffffff"

            # Configure the main window
            self.root.configure(bg=self.bg_color)

            # Create a frame to hold the close button
            self.top_frame = tk.Frame(root, bg=self.bg_color, height=30)
            self.top_frame.pack(fill=tk.X, side=tk.TOP)

            # Add custom close button in the top frame
            self.close_button = tk.Button(self.top_frame, text="open discord", command=self.close_window, bg="#ff5c5c", fg=self.fg_color, bd=0, padx=10, pady=5)
            self.close_button.pack(side=tk.RIGHT)

            # Main content frame
            self.content_frame = tk.Frame(root, bg=self.bg_color)
            self.content_frame.pack(fill=tk.BOTH, expand=True)

            self.label = tk.Label(self.content_frame, text="Enter TikTok Username:", bg=self.bg_color, fg=self.fg_color)
            self.label.pack(pady=10)

            self.username_entry = tk.Entry(self.content_frame, width=40, bg="#3e3e3e", fg=self.fg_color, insertbackground=self.fg_color)
            self.username_entry.pack(pady=5)

            self.start_button = tk.Button(self.content_frame, text="Start Client", command=self.start_client, bg=self.button_bg, fg=self.button_fg)
            self.start_button.pack(pady=20)

            self.status_label = tk.Label(self.content_frame, text="Status: Not Connected", bg=self.bg_color, fg=self.fg_color)
            self.status_label.pack(pady=10)

            # Define the path to the commands file
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
            self.commands_file_path = os.path.join(self.script_dir, 'commands.txt')
            self.client_tiktok = None

            # Handle window drag (for moving the window)
            self.top_frame.bind("<Button-1>", self.start_move)
            self.top_frame.bind("<B1-Motion>", self.on_motion)

        def start_client(self):
            username = self.username_entry.get().strip()
            if not username:
                messagebox.showerror("Error", "Username cannot be empty")
                return

            self.status_label.config(text="Status: Connecting...")
            self.root.update_idletasks()  # Ensure the status update is processed

            # Create the TikTok client and run it in a separate thread
            self.client_tiktok = TikTokLiveClient(unique_id=username)
            self.client_tiktok.on(ConnectEvent)(self.on_connect)
            self.client_tiktok.on(CommentEvent)(self.on_comment)
            self.client_tiktok.on(FollowEvent)(self.on_follow)

            def run_client():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.client_tiktok.run())

            threading.Thread(target=run_client, daemon=True).start()

        async def on_connect(self, event: ConnectEvent):
            self.status_label.config(text=f"Connected to @{event.unique_id}")
            self.root.update()

        async def on_comment(self, event: CommentEvent) -> None:
            comment = event.comment.strip()
            print(f"Received comment: {comment}")  # Print the comment to the console

            if comment.startswith('!play'):
                query = comment[5:].strip()  # Extract query after !play
                print(f"Processing !play command with query: {query}")  # Print feedback for the !play command

                try:
                    with open(self.commands_file_path, 'a') as f:
                        f.write(query + '\n')
                except Exception as e:
                    print(f"An error occurred while writing to the commands file: {e}")

        async def on_follow(self, event: FollowEvent) -> None:
            print(f"{event.user.nickname} followed the streamer!")

        def close_window(self):
            self.root.quit()
            self.root.destroy()

        def start_move(self, event):
            self.root.x = event.x
            self.root.y = event.y

        def on_motion(self, event):
            delta_x = event.x - self.root.x
            delta_y = event.y - self.root.y
            new_x = self.root.winfo_x() + delta_x
            new_y = self.root.winfo_y() + delta_y
            self.root.geometry(f'+{new_x}+{new_y}')

    root = tk.Tk()
    app = TikTokApp(root)
    root.mainloop()

# Start monitor.pyw when the script starts
start_monitor()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)

queues = {}
voice_clients = {}
yt_dl_options = {
    "format": "bestaudio/best",
    "cookiefile": COOKIES_FILE_PATH
}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"'
}
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

async def read_commands():
    while True:
        try:
            with open(COMMANDS_FILE_PATH, 'r') as f:
                lines = f.readlines()
            if lines:
                with open(COMMANDS_FILE_PATH, 'w') as f:
                    f.writelines(lines[1:])  # Keep only new lines

                for query in lines:
                    query = query.strip()
                    if query:
                        for guild_id, voice_client in voice_clients.items():
                            try:
                                search_response = youtube.search().list(
                                    q=query,
                                    part="id,snippet",
                                    maxResults=1,
                                    type="video"
                                ).execute()

                                video_id = search_response['items'][0]['id']['videoId']
                                video_title = search_response['items'][0]['snippet']['title']
                                video_url = f"https://www.youtube.com/watch?v={video_id}"

                                data = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(video_url, download=False))

                                song = {
                                    'url': data['url'],
                                    'title': video_title,
                                    'requester': 'TikTok User',
                                    'channel': None
                                }

                                if guild_id in queues:
                                    queues[guild_id].append(song)
                                else:
                                    queues[guild_id] = [song]

                                if not voice_client.is_playing():
                                    await play_next_song(guild_id)
                            except Exception as e:
                                print(e)
        except FileNotFoundError:
            print(f"File not found: {COMMANDS_FILE_PATH}")
        except Exception as e:
            print(f"An error occurred while reading the commands file: {e}")
        await asyncio.sleep(3)  # Check every 3 seconds

async def play_next_song(guild_id):
    if guild_id in queues and queues[guild_id]:
        voice_client = voice_clients[guild_id]
        song = queues[guild_id].pop(0)
        player = discord.FFmpegOpusAudio(song['url'], **ffmpeg_options)
        voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(guild_id), client_discord.loop))
        
        embed = discord.Embed(title="Now Playing", description=f"[{song['title']}]({song['url']})", color=discord.Color.blue())
        embed.set_footer(text=f"Requested by {song['requester']}")
        if song['channel']:
            await song['channel'].send(embed=embed)

async def delete_message(message, delay=0.01):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except discord.Forbidden:
        print("Permission denied: Unable to delete message.")
    except discord.NotFound:
        print("Message not found: It might have been already deleted.")

@client_discord.event
async def on_ready():
    print(f'{client_discord.user} is now online')

    # Join the voice channel on startup
    for guild in client_discord.guilds:
        if VOICE_CHANNEL_ID:
            channel = guild.get_channel(VOICE_CHANNEL_ID)
            if isinstance(channel, discord.VoiceChannel):
                voice_client = await channel.connect()
                voice_clients[guild.id] = voice_client
                print(f"Joined voice channel: {channel.name}")
                break

    client_discord.loop.create_task(read_commands())

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    if message.content.startswith("-play"):
        try:
            if message.author.voice and message.author.voice.channel:
                if message.guild.id not in voice_clients:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients[message.guild.id] = voice_client
                else:
                    voice_client = voice_clients[message.guild.id]
            else:
                await message.channel.send("You are not connected to a voice channel.")
                await delete_message(message)
                return
        except Exception as e:
            print(e)

        try:
            query = ' '.join(message.content.split()[1:])
            search_response = youtube.search().list(
                q=query,
                part="id,snippet",
                maxResults=1,
                type="video"
            ).execute()

            video_id = search_response['items'][0]['id']['videoId']
            video_title = search_response['items'][0]['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            data = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(video_url, download=False))

            song = {
                'url': data['url'],
                'title': video_title,
                'requester': message.author.display_name,
                'channel': message.channel
            }

            if message.guild.id in queues:
                queues[message.guild.id].append(song)
            else:
                queues[message.guild.id] = [song]

            if not voice_clients[message.guild.id].is_playing():
                await play_next_song(message.guild.id)
            else:
                await message.channel.send(f"Added to queue: [{video_title}]({video_url})")
            await delete_message(message)
        except Exception as e:
            print(e)

    elif message.content.startswith("-pause"):
        try:
            if message.guild.id in voice_clients and voice_clients[message.guild.id].is_playing():
                voice_clients[message.guild.id].pause()
                await message.channel.send("PAUSED")
            else:
                await message.channel.send("No audio is currently playing.")
            await delete_message(message)
        except Exception as e:
            print(e)

    elif message.content.startswith("-resume"):
        try:
            if message.guild.id in voice_clients and voice_clients[message.guild.id].is_paused():
                voice_clients[message.guild.id].resume()
                await message.channel.send("RESUMED")
            else:
                await message.channel.send("No audio is currently paused.")
            await delete_message(message)
        except Exception as e:
            print(e)

    elif message.content.startswith("-stop"):
        try:
            if message.guild.id in voice_clients:
                voice_clients[message.guild.id].stop()
                await voice_clients[message.guild.id].disconnect()
                del voice_clients[message.guild.id]
                del queues[message.guild.id]
                await message.channel.send("Bye Bye")
            else:
                await message.channel.send("No audio is currently playing.")
            await delete_message(message)
        except Exception as e:
            print(e)

    elif message.content.startswith("-next"):
        try:
            if message.guild.id in voice_clients:
                voice_clients[message.guild.id].stop()
                await play_next_song(message.guild.id)
                await message.channel.send("Skipped")
            else:
                await message.channel.send("No audio is currently playing.")
            await delete_message(message)
        except Exception as e:
            print(e)

    elif message.content.startswith("-query"):
        try:
            if message.guild.id in queues and queues[message.guild.id]:
                embed = discord.Embed(title="Song Queue", color=discord.Color.blue())
                for i, song in enumerate(queues[message.guild.id], start=1):
                    embed.add_field(name=f"{i}. {song['title']}", value=f"Requested by {song['requester']}", inline=False)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Queue is empty.")
            await delete_message(message)
        except Exception as e:
            print(e)

    elif message.content.startswith("-command"):
        embed = discord.Embed(title="Available Commands", color=discord.Color.red())
        embed.add_field(name="-play [song]", value="Play the specified song or video.", inline=False)
        embed.add_field(name="-pause", value="Pause the current playback.", inline=False)
        embed.add_field(name="-resume", value="Resume the paused playback.", inline=False)
        embed.add_field(name="-stop", value="Stop the current playback and disconnect.", inline=False)
        embed.add_field(name="-next", value="Skip to the next song in the queue.", inline=False)
        embed.add_field(name="-query", value="Display the current song queue.", inline=False)
        await message.channel.send(embed=embed)
        await delete_message(message)

client_discord.run(DISCORD_TOKEN)
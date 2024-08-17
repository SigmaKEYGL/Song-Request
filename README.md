# TikTok Discord Request Bot - README

## Overview

This application seamlessly connects TikTok live streams with a Discord server, allowing TikTok viewers to request songs in real-time through comments. The bot then plays the requested songs in a designated Discord voice channel.

**Download:**  
You can download the executable from the [Releases tab](#) or via [MEGA](https://mega.nz/file/pn9mmTDS#zy9jis0jjGbClfXXO1W4QMC0zapLJZX8ghQRFyseF0Y).

## Setup & Usage

1. **Download the Executable**  
   Obtain the executable file tailored to your operating system.

2. **Run the Application**  
   Launch the application by double-clicking the executable file.

3. **Configuration**

   * **Initial Setup**  
     Enter the required credentials:

     - **Discord Bot Token**: Your Discord bot's token.
     - **YouTube API Key**: API key for YouTube data access.
     - **Voice Channel ID**: The ID of the voice channel where the bot will play songs.

4. **TikTok Username Entry**  
   A GUI will prompt you to enter the TikTok username to monitor.

5. **Commands**

   **TikTok Commands:**
   * `!play [song name]`  
     Viewers can request a song by typing this command in the TikTok live chat. The song will be added to the queue and played in the Discord server. Ensure the `commands.txt` file is in place for processing.

   **Discord Commands:**
   * `-play [song name]`  
     Play a song or add it to the queue.
   * `-pause`  
     Pause the currently playing song.
   * `-resume`  
     Resume the paused song.
   * `-stop`  
     Stop the song and disconnect the bot.
   * `-next`  
     Skip to the next song in the queue.
   * `-query`  
     Display the current song queue.
   * `-command`  
     Show a list of available commands.

* **Connection Issues**  
  Confirm that your Discord bot token, YouTube API key, and voice channel ID are correct and that the bot has the necessary permissions. If issues persist, try dragging the `credentials.txt` file into the executable.

## Contributing

If you encounter any issues or have suggestions for improvements, please reach out via the provided support channels.

## License

This application is licensed under the MIT License.

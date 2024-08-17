# TikTok Discord Request Bot - README

## Overview

This application connects TikTok live streams with a Discord server, allowing TikTok viewers to request songs through comments in real-time. The bot then plays the requested songs in a specified Discord voice channel.
Download the .exe in the releases tab. Or donwload it thorugh mega ; https://mega.nz/file/trdhRTzK#tbHUxicFcV_o2aWsCPm-tae6T3Fli9jX_A3ogO0Jlfg

## Setup & Usage

1. **Download the Executable**  
   Download the provided executable file for your operating system.

2. **Run the Application**  
   Simply double-click the executable file to start the application.

3. **Configuration**

   * **Initial Setup**  
     Enter the required credentials.

     You will need:
     * **Discord Bot Token**  
       The token for your Discord bot.
     * **YouTube API Key**  
       Your API key for accessing YouTube data.
     * **Voice Channel ID**  
       The ID of the voice channel where the bot will play songs.
      

4. **TikTok Username Entry**  
   The application will display a GUI where you can enter the TikTok username you want to monitor.

5. **Commands**

   **TikTok Commands:**
   * **!play [song name]**  
     Viewers can request a song by typing `!play [song name]` in the TikTok live chat. The song will be added to the queue and played in the Discord server. The commands.txt is needed to procces them.

   **Discord Commands:**
   * **-play [song name]**  
     Directly play a song or add it to the queue using this command in Discord.
   * **-pause**  
     Pause the currently playing song.
   * **-resume**  
     Resume a paused song.
   * **-stop**  
     Stop the song and disconnect the bot from the voice channel.
   * **-next**  
     Skip to the next song in the queue.
   * **-query**  
     Display the current song queue.
   * **-command**  
     Display a list of available commands.

## Troubleshooting

* **Executable Not Starting**  
  Ensure all required dependencies are installed. If using a Windows system, you may need to install the Visual C++ Redistributable.

* **Connection Issues**  
  Verify that your Discord bot token, YouTube API key, and voice channel ID are correct and that the bot has the necessary permissions. If none of that worked, drag the credentials.txt into the .exe

## Contributing

If you encounter any issues or have suggestions for improvements, please reach out through the provided support channels.

## License

This application is licensed under the MIT License.

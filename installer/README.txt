Scarlet Hollow Voice Override (AI-generated voices)

Adds spoken voices to Scarlet Hollow: the narrator and every character except the player.
ALL VOICES ARE AI-GENERATED (text-to-speech). Lines that contain the player's name or pronouns,
and the player's own lines, have no audio.

Install (Windows):
1. Extract this zip into the folder that contains ScarletHollow.exe. This puts
   game\zz_auto_voice.rpy in place and adds Install.bat and install_voices.ps1.
2. Double-click Install.bat and wait for "Install finished".
   It downloads about 14 GB of voice files (needs roughly twice that free while installing).
   If it stops, run Install.bat again and it carries on.
   At the end it prints how many voice files are in game\voice. If that number is 0, tell me.
3. Start the game. If you hear nothing, check the in-game volume settings.

The voices match the game version listed on the mod page. If the game updates, new or changed
lines will be silent until the voice pack is updated.

What Install.bat does: it runs install_voices.ps1 (plain text, open it to read it), which
downloads the voice files from a public Hugging Face dataset and unpacks them into game\voice.
It does not change anything else.

Uninstall: delete game\voice, game\voice_pack_state, game\zz_auto_voice.rpy and
game\zz_auto_voice.rpyc (the game creates the last one).

Source code and voice-generation scripts: (add your GitHub link here)
Voices were generated locally with Breeze-TTS-2; see its license for terms.

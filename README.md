# Scarlet Hollow Voice Override (AI voices)

An unofficial mod that adds AI-generated voice acting to **Scarlet Hollow**: the narrator and
every character except the player. The voices are generated with a text-to-speech model
(Breeze TTS server) from written character descriptions. **All audio is AI-generated.**

- Voice files (about 14 GB, 53,000 clips): https://huggingface.co/datasets/moond13/scarlet-hollow-voices
- Mod page: (add the Nexus Mods link here)

This repository contains the tools and the installer. It contains **no game files, no game
script text and no audio**.

## Not voiced
- The player's own lines.
- About 1,300 lines that contain the player's name or a pronoun variable (for example
  `[player_name]`), because those can't be spoken ahead of time.
- 18 "???" lines are still silent (17 with variables, 1 with no known speaker).

## Install (players)
1. Extract the mod zip from Nexus into the folder that contains `ScarletHollow.exe` (it adds `game\zz_auto_voice.rpy`, `Install.bat` and `install_voices.ps1`).
2. Run `Install.bat`. It downloads the voice files from Hugging Face into `game\voice`.
   Resumable: if it stops, run it again.
3. Start the game.

Needs Windows 10/11, an internet connection, about 14 GB to download and roughly twice that
free on the drive while installing.

## Folders
- `loader/game/zz_auto_voice.rpy` : the one-line Ren'Py script that makes the game play `game/voice/<line id>.wav`.
- `installer/` : `Install.bat`, `install_voices.ps1` (downloads and unpacks the voice zips), `README.txt`.
- `tools/` : the scripts used to make the voices.
  - `cast_data.py` : the cast list, voice descriptions, and which game speaker id uses which voice.
  - `cast_voices.py` : creates a saved voice on the TTS server for each cast member.
  - `batch_generate_all.py` : generates a clip for every line (needs `dialogue_dump.tsv`, see below).
  - `check_silent.py` : lists "???" lines that still have no clip.
  - `make_shards.py` / `upload_to_hf.py` : pack the clips into zips and upload them to Hugging Face.
  - `convert_to_ogg.py` : optional wav to ogg conversion.
  - `breeze_common.py` : shared helpers.
- `data/speaker_overrides.tsv` : line id to real speaker, for lines the game labels `speaker`, `unknown` or `extend`.

## Rebuilding the voices yourself
You need your own copy of Scarlet Hollow and a running Breeze TTS server.
1. Make `dialogue_dump.tsv` (columns: line id, speaker id, text) from your own copy of the game.
   It is not included here because it is the game's script.
2. Put `data/speaker_overrides.tsv` next to it.
3. Edit the folder paths at the top of `tools/breeze_common.py`.
4. `py cast_voices.py`, then `py batch_generate_all.py`, then `py check_silent.py`.

## Legal
Unofficial fan project, not affiliated with the Scarlet Hollow developers.
The voices are AI-generated and are not the voices of any real actor.
Scarlet Hollow and its characters belong to their owners.

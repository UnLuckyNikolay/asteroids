import os, random, pygame.mixer as mxr
from abc import ABC, abstractmethod
from enum import Enum


class SFX(Enum):
    """The list of all SFX. Values are dir paths."""

    PLAYER_PLASMA_SHOT = "player/plasma_shot/"
    PLAYER_DEATH = "player/death/"

class SFXManager:
    def __init__(self):
        mxr.init()
        self.volume = 0.6
        sfx_dir = "./sfx/sounds/"
        self.sfx_dict : dict[SFX, _SoundBase] = {}

        for sfx_enum in SFX:
            path = f"{sfx_dir}{sfx_enum.value}"
            match sfx_enum:
                case (
                    SFX.PLAYER_PLASMA_SHOT |
                    SFX.PLAYER_DEATH
                ):
                    self.sfx_dict[sfx_enum] = _SoundRandom(path)

    def play_sound(self, sound_enum : SFX):
        try:
            self.sfx_dict[sound_enum].play_sound(self.volume)
        except KeyError:
            print(f"ERROR: SFX.sfx_dict is missing {sound_enum}")


class _SoundBase:
    def __init__(self, dir_path):
        self.sounds : list[mxr.Sound] = []
        self.path = dir_path
        self._append_sound_files(dir_path)

    @abstractmethod
    def play_sound(self, volume):
        pass

    def _append_sound_files(self, dir_path):
        file_list = os.listdir(dir_path)
        for path in file_list:
            if os.path.splitext(path)[1] in (".wav", ".ogg", ".mp3"):
                full_path = f"{dir_path}{path}"
                print(f"Getting SFX file from `{full_path}`")
                self.sounds.append(mxr.Sound(full_path))


class _SoundRandom(_SoundBase):
    """Plays a random sound file from the chosen directory."""

    def __init__(self, dir_path):
        super().__init__(dir_path)

        self.last_i : int = -1

    def play_sound(self, volume):
        if len(self.sounds) == 0:
            print(f"ERROR: no sound for {self.path}")
            return
        
        if len(self.sounds) == 1:
            self.sounds[0].play()
            return
        
        i = random.randint(0, len(self.sounds)-1)
        if self.last_i == i:
            i = (i+1) % len(self.sounds)
        self.last_i = i
        
        sound = self.sounds[i]
        sound.set_volume(volume)
        print(f"Playing sound {i} at volume {sound.get_volume()}")
        sound.play()
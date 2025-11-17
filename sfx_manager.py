import os, random, pygame, pygame.mixer as mxr
from abc import ABC, abstractmethod
from enum import Enum


# New SFX should be added to:
# - SFXManager.sfx_dict match statement in _init_
class SFX(Enum):
    """The list of all SFX. Values are dir paths."""

    PLAYER_PLASMA_SHOT = "player/plasma_shot/"
    PLAYER_HIT = "player/hit/"
    PLAYER_DEATH = "player/death/"

    ASTEROID_EXPLOSION = "asteroid/explosion/"
    ORE_COLLECTED = "ore/"

    BUTTON_CLICK_SUCCESS = "button/click_successful/"
    BUTTON_CLICK_FAIL = "button/click_failed/"

    SECRET_CHEATS = "secret/cheats/"
    SECRET_UFO = "secret/ufo/"

# Additional OPTIONAL volume adjust for sounds.
_volume_adjust : dict [SFX, float] = {
    SFX.PLAYER_PLASMA_SHOT : 0.6,
    SFX.PLAYER_HIT : 0.8,
    SFX.PLAYER_DEATH : 0.8,
}

class SFXManager(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()

        mxr.init()

        self.volume = 0.6
        sfx_dir = "./_internal/sounds/"
        self.sfx_dict : dict[SFX, _SoundBase] = {}
        self.time : float = 0.0

        for sfx_enum in SFX:
            path = f"{sfx_dir}{sfx_enum.value}"

            match sfx_enum: # Add new enums here
                case (
                    SFX.PLAYER_PLASMA_SHOT |
                    SFX.PLAYER_HIT | 
                    SFX.PLAYER_DEATH |
                    SFX.BUTTON_CLICK_SUCCESS |
                    SFX.BUTTON_CLICK_FAIL |
                    SFX.ASTEROID_EXPLOSION | 
                    SFX.SECRET_CHEATS |
                    SFX.SECRET_UFO
                ):
                    self.sfx_dict[sfx_enum] = _SoundRandom(sfx_enum, path)

                case (
                    SFX.ORE_COLLECTED
                ):
                    self.sfx_dict[sfx_enum] = _SoundGrowingPitch(sfx_enum, path)

    def play_sound(self, sound_enum : SFX):
        try:
            sound = self.sfx_dict[sound_enum]
            if isinstance(sound, _SoundRandom):
                sound.play_sound(self.volume)
            elif isinstance(sound, _SoundGrowingPitch):
                sound.play_sound(self.volume, self.time)
        except KeyError:
            print(f"ERROR: SFX.sfx_dict is missing {sound_enum}")

    def update(self, delta : float):
        self.time += delta


class _SoundBase:
    def __init__(self, type_enum : SFX, dir_path : str):
        self.type : SFX = type_enum
        self.sounds : list[mxr.Sound] = []
        self.path : str = dir_path
        self._append_sound_files(dir_path)

    @abstractmethod
    def play_sound(self, volume):
        """Chooses which sound will be played."""

        pass

    def _append_sound_files(self, dir_path):
        file_list = sorted(os.listdir(dir_path))
        for path in file_list:
            if os.path.splitext(path)[1] in (".wav", ".ogg", ".mp3"):
                full_path = f"{dir_path}{path}"
                print(f"Getting SFX file from `{full_path}`")
                self.sounds.append(mxr.Sound(full_path))

    def _play_sound_inner(self, sound, volume):
        """Plays the sound with adjusted volume."""

        sound.set_volume(volume * _volume_adjust.get(self.type, 1))
        sound.play()


class _SoundRandom(_SoundBase):
    """Plays a random sound file from the chosen directory."""

    def __init__(self, type_enum : SFX, dir_path : str):
        super().__init__(type_enum, dir_path)

        self.last_i : int = -1

    def play_sound(self, volume):
        if len(self.sounds) == 0:
            print(f"ERROR: no sounds for {self.type}")
            return
        
        if len(self.sounds) == 1:
            self._play_sound_inner(self.sounds[0], volume)
            return
        
        i = random.randint(0, len(self.sounds)-1)
        if self.last_i == i:
            i = (i+1) % len(self.sounds)
        self.last_i = i
        
        sound = self.sounds[i]
        self._play_sound_inner(sound, volume)


class _SoundGrowingPitch(_SoundBase):
    """Plays a chain of sounds with increasing pitch."""

    def __init__(self, type_enum : SFX, dir_path : str):
        super().__init__(type_enum, dir_path)

        self.last_i : int = -1
        self.last_time : float = -1.0
        self.reset_timer = 2.0

    def play_sound(self, volume, time):
        if len(self.sounds) == 0:
            print(f"ERROR: no sounds for {self.type}")
            return
        
        if len(self.sounds) == 1:
            self._play_sound_inner(self.sounds[0], volume)
            return
        
        if time - self.last_time > self.reset_timer:
            sound = self.sounds[0]
            self.last_i = 0
        else:
            i = self.last_i+1
            if i >= len(self.sounds):
                i = len(self.sounds)-1
            sound = self.sounds[i]
            self.last_i = i
        self.last_time = time
        self._play_sound_inner(sound, volume)


# class _SoundCombined(_SoundBase):
#     """Plays all the sounds at once."""

#     def __init__(self, type_enum : SFX, dir_path : str):
#         super().__init__(type_enum, dir_path)

#     def play_sound(self, volume):
#         if len(self.sounds) == 0:
#             print(f"ERROR: no sounds for {self.type}")
#             return
        
#         for sound in self.sounds:
#             self._play_sound_inner(sound, volume)

from abc import ABC, abstractmethod


class MediaPlayable(ABC):
    @abstractmethod
    def play_media(self, file: str) -> None:
        pass

    @abstractmethod
    def stop_media(self) -> None:
        pass


class LyricsDisplayable(ABC):
    @abstractmethod
    def display_lyrics(self, file: str) -> None:
        pass


class VideoFilterable(ABC):
    @abstractmethod
    def apply_video_filter(self, filter: str) -> None:
        pass


class MusicPlayer(MediaPlayable, LyricsDisplayable):
    def play_media(self, file: str) -> None:
        print(f"Playing music: {file}")

    def stop_media(self) -> None:
        print("Stopping music")

    def display_lyrics(self, file: str) -> None:
        print(f"Displaying lyrics for: {file}")


class VideoPlayer(MediaPlayable, VideoFilterable):
    def play_media(self, file: str) -> None:
        print(f"Playing video: {file}")

    def stop_media(self) -> None:
        print("Stopping video")

    def apply_video_filter(self, filter: str) -> None:
        print(f"Applying video filter: {filter}")


class BasicAudioPlayer(MediaPlayable):
    def play_media(self, file: str) -> None:
        print(f"Playing audio: {file}")

    def stop_media(self) -> None:
        print("Stopping audio")

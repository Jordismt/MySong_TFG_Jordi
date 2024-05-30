from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import sys
import os
import requests
import tempfile


class ReproductorCanciones(QWidget):
    progress_changed = Signal(int)

    def __init__(self):
        super().__init__()
        
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)

        # Barra de progreso (QProgressBar)
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(
            "QProgressBar {border: 2px solid grey; border-radius: 5px; background-color: white;}"
            "QProgressBar::chunk {background-color: blue;}"
        )
        self.progress_bar.setRange(0, 100)

        self.pause_button = QPushButton()
        self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))

        # Control de volumen
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setToolTip("Control de Volumen")

        self.media_player.positionChanged.connect(self.actualizar_barra_progreso)
        self.media_player.durationChanged.connect(self.media_duration_changed)
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)
        self.media_player.playbackStateChanged.connect(self.handle_playback_state_changed)  # Manejo de la nueva señal
        self.current_temp_file = None



    def reproducir_cancion_url(self, cancion_id):
        self.detener()
        url = f"http://localhost:8181/canciones/stream/{cancion_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content
            self.reproducir_url(data)
        else:
            print("Error al obtener la canción")

    def reproducir_url(self, data):
        self.detener()  # Ensure any existing playback is stopped before starting new one
        if self.current_temp_file:
            os.unlink(self.current_temp_file.name)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.write(data)
        temp_file.close()
        self.current_temp_file = temp_file
        media_url = QUrl.fromLocalFile(temp_file.name)
        self.media_player.setSource(media_url)
        self.media_player.play()

    def pausar(self):
        print("Pausa presionada")
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            print("Estado del reproductor después de pausar:", self.media_player.playbackState())

    def detener(self):
        print("Detener presionado")
        self.media_player.stop()
        if self.current_temp_file:
            os.unlink(self.current_temp_file.name)
            self.current_temp_file = None
        print("Estado del reproductor después de detener:", self.media_player.playbackState())

    def continuar(self):
        print("Continuar presionado")
        if self.media_player.playbackState() != QMediaPlayer.PlayingState:
            self.media_player.play()
            print("Estado del reproductor después de continuar:", self.media_player.playbackState())

    def estado(self):
        estado = self.media_player.playbackState()
        print(f"Estado actual del reproductor: {estado}")
        return estado

    @Slot(int)
    def set_volume(self, value):
        print("Volumen:", value)
        self.audio_output.setVolume(value / 100.0)  # Ajuste del volumen

    @Slot(int)
    def actualizar_barra_progreso(self, position):
        duration = self.media_player.duration()
        if duration > 0:
            progress = int((position / duration) * 100)
            self.progress_bar.setValue(progress)

    @Slot()
    def media_duration_changed(self, duration):
        print("Duración de la media:", duration)
        print(f"estado {self.estado()}")

    @Slot(QMediaPlayer.MediaStatus)
    def handle_media_status(self, status):
        print("Estado de la media:", status)
        if status == QMediaPlayer.EndOfMedia:
            self.detener()

    @Slot(QMediaPlayer.PlaybackState)
    def handle_playback_state_changed(self, state):
        print("Estado de reproducción cambiado:", state)
        if state == QMediaPlayer.PausedState:
            print("Reproducción en pausa")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_menu = ReproductorCanciones()
    window_menu.show()
    sys.exit(app.exec())

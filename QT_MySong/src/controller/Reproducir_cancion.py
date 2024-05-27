from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QObject, Signal, Slot
import sys
import os
import requests
import tempfile



class ReproductorCanciones(QObject):

    progress_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        # Configurar el volumen del QAudioOutput
        self.audio_output.setVolume(1.0)
        
        # Establecer el QAudioOutput en el QMediaPlayer
        self.media_player.setAudioOutput(self.audio_output)

        # Conectar la señal positionChanged al método actualizar_barra_progreso
        self.media_player.positionChanged.connect(self.actualizar_barra_progreso)
        
        # Conectar la señal durationChanged al método media_duration_changed
        self.media_player.durationChanged.connect(self.media_duration_changed)
        
        # Almacenar el archivo temporal actual
        self.current_temp_file = None

    def reproducir_cancion_url(self, cancion_id):
        # Detener cualquier reproducción actual
        self.detener()

        # Hacer la llamada al endpoint del backend para obtener los datos de la canción
        url = f"http://localhost:8181/canciones/stream/{cancion_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content
            self.reproducir_url(data)
        else:
            print("Error al obtener la canción")

    def reproducir_url(self, data):
        # Crear un archivo temporal para almacenar los datos de la canción
        if self.current_temp_file:
            os.unlink(self.current_temp_file.name)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.write(data)
        temp_file.close()
        self.current_temp_file = temp_file

        # Crear una URL desde el archivo temporal
        media_url = QUrl.fromLocalFile(temp_file.name)

        # Establecer la fuente de medios en el QMediaPlayer
        self.media_player.setSource(media_url)

        # Conectar la señal de finalización de la reproducción para eliminar el archivo temporal
        self.media_player.mediaStatusChanged.connect(self.cleanup_temp_file)

        # Iniciar la reproducción
        self.media_player.play()

    def cleanup_temp_file(self, status):
        if status == QMediaPlayer.EndOfMedia and self.current_temp_file:
            os.unlink(self.current_temp_file.name)
            self.current_temp_file = None

    def reproducir(self, file_path):
        # Detener cualquier reproducción actual
        self.detener()

        url = QUrl.fromLocalFile(file_path)
        
        # Establecer la fuente de medios en el QMediaPlayer
        self.media_player.setSource(url)
        
        # Iniciar la reproducción
        self.media_player.play()

    def pausar(self):
        self.media_player.pause()
        print("Reproductor pausado")

    
    def detener(self):
        print("Detener presionado")
        if self.media_player.playbackState() in [QMediaPlayer.PlayingState, QMediaPlayer.PausedState]:
            self.media_player.stop()
            print("Reproductor detenido")
        else:
            print("El reproductor no está en estado de reproducción o pausa")

        if self.current_temp_file:
            os.unlink(self.current_temp_file.name)
            self.current_temp_file = None

    def continuar(self):
        if self.media_player.playbackState() == QMediaPlayer.PausedState:
            self.media_player.play()
            print("Reproducción continuada")
        else:
            print("El reproductor no está en estado de pausa")

    def estado(self):
        estado = self.media_player.playbackState()
        print(f"Estado actual del reproductor: {estado}")
        return estado
    
    def set_volume(self, value):
        print("Volumen: ", value)
        self.audio_output.setVolume(value / 100)
        
    @Slot()
    def actualizar_barra_progreso(self, position):
        print("Position:", position)
        duration = self.media_player.duration()
        if duration > 0:
            progress = int((position / duration) * 100)
            self.progress_changed.emit(progress)
            print("posicio en segons:  ", progress)
            
    @Slot()
    def media_duration_changed(self, duration):
        print("Duración de la media:", duration)

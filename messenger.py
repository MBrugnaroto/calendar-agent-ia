import uuid

import numpy as np
import sounddevice as sd

from threading import Thread
from scipy.io.wavfile import write
from datetime import datetime
from dataclasses import dataclass

from crew.agent import graph


@dataclass
class AudioInfo():
    name: str
    type: str
    path: str


def record_audio():
    audio_data = []
    recording = True
    sample_rate = 16000
    name = str(uuid.uuid1().hex) + (datetime.now().strftime("%Y%m%dT%H%M%S")) + ".wav"

    def record_audio():
        nonlocal audio_data, recording

        with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
            while recording:
                audio_chunk, _ = stream.read(1024)
                audio_data.append(audio_chunk)

    def stop_recording():
        input("Recording...")
        nonlocal recording
        recording = False

    start_record_thread = Thread(target=record_audio)
    start_record_thread.start()

    stop_record_thread = Thread(target=stop_recording)
    stop_record_thread.start()

    stop_record_thread.join()
    start_record_thread.join()

    audio_data = np.concatenate(audio_data, axis=0)

    write(f"calendar-agent-ia/media/audio/{name}", sample_rate, audio_data)

    return AudioInfo(
        name=name,
        type='audio',
        path="calendar-agent-ia/media/audio"
    )


def receive_message():
    while True:
        message = input("Você: ")
        if message.lower() == "sair":
            print("Encerrando o chat...", flush=True)
            break

        if message.lower() == "record":
            message = str(record_audio())

        output = graph.invoke({"messages": [message]})
        print(f"Assistente: {output['messages'][-1].content}")


if __name__ == "__main__":
    receive_message()

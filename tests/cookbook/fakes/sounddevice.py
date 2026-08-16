"""Deterministic microphone/speaker fixture for the voice cookbook."""

import numpy as np


_stream_count = 0


class InputStream:
    def __init__(self, samplerate, channels, dtype):
        del channels, dtype
        global _stream_count
        _stream_count += 1
        self.stream_number = _stream_count
        self.samplerate = samplerate
        self.read_count = 0

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, frames):
        self.read_count += 1
        # The first recording contains one speech chunk followed by enough
        # silence to finish VAD. The second recording contains no speech and
        # terminates the otherwise continuous demo cleanly.
        amplitude = 0.1 if self.stream_number == 1 and self.read_count == 1 else 0.0
        return np.full((frames, 1), amplitude, dtype=np.float32), False


def play(_audio, _sample_rate):
    return None


def wait():
    return None

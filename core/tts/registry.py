from core.tts.infer import TextToSpeech

_TTS_INSTANCES = {}


def get_tts(model_id: str):
    """
    Process-wide TTS singleton.
    """
    if model_id not in _TTS_INSTANCES:
        _TTS_INSTANCES[model_id] = TextToSpeech(model_id)
    return _TTS_INSTANCES[model_id]
DEFAULT_TTS_MODEL = "lightning-v3.1"

DEFAULT_STT_MODEL = "pulse"

# Lightning v2: supports 19 languages
TTSLanguages_lightning_v2 = [
    "en", "hi", "ta", "kn", "mr", "bn", "gu", "ar", "he", 
    "fr", "de", "pl", "ru", "it", "nl", "es", "sv", "ml", "te"
]
# Lightning v3.1: supports 4 languages
TTSLanguages_lightning_v3_1 = ["en", "hi", "ta", "es"]

# Available TTS Models
TTSModels = [
    "lightning-v2",
    "lightning-v3.1"
]

# STT Languages (Pulse model)
STTLanguages_pulse = [
    "it", "es", "en", "pt", "hi", "de", "fr", "uk", "ru", "kn", "ml", "pl",
    "mr", "gu", "cs", "sk", "te", "or", "nl", "bn", "lv", "et", "ro", "pa",
    "fi", "sv", "bg", "ta", "hu", "da", "lt", "mt", "multi"
]

# Available STT Models
STTModels = [
    "pulse"
]

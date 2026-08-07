"""Optional adapters for third-party voice-agent frameworks.

These are thin, lazy re-exports of the framework-native Smallest AI plugins, so you
can reach them from the SDK namespace without the core SDK depending on those
frameworks. Each adapter imports its framework only on first use and raises a clear
"install the extra" error otherwise.

    from smallestai.integrations.pipecat import SmallestSTTService   # needs smallestai[pipecat]
    from smallestai.integrations.livekit import TTS                  # needs smallestai[livekit]
"""

"""
J.A.R.V.I.S. Event Types
All event type constants used throughout the system.
"""

# Boot events
BOOT_CORE_STARTED = "boot.core.started"
BOOT_CORE_COMPLETE = "boot.core.complete"
BOOT_VOICE_STARTED = "boot.voice.started"
BOOT_VOICE_COMPLETE = "boot.voice.complete"
BOOT_BRAIN_STARTED = "boot.brain.started"
BOOT_BRAIN_COMPLETE = "boot.brain.complete"
BOOT_TOOLS_STARTED = "boot.tools.started"
BOOT_TOOLS_COMPLETE = "boot.tools.complete"
BOOT_UI_STARTED = "boot.ui.started"
BOOT_UI_COMPLETE = "boot.ui.complete"

# System events
JARVIS_READY = "jarvis.ready"
JARVIS_SHUTDOWN = "jarvis.shutdown"
JARVIS_STATE_CHANGED = "jarvis.state_changed"
JARVIS_ERROR = "jarvis.error"

# Voice events
VOICE_WAKE_WORD_DETECTED = "voice.wake_word_detected"
VOICE_COMMAND_RECEIVED = "voice.command_received"
VOICE_SLEEP_WORD_DETECTED = "voice.sleep_word_detected"
VOICE_RESPONSE_READY = "voice.response_ready"
VOICE_SPEAKING_STARTED = "voice.speaking.started"
VOICE_SPEAKING_COMPLETE = "voice.speaking.complete"

# Brain events
BRAIN_INTENT_CLASSIFIED = "brain.intent_classified"
BRAIN_RESPONSE_GENERATED = "brain.response_generated"
BRAIN_MEMORY_SAVED = "brain.memory_saved"
BRAIN_MEMORY_RECALLED = "brain.memory_recalled"

# Tool events
TOOL_SEARCH_STARTED = "tool.search.started"
TOOL_SEARCH_COMPLETE = "tool.search.complete"
TOOL_NEWS_FETCHED = "tool.news.fetched"
TOOL_WEATHER_FETCHED = "tool.weather.fetched"
TOOL_MAP_RENDERED = "tool.map.rendered"
TOOL_CAMERA_OPENED = "tool.camera.opened"
TOOL_CAMERA_CLOSED = "tool.camera.closed"

# UI events
UI_ARC_REACTOR_IDLE = "ui.arc_reactor.idle"
UI_ARC_REACTOR_AWAKE = "ui.arc_reactor.awake"
UI_ARC_REACTOR_LISTENING = "ui.arc_reactor.listening"
UI_ARC_REACTOR_THINKING = "ui.arc_reactor.thinking"
UI_ARC_REACTOR_SPEAKING = "ui.arc_reactor.speaking"
UI_ARC_REACTOR_TASK = "ui.arc_reactor.task"
UI_ARC_REACTOR_SLEEPING = "ui.arc_reactor.sleeping"
UI_ARC_REACTOR_ERROR = "ui.arc_reactor.error"
UI_TASK_OPENED = "ui.task.opened"
UI_TASK_CLOSED = "ui.task.closed"
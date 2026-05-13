"""
J.A.R.V.I.S. Name Registry
Defines wake words, sleep words, and assistant identity.
"""

WAKE_WORDS = [
    "wake up",
    "wake up jarvis",
    "jarvis wake up",
]

SLEEP_WORDS = [
    "sleep",
    "go to sleep",
    "rest",
    "stand by",
    "standby",
]

ASSISTANT_NAME = "J.A.R.V.I.S."
USER_TITLE = "Sir"
CREATOR_NAME = "Lord Vader"

RESPONSE_PREFIXES = [
    f"Yes, {USER_TITLE}.",
    f"At once, {USER_TITLE}.",
    f"Of course, {USER_TITLE}.",
    f"Right away, {USER_TITLE}.",
]
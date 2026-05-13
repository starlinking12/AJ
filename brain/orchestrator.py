"""
J.A.R.V.I.S. Brain Orchestrator
Central reasoning coordinator. Routes inputs through the full thinking pipeline:
Intent classification, LLM reasoning, tool execution, response generation.
"""

import asyncio
import time
from typing import Any, Dict, Optional, Callable

from brain.model_loader.ollama_client import OllamaClient
from brain.intent_classifier.classifier import IntentClassifier
from brain.prompt_engine.system_prompt import SystemPrompt
from brain.prompt_engine.context_assembler import ContextAssembler
from brain.memory.memory_manager import MemoryManager
from brain.task_planner import TaskPlanner
from brain.reflection_agent import ReflectionAgent
from brain.fallback_manager import FallbackManager
from brain.handoff.handoff_manager import HandoffManager
from brain.guardrails.output_validator import OutputValidator

from jarvis_core.logger import Logger
from jarvis_core.events.event_bus import EventBus


class BrainOrchestrator:
    """
    Master coordinator for all brain functions.
    Takes transcribed text input, thinks, and returns response text.
    """

    def __init__(self, config, event_bus: EventBus):
        self.log = Logger("BrainOrchestrator")
        self.config = config
        self.event_bus = event_bus

        self.llm = OllamaClient(config)
        self.intent_classifier = IntentClassifier()
        self.system_prompt = SystemPrompt()
        self.context_assembler = ContextAssembler()
        self.memory = MemoryManager()
        self.task_planner = TaskPlanner()
        self.reflection = ReflectionAgent(self.llm)
        self.fallback = FallbackManager()
        self.handoff = HandoffManager(event_bus)
        self.validator = OutputValidator()

        self._initialized = False
        self._on_response: Optional[Callable] = None
        self._on_action: Optional[Callable] = None

    def initialize(self) -> bool:
        self.log.info("Initializing brain...")

        try:
            if not self.llm.initialize():
                self.log.error("LLM initialization failed.")
                return False

            self.intent_classifier.initialize()
            self.memory.initialize()
            self.task_planner.initialize()
            self.validator.initialize()

            self._initialized = True
            self.log.info("Brain ready.")
            self.event_bus.emit("brain.ready", {})
            return True

        except Exception as e:
            self.log.error(f"Brain init failed: {e}")
            return False

    def set_callbacks(
        self,
        on_response: Optional[Callable] = None,
        on_action: Optional[Callable] = None
    ) -> None:
        self._on_response = on_response
        self._on_action = on_action

    def process(self, user_text: str, user_id: str = "lord_vader") -> Dict[str, Any]:
        """
        Process user input through the full reasoning pipeline.
        Returns a dict with response text and any actions to execute.
        """
        start_time = time.time()

        self.event_bus.emit("brain.processing_started", {"text": user_text})

        # Step 1: Classify intent
        intent = self.intent_classifier.classify(user_text)
        self.event_bus.emit("brain.intent_classified", {"intent": intent})

        # Step 2: Retrieve relevant memories
        memories = self.memory.retrieve_relevant(user_text, user_id)

        # Step 3: Assemble context
        context = self.context_assembler.build(
            user_text=user_text,
            intent=intent,
            memories=memories,
            user_id=user_id
        )

        # Step 4: Generate system prompt
        system_prompt = self.system_prompt.get_prompt(intent=intent)

        # Step 5: Plan tasks if needed
        tasks = self.task_planner.plan(user_text, intent)

        # Step 6: Get LLM response
        response = self.llm.generate(
            system_prompt=system_prompt,
            user_message=user_text,
            context=context
        )

        # Step 7: Reflect and refine
        if self.reflection.should_reflect(response):
            response = self.reflection.refine(response, user_text)

        # Step 8: Validate output
        response = self.validator.validate(response)

        # Step 9: Save to memory
        self.memory.save_interaction(
            user_id=user_id,
            user_text=user_text,
            response=response,
            intent=intent
        )

        # Step 10: Handle any actions
        actions = self.task_planner.get_actions()
        if actions and self._on_action:
            for action in actions:
                self._on_action(action)

        elapsed = time.time() - start_time
        self.log.info(f"Processing complete in {elapsed:.2f}s")

        result = {
            "text": response,
            "intent": intent,
            "actions": actions,
            "elapsed_ms": int(elapsed * 1000),
        }

        if self._on_response:
            self._on_response(result)

        self.event_bus.emit("brain.response_generated", result)
        return result

    def process_async(self, user_text: str, user_id: str = "lord_vader"):
        """Async wrapper for processing."""
        import threading
        result_container = {}

        def run():
            result_container["result"] = self.process(user_text, user_id)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        thread.join(timeout=30)

        return result_container.get("result", {})

    def shutdown(self) -> None:
        self.memory.close()
        self.llm.close()
        self.log.info("Brain shutdown complete.")
"""Tests for memory systems."""

import pytest
from brain.memory.short_term import ShortTermMemory
from brain.memory.working_memory import WorkingMemory
from brain.memory.cache_layer import CacheLayer


class TestShortTermMemory:
    def test_add_and_retrieve(self):
        stm = ShortTermMemory(max_turns=10)
        stm.add("user1", "Hello", "Hi Sir.")
        recent = stm.get_recent("user1", limit=5)
        assert len(recent) >= 1

    def test_max_turns(self):
        stm = ShortTermMemory(max_turns=4)
        for i in range(10):
            stm.add("user1", f"msg{i}", f"response{i}")
        recent = stm.get_recent("user1", limit=20)
        assert len(recent) <= 8

    def test_clear(self):
        stm = ShortTermMemory()
        stm.add("user1", "Hello", "Hi.")
        stm.clear("user1")
        recent = stm.get_recent("user1")
        assert len(recent) == 0

    def test_multiple_users(self):
        stm = ShortTermMemory()
        stm.add("user1", "Hello", "Hi Sir.")
        stm.add("user2", "Hi", "Hello Sir.")
        assert len(stm.get_recent("user1")) > 0
        assert len(stm.get_recent("user2")) > 0


class TestWorkingMemory:
    def test_set_and_get(self):
        wm = WorkingMemory()
        wm.set("key", "value")
        assert wm.get("key") == "value"

    def test_default_value(self):
        wm = WorkingMemory()
        assert wm.get("nonexistent", "default") == "default"

    def test_task_context(self):
        wm = WorkingMemory()
        wm.set_task("search", {"query": "test"})
        assert wm.get_active_task() == "search"
        assert wm.get_task_context()["query"] == "test"

    def test_clear_task(self):
        wm = WorkingMemory()
        wm.set_task("search", {})
        wm.clear_task()
        assert wm.get_active_task() is None


class TestCacheLayer:
    def test_set_and_get(self):
        cache = CacheLayer(default_ttl=60)
        cache.set("key", "value")
        assert cache.get("key") == "value"

    def test_expiry(self):
        cache = CacheLayer(default_ttl=0)
        cache.set("key", "value")
        import time
        time.sleep(0.1)
        assert cache.get("key") is None

    def test_delete(self):
        cache = CacheLayer()
        cache.set("key", "value")
        cache.delete("key")
        assert cache.get("key") is None

    def test_clear(self):
        cache = CacheLayer()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert cache.get("a") is None
        assert cache.get("b") is None
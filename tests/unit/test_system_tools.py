"""Tests for system tools."""

import pytest
from tools.system.shell_executor import ShellExecutor
from tools.system.file_operations import FileOperations
from brain.guardrails.command_sanitizer import CommandSanitizer


class TestCommandSanitizer:
    def test_allowed_command(self):
        cs = CommandSanitizer()
        command, allowed = cs.sanitize("echo hello")
        assert allowed is True

    def test_blocked_injection(self):
        cs = CommandSanitizer()
        command, allowed = cs.sanitize("echo hello; rm -rf /")
        assert allowed is False

    def test_unknown_command(self):
        cs = CommandSanitizer()
        command, allowed = cs.sanitize("unknown_command")
        assert allowed is False

    def test_escape_argument(self):
        cs = CommandSanitizer()
        result = cs.escape_argument("hello world")
        assert '"' in result


class TestShellExecutor:
    def test_initialize(self):
        se = ShellExecutor()
        assert se.initialize() is True

    def test_blocked_command(self):
        se = ShellExecutor()
        se.initialize()
        result = se.execute("rm -rf /")
        assert result["success"] is False

    def test_allowed_command(self):
        se = ShellExecutor()
        se.initialize()
        result = se.execute("echo hello")
        assert result["success"] is True
        assert "hello" in result.get("stdout", "")


class TestFileOperations:
    def test_initialize(self):
        fo = FileOperations()
        assert fo.initialize() is True

    def test_read_nonexistent_file(self):
        fo = FileOperations()
        fo.initialize()
        result = fo.read_file("/tmp/nonexistent_jarvis_test_file.txt")
        assert result is None

    def test_write_and_read(self, tmp_path):
        fo = FileOperations()
        fo.initialize()
        test_file = str(tmp_path / "test.txt")
        fo.write_file(test_file, "Hello Sir.")
        content = fo.read_file(test_file)
        assert content == "Hello Sir."

    def test_list_directory(self, tmp_path):
        fo = FileOperations()
        fo.initialize()
        items = fo.list_directory(str(tmp_path))
        assert isinstance(items, list)
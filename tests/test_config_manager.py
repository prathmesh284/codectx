"""Tests for CodeCtx configuration manager."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from codectx.config_manager import ConfigManager, get_config_manager, reset_config_manager

TEST_TEMP_ROOT = Path.cwd().resolve() / ".tmp-tests"
TEST_TEMP_ROOT.mkdir(exist_ok=True)


class ConfigManagerTests(unittest.TestCase):
    """Test suite for ConfigManager."""

    def tearDown(self) -> None:
        reset_config_manager()

    def make_tempdir(self) -> Path:
        """Create a temporary directory inside the writable workspace."""
        return Path(tempfile.mkdtemp(dir=TEST_TEMP_ROOT))

    def test_creates_config_dir_and_plugins_dir(self) -> None:
        tmpdir = self.make_tempdir()
        self.addCleanup(shutil.rmtree, tmpdir, True)
        with patch.dict("os.environ", {"CODECTX_CONFIG_DIR": str(tmpdir)}, clear=False):
            manager = ConfigManager()

        self.assertTrue(tmpdir.exists())
        self.assertEqual(manager.get_plugins_dir(), tmpdir.resolve() / "plugins")
        self.assertTrue(manager.get_plugins_dir().exists())

    def test_creates_default_config_file(self) -> None:
        tmpdir = self.make_tempdir()
        self.addCleanup(shutil.rmtree, tmpdir, True)
        with patch.dict("os.environ", {"CODECTX_CONFIG_DIR": str(tmpdir)}, clear=False):
            manager = ConfigManager()

        config_file = tmpdir / "config.json"
        self.assertTrue(config_file.exists())
        self.assertEqual(manager.config_file, config_file.resolve())

        with config_file.open("r", encoding="utf-8") as handle:
            config = json.load(handle)

        self.assertIn("project_root", config)
        self.assertIn("output_file", config)
        self.assertIn("ignore_dirs", config)

    def test_environment_variable_overrides_default_path(self) -> None:
        tmpdir = self.make_tempdir()
        self.addCleanup(shutil.rmtree, tmpdir, True)
        custom_dir = tmpdir / "nested-config"
        with patch.dict(
            "os.environ",
            {"CODECTX_CONFIG_DIR": f"  {custom_dir}  "},
            clear=False,
        ):
            manager = ConfigManager()

        self.assertEqual(manager.get_config_dir(), custom_dir.resolve())

    def test_load_and_update_config(self) -> None:
        tmpdir = self.make_tempdir()
        self.addCleanup(shutil.rmtree, tmpdir, True)
        with patch.dict("os.environ", {"CODECTX_CONFIG_DIR": str(tmpdir)}, clear=False):
            manager = ConfigManager()
            manager.update_config("verbose", True)
            config = manager.load_config()

        self.assertTrue(config["verbose"])
        self.assertEqual(manager.get("project_root", "./"), "./")

    def test_singleton_can_be_reset_between_environment_changes(self) -> None:
        first_dir = self.make_tempdir()
        second_dir = self.make_tempdir()
        self.addCleanup(shutil.rmtree, first_dir, True)
        self.addCleanup(shutil.rmtree, second_dir, True)
        with patch.dict("os.environ", {"CODECTX_CONFIG_DIR": str(first_dir)}, clear=False):
            first = get_config_manager()
            second = get_config_manager()

        self.assertIs(first, second)
        self.assertEqual(first.get_config_dir(), first_dir.resolve())

        reset_config_manager()

        with patch.dict("os.environ", {"CODECTX_CONFIG_DIR": str(second_dir)}, clear=False):
            third = get_config_manager()

        self.assertEqual(third.get_config_dir(), second_dir.resolve())
        self.assertIsNot(first, third)


if __name__ == "__main__":
    unittest.main()

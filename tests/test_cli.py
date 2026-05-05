"""Tests for CodeCtx CLI."""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from codectx.cli import CLIHandler
from codectx.config_manager import reset_config_manager

TEST_TEMP_ROOT = Path.cwd().resolve() / ".tmp-tests"
TEST_TEMP_ROOT.mkdir(exist_ok=True)


class CLIHandlerTests(unittest.TestCase):
    """Test suite for CLI behavior."""

    def setUp(self) -> None:
        reset_config_manager()
        self._env_patcher = patch.dict(
            os.environ,
            {"CODECTX_CONFIG_DIR": str(TEST_TEMP_ROOT / "config")},
            clear=False,
        )
        self._env_patcher.start()

    def tearDown(self) -> None:
        self._env_patcher.stop()
        reset_config_manager()

    def make_tempdir(self) -> Path:
        """Create a temporary directory inside the writable workspace."""
        return Path(tempfile.mkdtemp(dir=TEST_TEMP_ROOT))

    def test_cli_handler_initializes_expected_components(self) -> None:
        handler = CLIHandler()
        self.assertIsNotNone(handler.parser)
        self.assertIsNotNone(handler.analysis_service)
        self.assertIsNotNone(handler.fs_service)

    def test_legacy_mode_path_is_rewritten_to_analyze_command(self) -> None:
        handler = CLIHandler()
        handler.handle_project_analysis = MagicMock()

        handler.run(["."])

        handler.handle_project_analysis.assert_called_once_with(
            ".",
            use_reload=False,
            verbose=False,
        )

    def test_plugin_list_command_routes_to_plugin_handler(self) -> None:
        handler = CLIHandler()
        handler.handle_plugin_list = MagicMock()

        handler.run(["plugin", "list"])

        handler.handle_plugin_list.assert_called_once_with(None)

    def test_project_analysis_uses_services_and_writer(self) -> None:
        tmpdir = self.make_tempdir()
        self.addCleanup(shutil.rmtree, tmpdir, True)
        project_file = tmpdir / "example.py"
        project_file.write_text("def hello():\n    return 'world'\n", encoding="utf-8")

        handler = CLIHandler()
        handler.fs_service.scan_project = MagicMock(return_value=[str(project_file)])
        fake_context = MagicMock()
        fake_context.plugins = {}
        handler.analysis_service.analyze_project = MagicMock(return_value=fake_context)

        with patch("codectx.cli.write_output") as mock_write_output:
            handler.handle_project_analysis(str(tmpdir), use_reload=True, verbose=False)

        handler.fs_service.scan_project.assert_called_once_with(str(tmpdir))
        handler.analysis_service.analyze_project.assert_called_once_with(
            [str(project_file)],
            str(tmpdir),
            use_reload=True,
        )
        mock_write_output.assert_called_once_with(fake_context, "project.ctx.json")


if __name__ == "__main__":
    unittest.main()

import subprocess
import tempfile
from pathlib import Path

import pytest
from fake import FAKER

import git_dump_diff

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "temp_git_repo",
    "test_build_tree_lines",
    "test_dashed_block",
    "test_get_changed_files",
    "test_is_binary",
    "test_main_integration",
    "test_main_invalid_format",
    "test_main_no_args",
    "test_main_no_differences",
    "test_main_version",
    "test_run_command_failure",
    "test_run_command_success",
    "test_section_header",
)


@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository with branches and files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Initialize git repo
        subprocess.run(
            ["git", "init"], cwd=repo_path, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo_path,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo_path,
            check=True,
        )

        # Create default branch with README.md and LICENSE
        readme_md = repo_path / "README.md"
        readme_md.write_text(FAKER.text())

        license_file = repo_path / "LICENSE"
        license_file.write_text(FAKER.text())

        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "branch", "-M", "main"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )

        # Create feature branch
        subprocess.run(
            ["git", "checkout", "-b", "feature"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )

        # Remove README.md
        readme_md.unlink()
        subprocess.run(
            ["git", "rm", "README.md"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )

        # Add README.rst
        readme_rst = repo_path / "README.rst"
        readme_rst.write_text(FAKER.text())
        subprocess.run(["git", "add", "README.rst"], cwd=repo_path, check=True)

        # Add other files
        (repo_path / "config.py").write_text(f"CONFIG = '{FAKER.word()}'")
        (repo_path / "utils.py").write_text(
            f"def helper(): return '{FAKER.word()}'"
        )
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Feature changes"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )

        yield repo_path


def test_get_changed_files(temp_git_repo, monkeypatch):
    """Test get_changed_files returns correct file statuses."""
    monkeypatch.chdir(temp_git_repo)
    result = git_dump_diff.get_changed_files("main", "feature")

    assert "README.md" in result
    assert result["README.md"] == "REMOVED"
    assert "README.rst" in result
    assert result["README.rst"] == "ADDED"
    assert "config.py" in result
    assert result["config.py"] == "ADDED"
    assert "utils.py" in result
    assert result["utils.py"] == "ADDED"


def test_build_tree_lines():
    """Test build_tree_lines creates correct tree structure."""
    changed_files = {
        "README.md": "REMOVED",
        "README.rst": "ADDED",
        "config.py": "ADDED",
    }
    lines = git_dump_diff.build_tree_lines("test-repo", changed_files)

    assert lines[0] == "test-repo/"
    assert any("README.md" in line and "REMOVED" in line for line in lines)
    assert any("README.rst" in line and "ADDED" in line for line in lines)
    assert any("config.py" in line and "ADDED" in line for line in lines)


def test_is_binary(temp_git_repo, monkeypatch):
    """Test is_binary correctly identifies text files."""
    monkeypatch.chdir(temp_git_repo)
    assert not git_dump_diff.is_binary("main", "feature", "README.rst")
    assert not git_dump_diff.is_binary("main", "feature", "config.py")


def test_section_header():
    """Test section_header formatting."""
    result = git_dump_diff.section_header("Test Title")
    assert "Test Title" in result
    assert result.startswith("# *")
    assert result.count("\n") == 2


def test_dashed_block():
    """Test dashed_block formatting."""
    result = git_dump_diff.dashed_block("Test Label")
    assert "Test Label" in result
    assert result.startswith("# -")
    assert result.count("\n") == 2


def test_run_command_success():
    """Test run_command with successful command."""
    result = git_dump_diff.run_command("echo test")
    assert result == "test"


def test_run_command_failure():
    """Test run_command with failing command."""
    result = git_dump_diff.run_command("false")
    assert result is None


def test_main_integration(temp_git_repo, capsys, monkeypatch):
    """Test main function end-to-end."""
    monkeypatch.chdir(temp_git_repo)
    monkeypatch.setattr("sys.argv", ["git-dump-diff", "main..feature"])

    git_dump_diff.main()

    captured = capsys.readouterr()
    assert "Affected files structure" in captured.out
    assert "Changes" in captured.out
    assert "README.md" in captured.out
    assert "README.rst" in captured.out
    assert "config.py" in captured.out
    assert "utils.py" in captured.out


def test_main_no_differences(temp_git_repo, capsys, monkeypatch):
    """Test main when no differences exist."""
    monkeypatch.chdir(temp_git_repo)
    monkeypatch.setattr("sys.argv", ["git-dump-diff", "main..main"])

    git_dump_diff.main()

    captured = capsys.readouterr()
    assert "No differences found." in captured.out


def test_main_version(capsys, monkeypatch):
    """Test --version flag."""
    monkeypatch.setattr("sys.argv", ["git-dump-diff", "--version"])

    with pytest.raises(SystemExit) as exc:
        git_dump_diff.main()

    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "version" in captured.out


def test_main_no_args(capsys, monkeypatch):
    """Test main with no arguments."""
    monkeypatch.setattr("sys.argv", ["git-dump-diff"])

    with pytest.raises(SystemExit) as exc:
        git_dump_diff.main()

    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "Usage" in captured.out


def test_main_invalid_format(capsys, monkeypatch):
    """Test main with invalid argument format."""
    monkeypatch.setattr("sys.argv", ["git-dump-diff", "invalid"])

    with pytest.raises(SystemExit) as exc:
        git_dump_diff.main()

    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.out

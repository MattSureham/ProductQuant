from __future__ import annotations

import os
import stat
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier

import pytest

from productquant import uci
from productquant.errors import StateError


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission contract")
def test_private_tree_preserves_existing_modes_and_privates_only_new_paths(
    tmp_path: Path,
) -> None:
    data_root = tmp_path / "existing-root"
    existing_child = data_root / "existing-child"
    existing_child.mkdir(parents=True)
    data_root.chmod(0o755)
    existing_child.chmod(0o751)
    target = existing_child / "new-private" / "leaf"

    uci.ensure_private_data_tree(data_root, target)

    assert stat.S_IMODE(data_root.stat().st_mode) == 0o755
    assert stat.S_IMODE(existing_child.stat().st_mode) == 0o751
    assert stat.S_IMODE((existing_child / "new-private").stat().st_mode) == 0o700
    assert stat.S_IMODE(target.stat().st_mode) == 0o700


@pytest.mark.parametrize(
    "target_kind", ["file", "empty-directory", "nonempty-directory", "symlink"]
)
def test_atomic_directory_publication_never_replaces_existing_entry(
    tmp_path: Path,
    target_kind: str,
) -> None:
    stage = tmp_path / "stage"
    stage.mkdir()
    (stage / "complete.txt").write_text("complete", encoding="utf-8")
    destination = tmp_path / "final"
    if target_kind == "file":
        destination.write_text("competitor", encoding="utf-8")
    elif target_kind in {"empty-directory", "nonempty-directory"}:
        destination.mkdir()
        if target_kind == "nonempty-directory":
            (destination / "competitor.txt").write_text("competitor", encoding="utf-8")
    else:
        destination.symlink_to(tmp_path / "missing-competitor")
    before = destination.lstat()

    with pytest.raises(StateError, match="appeared during publication"):
        uci.atomic_publish_directory(stage, destination)

    after = destination.lstat()
    assert (after.st_dev, after.st_ino, after.st_mode) == (
        before.st_dev,
        before.st_ino,
        before.st_mode,
    )
    assert stage.is_dir()
    if target_kind == "file":
        assert destination.read_text(encoding="utf-8") == "competitor"
    elif target_kind == "symlink":
        assert destination.readlink() == tmp_path / "missing-competitor"
    elif target_kind == "nonempty-directory":
        assert (destination / "competitor.txt").read_text(encoding="utf-8") == (
            "competitor"
        )


def test_atomic_directory_publication_fails_safely_if_target_appears_at_commit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stage = tmp_path / "stage"
    stage.mkdir()
    (stage / "complete.txt").write_text("complete", encoding="utf-8")
    destination = tmp_path / "final"
    original = uci._rename_noreplace

    def appear_then_publish(source: Path, target: Path) -> None:
        target.write_text("late competitor", encoding="utf-8")
        original(source, target)

    monkeypatch.setattr(uci, "_rename_noreplace", appear_then_publish)

    with pytest.raises(StateError, match="appeared during publication"):
        uci.atomic_publish_directory(stage, destination)

    assert destination.read_text(encoding="utf-8") == "late competitor"
    assert stage.is_dir()


def test_atomic_directory_publication_precommit_failure_leaves_no_final(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stage = tmp_path / "stage"
    stage.mkdir()
    destination = tmp_path / "final"
    monkeypatch.setattr(
        uci,
        "_rename_noreplace",
        lambda *_args: (_ for _ in ()).throw(StateError("injected precommit failure")),
    )

    with pytest.raises(StateError, match="injected precommit failure"):
        uci.atomic_publish_directory(stage, destination)

    assert stage.is_dir()
    assert not uci._path_entry_exists(destination)


def test_atomic_directory_publication_postcommit_sync_failure_leaves_complete_final(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stage = tmp_path / "stage"
    stage.mkdir()
    (stage / "complete.txt").write_text("complete", encoding="utf-8")
    destination = tmp_path / "final"
    monkeypatch.setattr(
        uci,
        "fsync_directory",
        lambda *_args: (_ for _ in ()).throw(OSError("injected sync failure")),
    )

    with pytest.raises(StateError, match="directory sync failed"):
        uci.atomic_publish_directory(stage, destination)

    assert not uci._path_entry_exists(stage)
    assert destination.is_dir() and not destination.is_symlink()
    assert (destination / "complete.txt").read_text(encoding="utf-8") == "complete"


def test_concurrent_directory_publishers_produce_one_complete_winner(
    tmp_path: Path,
) -> None:
    stages = [tmp_path / "stage-a", tmp_path / "stage-b"]
    for index, stage in enumerate(stages):
        stage.mkdir()
        (stage / "winner.txt").write_text(str(index), encoding="utf-8")
    destination = tmp_path / "final"
    barrier = Barrier(2)

    def publish(stage: Path) -> str:
        barrier.wait()
        try:
            uci.atomic_publish_directory(stage, destination)
        except StateError:
            return "conflict"
        return "published"

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(publish, stages))

    assert sorted(outcomes) == ["conflict", "published"]
    assert destination.is_dir() and not destination.is_symlink()
    assert (destination / "winner.txt").read_text(encoding="utf-8") in {"0", "1"}


def _git_init(path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(path)], check=True)


def test_unignored_in_worktree_data_root_fails_before_network_or_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _git_init(repository)
    data_root = repository / "trackable-data"
    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: pytest.fail("privacy guard opened the network"),
    )

    with pytest.raises(StateError, match="not fully Git-ignored"):
        uci.fetch(data_root)

    assert not data_root.exists()


@pytest.mark.skipif(os.name != "posix", reason="mode-preservation assertion")
def test_final_files_only_ignore_rules_do_not_cover_staging_or_pass_policy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: object,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _git_init(repository)
    data_root = repository / "granular-data"
    data_root.mkdir()
    data_root.chmod(0o755)
    representatives = (
        uci.raw_directory(data_root) / uci.ARCHIVE_NAME,
        uci.raw_directory(data_root) / "manifest.json",
        uci.normalized_directory(data_root) / "events.parquet",
        uci.normalized_directory(data_root) / "manifest.json",
        uci.receipts_directory(data_root) / "productquant-ignore-probe.json",
    )
    (repository / ".gitignore").write_text(
        "".join(f"/{path.relative_to(repository)}\n" for path in representatives),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: pytest.fail("privacy guard opened the network"),
    )

    with pytest.raises(StateError, match="not fully Git-ignored"):
        uci.fetch(data_root)

    assert stat.S_IMODE(data_root.stat().st_mode) == 0o755
    assert not (data_root / "raw").exists()
    assert {path.name for path in data_root.iterdir()} == set()


def test_ignored_in_worktree_custom_data_root_is_allowed(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _git_init(repository)
    (repository / ".gitignore").write_text("/private-data/\n", encoding="utf-8")
    data_root = repository / "private-data"

    uci.ensure_private_data_tree(data_root, data_root / "raw" / "source")

    assert (data_root / "raw" / "source").is_dir()

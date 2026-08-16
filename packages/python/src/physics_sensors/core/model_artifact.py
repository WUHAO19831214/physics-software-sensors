"""Explicit external model artifact metadata and local-file verification."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


@dataclass(frozen=True)
class ModelArtifact:
    """A model reference; the sensor package never treats weights as sensor code."""

    model_id: str
    model_family: str
    uri: str
    sha256: str
    runtime: str
    runtime_version: str
    class_names: tuple[str, ...]
    license_state: str

    def __post_init__(self) -> None:
        if not self.model_id or not self.model_family or not self.uri:
            raise ValueError("model_id, model_family, and uri are required")
        digest = self.sha256.lower()
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise ValueError("sha256 must be a 64-character hexadecimal digest")
        object.__setattr__(self, "sha256", digest)
        if not self.runtime or not self.runtime_version:
            raise ValueError("runtime and runtime_version are required")
        if not self.license_state:
            raise ValueError("license_state is required and must not be guessed")
        if len(set(self.class_names)) != len(self.class_names):
            raise ValueError("class_names must be unique")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ModelArtifact":
        names = value.get("class_names", ())
        if not isinstance(names, Sequence) or isinstance(names, (str, bytes)):
            raise ValueError("class_names must be an array of strings")
        return cls(
            model_id=str(value.get("model_id", "")),
            model_family=str(value.get("model_family", "")),
            uri=str(value.get("uri", "")),
            sha256=str(value.get("sha256", "")),
            runtime=str(value.get("runtime", "")),
            runtime_version=str(value.get("runtime_version", "")),
            class_names=tuple(str(item) for item in names),
            license_state=str(value.get("license_state", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "model_family": self.model_family,
            "uri": self.uri,
            "sha256": self.sha256,
            "runtime": self.runtime,
            "runtime_version": self.runtime_version,
            "class_names": list(self.class_names),
            "license_state": self.license_state,
        }

    def local_path(self) -> Path:
        parsed = urlparse(self.uri)
        if parsed.scheme in ("http", "https"):
            raise ValueError("remote model URIs are not allowed; provide an explicit local artifact")
        if parsed.scheme == "file":
            path = Path(unquote(parsed.path))
        elif parsed.scheme:
            raise ValueError(f"unsupported model URI scheme: {parsed.scheme}")
        else:
            path = Path(self.uri)
        return path.expanduser().resolve()

    def verify_local_file(self) -> Path:
        path = self.local_path()
        if not path.is_file():
            raise FileNotFoundError(f"model artifact does not exist: {path}")
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        actual = digest.hexdigest()
        if actual != self.sha256:
            raise ValueError(f"model artifact SHA-256 mismatch: expected {self.sha256}, found {actual}")
        return path

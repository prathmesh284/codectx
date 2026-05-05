#!/usr/bin/env python3
"""Compatibility shim for setuptools builds driven by pyproject.toml."""

from __future__ import annotations


def main() -> None:
    from setuptools import setup

    setup()


if __name__ == "__main__":
    main()

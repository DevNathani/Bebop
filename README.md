# Bebop

> High-performance LAN file transfer platform built for scalable networking experimentation.

---

# Overview

Bebop is a modular LAN-based file transfer system designed to transfer large files efficiently between multiple systems on the same network.

The project focuses on:
- scalable architecture
- reliable file transfers
- chunked transfer systems
- event-driven backend design
- future multi-platform support

---

# Features

- Large file transfer over LAN
- Modular architecture
- Chunked file transfer system
- Future parallel transfer support
- Event-driven backend
- Cross-platform design
- Future Rich/Textual UI support

---

# Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Dependency Manager | uv |
| Linting | Ruff |
| Testing | pytest |
| Type Checking | mypy |
| Git Hooks | pre-commit |

---

# Project Structure

```text
bebop/
│
├── src/
├── tests/
├── docs/
├── scripts/
├── pyproject.toml
└── README.md
```

---

# Development Workflow

```text
feature/*
    ↓
dev
    ↓
stable
    ↓
main
```

---

# Roadmap

| Phase | Goal |
|---|---|
| Phase 0 | Architecture & Tooling |
| Phase 1 | Basic TCP File Transfer |
| Phase 2 | Peer Discovery |
| Phase 3 | Chunked Transfers |
| Phase 4 | Parallel Streams |
| Phase 5 | Reliability Layer |
| Phase 6 | Event System |
| Phase 7 | Rich/Textual UI |

---

# Setup

```bash
git clone <repo-url>
cd bebop

uv sync
```

---

# Status

```text
Currently under active development.
```

---

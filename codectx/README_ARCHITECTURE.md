# CodeCtx Architecture - Modular Structure

## Overview

CodeCtx has been refactored into a modular, well-organized architecture following SOLID principles and clean code patterns.

## Directory Structure

```
codectx/
├── __init__.py              # Root module exports (main API)
├── main.py                  # Minimal CLI entry point
├── config.py                # Configuration constants
│
├── cli/                      # Command-line interface layer
│   └── __init__.py          # CLIHandler - CLI command parsing & routing
│
├── models/                   # Data models & schemas
│   └── __init__.py          # AnalysisContext, FileAnalysis dataclasses
│
├── services/                 # High-level business logic
│   └── __init__.py          # AnalysisService, FileSystemService
│
├── utils/                    # Shared utilities
│   └── __init__.py          # TimestampUtils, FormattingUtils
│
├── core/                     # Core file operations (legacy)
│   ├── __init__.py
│   ├── scanner.py           # File tree scanning
│   ├── analyzer.py          # (legacy, integrated into AnalysisService)
│   └── utils.py             # Language detection, etc.
│
├── extractors/              # Data extraction modules
│   ├── __init__.py
│   ├── functions.py         # Extract functions
│   ├── apis.py              # Extract API endpoints
│   ├── dependencies.py      # Extract dependencies
│   ├── env.py               # Extract env vars
│   ├── secrets.py           # Detect secrets
│   └── schema.py            # Data schema definitions
│
├── processors/              # Data processing modules
│   ├── __init__.py
│   ├── summary.py           # Generate file summaries
│   ├── dataflow.py          # Detect data flows
│   ├── error_analysis.py    # Analyze error handling
│   └── auth.py              # Detect auth patterns
│
├── plugins/                 # Plugin system
│   ├── __init__.py
│   ├── base.py              # BasePlugin interface
│   ├── manager.py           # Plugin loading & management
│   ├── loader.py            # Plugin discovery
│   └── sample_plugin.py     # Example plugin
│
├── output/                  # Output handling
│   ├── __init__.py
│   └── writer.py            # JSON output & backup management
│
└── README_ARCHITECTURE.md   # This file
```

## Module Responsibilities

### CLI Module (`cli/__init__.py`)
**Responsibility**: Handle command-line interface and user interaction

```python
from cli import CLIHandler
handler = CLIHandler()
handler.run()  # Parses args and routes to appropriate handlers
```

**Key Classes**:
- `CLIHandler`: Orchestrates CLI argument parsing and command execution

**Exports**:
- `CLIHandler`

---

### Models Module (`models/__init__.py`)
**Responsibility**: Define data structures and schemas

```python
from models import AnalysisContext, FileAnalysis

ctx = AnalysisContext(project="myapp", file_tree=[...])
ctx.to_dict()  # Serialize to JSON
```

**Key Classes**:
- `AnalysisContext`: Complete project analysis result
- `FileAnalysis`: Single-file analysis result

**Exports**:
- `AnalysisContext`
- `FileAnalysis`

---

### Services Module (`services/__init__.py`)
**Responsibility**: High-level business logic and orchestration

```python
from services import AnalysisService, FileSystemService

analysis_svc = AnalysisService()
results = analysis_svc.analyze_project(files, root)

fs_svc = FileSystemService()
files = fs_svc.scan_project(path)
```

**Key Classes**:
- `AnalysisService`: Orchestrates project analysis
  - `analyze_single_file()`: Analyzes one file
  - `analyze_project()`: Parallel analysis of all files
  
- `FileSystemService`: File system operations
  - `scan_project()`: Get file list
  - `get_file_content()`: Read file content

**Exports**:
- `AnalysisService`
- `FileSystemService`

---

### Utils Module (`utils/__init__.py`)
**Responsibility**: Shared utility functions

```python
from utils import TimestampUtils, FormattingUtils

time = TimestampUtils.get_ist_timestamp()
msg = FormattingUtils.format_ok("Analysis complete")
```

**Key Classes**:
- `TimestampUtils`: Timestamp helpers
  - `get_ist_timestamp()`: Get India Standard Time
  - `get_utc_timestamp()`: Get UTC time
  
- `FormattingUtils`: Output formatting
  - `format_scan()`, `format_ok()`, `format_error()`, etc.

**Exports**:
- `TimestampUtils`
- `FormattingUtils`

---

### Output Module (`output/__init__.py`)
**Responsibility**: Handle file writing, serialization, and backups

```python
from output.writer import write_output

write_output(ctx, "output.json")  # Also creates output.json.backup
```

**Key Functions**:
- `write_output()`: Write analysis to JSON + maintain backup history

**Features**:
- Automatic backup on each write
- Sorted backup history by analysis_time
- Dataclass to dict conversion

---

### Core Modules (`core/`)
**Responsibility**: Low-level file operations

**Files**:
- `scanner.py`: File tree walking (`build_file_tree()`)
- `utils.py`: Language detection (`detect_language()`)
- `analyzer.py`: Legacy (logic moved to `AnalysisService`)

---

### Extractors (`extractors/`)
**Responsibility**: Extract specific code elements

**Files**:
- `functions.py`: Extract function definitions
- `apis.py`: Extract API endpoints
- `dependencies.py`: Extract module dependencies
- `env.py`: Extract environment variables
- `secrets.py`: Detect hardcoded secrets
- `schema.py`: Data schema definitions

---

### Processors (`processors/`)
**Responsibility**: Process and analyze extracted data

**Files**:
- `summary.py`: Generate file summaries
- `dataflow.py`: Detect data flow patterns
- `error_analysis.py`: Analyze error handling
- `auth.py`: Detect auth patterns

---

### Plugins (`plugins/`)
**Responsibility**: Plugin system for extensibility

**Key Files**:
- `base.py`: `BasePlugin` interface
- `manager.py`: Plugin loading & execution
  - `load_plugins()`: Load all plugins
  - `reload_plugins()`: Hot reload plugins
  - `run_plugins()`: Execute plugins on a file
- `loader.py`: Plugin discovery
- `sample_plugin.py`: Example plugin implementation

---

## Data Flow

```
main.py (entry point)
    ↓
CLIHandler.run() (parse args)
    ↓
CLIHandler.handle_project_analysis()
    ↓
AnalysisService.analyze_project()
    ├─ FileSystemService.scan_project()
    ├─ Parallel: analyze_single_file()
    │   ├─ Language detection (core.utils)
    │   ├─ Extractors (functions, apis, deps, etc.)
    │   ├─ Processors (summary, dataflow, auth, etc.)
    │   └─ RunPlugins (plugin.manager)
    ├─ Aggregate results → AnalysisContext
    └─ Return AnalysisContext
    ↓
write_output(ctx, "project.ctx.json")
    ├─ Backup old output
    ├─ Sort backups by analysis_time
    └─ Write JSON
```

## Usage Examples

### As a CLI Tool
```bash
python main.py .                    # Scan current directory
python main.py /path/to/project     # Scan specific path
python main.py . --verbose          # With verbose output
python main.py . --reload-plugins   # Hot reload plugins
python main.py . -p /path/to/plugin # Add plugin
```

### As a Python Library
```python
from services import AnalysisService
from models import AnalysisContext
from output.writer import write_output

# Create service
service = AnalysisService()

# Analyze project
ctx = service.analyze_project(files, root)

# Use results
print(ctx.project)
print(ctx.functions)
print(ctx.api_endpoints)

# Save results
write_output(ctx, "output.json")
```

## Benefits of Modular Architecture

✅ **Separation of Concerns**: Each module has single responsibility  
✅ **Testability**: Modules can be tested independently  
✅ **Reusability**: Services can be imported and used standalone  
✅ **Maintainability**: Clear module boundaries make debugging easier  
✅ **Extensibility**: New modules can be added without affecting existing code  
✅ **Scalability**: Easy to add new extractors, processors, or services  

## Adding New Features

### Add a New Extractor
```python
# extractors/custom_extractor.py
def extract_custom_data(code):
    # Your extraction logic
    return results

# Add to AnalysisService.analyze_single_file()
```

### Add a New Processor
```python
# processors/custom_processor.py
def process_custom_data(code, file):
    # Your processing logic
    return results

# Add to AnalysisService.analyze_single_file()
```

### Add a New Service
```python
# services/__init__.py (add new class)
class CustomService:
    def custom_operation(self):
        pass
```

### Add a New CLI Command
```python
# cli/__init__.py (expand CLIHandler)
def handle_custom_command(self, args):
    # Your command logic
```

## Next Steps

1. **Add type hints**: Enhance with full Python type annotations
2. **Add logging**: Implement structured logging across modules
3. **Add tests**: Create unit tests for each module
4. **Add config**: Move hardcoded values to config system
5. **Add caching**: Implement result caching for performance

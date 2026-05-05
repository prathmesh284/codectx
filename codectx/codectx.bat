@echo off
setlocal enabledelayedexpansion

REM ==============================================
REM CodeCtx CLI Launcher - Advanced Code Analysis
REM ==============================================

REM Get directory where this script is located
set SCRIPT_DIR=%~dp0

REM Default project path
set PROJECT_PATH=%CD%

REM ----------------------
REM Parse arguments
REM ----------------------

if "%1"=="" (
    goto :RUN_ANALYZER
)

REM Handle 'plugin' subcommand
if /I "%1"=="plugin" (
    if "%2"=="" (
        echo [ERROR] Plugin command required: add, remove, or list
        echo Usage:
        echo   codectx plugin add ^<file^> [--dir ^<directory^>]
        echo   codectx plugin remove ^<name^> [--dir ^<directory^>]
        echo   codectx plugin list [--dir ^<directory^>]
        goto :EOF
    )

    if /I "%2"=="add" (
        if "%3"=="" (
            echo [ERROR] Please specify plugin file path
            goto :EOF
        )
        REM Check for --dir option
        set TARGET_DIR=
        if /I "%4"=="--dir" (
            if "%5"=="" (
                echo [ERROR] Please specify target directory
                goto :EOF
            )
            set TARGET_DIR=--dir "%5"
        )
        echo [PLUGIN] Adding plugin: %3 !TARGET_DIR!
        python "%SCRIPT_DIR%main.py" plugin add "%3" !TARGET_DIR!
        goto :EOF
    )

    if /I "%2"=="remove" (
        if "%3"=="" (
            echo [ERROR] Please specify plugin name
            echo Usage: codectx plugin remove ^<name^> [--dir ^<directory^>]
            goto :EOF
        )
        REM Check for --dir option
        set TARGET_DIR=
        if /I "%4"=="--dir" (
            if "%5"=="" (
                echo [ERROR] Please specify target directory
                goto :EOF
            )
            set TARGET_DIR=--dir "%5"
        )
        echo [PLUGIN] Removing plugin: %3 !TARGET_DIR!
        python "%SCRIPT_DIR%main.py" plugin remove "%3" !TARGET_DIR!
        goto :EOF
    )

    if /I "%2"=="list" (
        set TARGET_DIR=
        if /I "%3"=="--dir" (
            if "%4"=="" (
                echo [ERROR] Please specify target directory
                goto :EOF
            )
            set TARGET_DIR=--dir "%4"
        )
        echo [PLUGIN] Listing plugins !TARGET_DIR!
        python "%SCRIPT_DIR%main.py" plugin list !TARGET_DIR!
        goto :EOF
    )

    echo [ERROR] Unknown plugin command: %2
    goto :EOF
)

REM Handle 'analyze' subcommand
if /I "%1"=="analyze" (
    if "%2"=="" (
        set PROJECT_PATH=%CD%
    ) else (
        set PROJECT_PATH=%2
    )
    goto :RUN_ANALYZER_WITH_OPTIONS
)

REM Handle help command
if /I "%1"=="/?" (
    call :SHOW_HELP
    goto :EOF
)

if /I "%1"=="help" (
    call :SHOW_HELP
    goto :EOF
)

REM Otherwise, treat as path to scan (legacy mode)
set PROJECT_PATH=%1

REM Check for --reload-plugins or --verbose flags
set FLAGS=
if /I "%2"=="--reload-plugins" (
    set FLAGS=!FLAGS! --reload-plugins
)
if /I "%3"=="--reload-plugins" (
    set FLAGS=!FLAGS! --reload-plugins
)
if /I "%2"=="--verbose" (
    set FLAGS=!FLAGS! --verbose
)
if /I "%3"=="--verbose" (
    set FLAGS=!FLAGS! --verbose
)

:RUN_ANALYZER
echo [SCAN] Running CodeCtx on: "%PROJECT_PATH%"
python "%SCRIPT_DIR%main.py" analyze "%PROJECT_PATH%" !FLAGS!
echo [OK] Analysis complete!
goto :EOF

:RUN_ANALYZER_WITH_OPTIONS
set FLAGS=
if /I "%3"=="--reload-plugins" set FLAGS=!FLAGS! --reload-plugins
if /I "%4"=="--reload-plugins" set FLAGS=!FLAGS! --reload-plugins
if /I "%3"=="--verbose" set FLAGS=!FLAGS! --verbose
if /I "%4"=="--verbose" set FLAGS=!FLAGS! --verbose

echo [SCAN] Running CodeCtx on: "%PROJECT_PATH%"
python "%SCRIPT_DIR%main.py" analyze "%PROJECT_PATH%" !FLAGS!
echo [OK] Analysis complete!
goto :EOF

:SHOW_HELP
echo.
echo CodeCtx - Advanced Code Analysis Tool
echo Version 2.0.0 (Modular Architecture)
echo.
echo USAGE:
echo   codectx [path] [options]                 Analyze a project
echo   codectx analyze [path] [options]         Analyze a project (explicit)
echo   codectx plugin add ^<file^> [--dir ^<dir^>]   Add a plugin
echo   codectx plugin remove ^<name^> [--dir ^<dir^>] Remove a plugin
echo   codectx plugin list [--dir ^<dir^>]       List plugins
echo   codectx help                             Show this help message
echo.
echo OPTIONS:
echo   --reload-plugins                        Force reload plugins (development)
echo   --verbose                               Show detailed output
echo.
echo EXAMPLES:
echo   codectx .                                Analyze current directory
echo   codectx C:\project --verbose             Analyze with verbose output
echo   codectx plugin add my_plugin.py          Add plugin to default location
echo   codectx plugin add plugin.py --dir ./custom_dir  Add to custom directory
echo   codectx plugin remove my_plugin         Remove plugin
echo   codectx plugin list                     Show all plugins
echo   codectx plugin list --dir ./custom_dir  Show plugins in custom directory
echo.
goto :EOF

:EOF
endlocal
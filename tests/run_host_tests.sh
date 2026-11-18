#!/bin/sh
set -eu
task_script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$task_script_dir/run_host_tests.py" "$@"

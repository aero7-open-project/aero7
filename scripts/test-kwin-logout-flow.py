#!/usr/bin/env python3
"""Compile real session-method bodies with controlled timer/transport fixtures."""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path, help="Prepared KWin source directory")
parser.add_argument("--work-parent", required=True, type=Path)
parser.add_argument("--no-notifications", action="store_true")
args = parser.parse_args()
source = (args.source / "src/sm.cpp").read_text()
start = source.index("bool SessionManager::closeWaylandWindows()")
end = source.index("void SessionManager::quit()", start)
work = Path(tempfile.mkdtemp(prefix="logout-flow-", dir=args.work_parent))
print(f"FLOW_TEST_DIRECTORY={work}", flush=True)
(work / "production-session-methods.inc").write_text(source[start:end])
shutil.copyfile(Path(__file__).resolve().parents[1] / "tests/kwin_logout_harness.cpp",
                work / "kwin_logout_harness.cpp")
cmake = '''cmake_minimum_required(VERSION 3.24)
project(KWinLogoutControlFlow LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_AUTOMOC ON)
find_package(Qt6 REQUIRED COMPONENTS Core Test DBus)
add_executable(logout-flow kwin_logout_harness.cpp)
target_link_libraries(logout-flow PRIVATE Qt6::Core Qt6::Test Qt6::DBus)
'''
if args.no_notifications:
    cmake += 'target_compile_definitions(logout-flow PRIVATE KWIN_BUILD_NOTIFICATIONS=0)\n'
(work / "CMakeLists.txt").write_text(cmake)
subprocess.run(["cmake", "-S", str(work), "-B", str(work / "build")], check=True)
subprocess.run(["cmake", "--build", str(work / "build"), "--parallel", "2"], check=True)
raise SystemExit(subprocess.run([str(work / "build/logout-flow")]).returncode)

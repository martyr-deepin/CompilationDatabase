#!/usr/bin/env python3

'''
Generate compilation database file for project.

Usage: ./tools/generate_db.py path/to/project 
'''

import os
import sys
import glob
import shutil
import subprocess

def print_usage_and_exit():
    print(__doc__)
    os._exit(-1)

def guess_build_system(project_path):
    if glob.glob("{}/*.pro".format(project_path)):
        return 'qmake'
    elif glob.glob("{}/CMakeLists.txt".format(project_path)):
        return 'cmake'
    return ''

def generate_db_for_project(project_path, build_sys):
    if build_sys == 'qmake':
        _generate_db_for_qmake_project(project_path)
    elif build_sys == 'cmake':
        _generate_db_for_cmake_project(project_path)
    db_file = _move_file_to_db(project_path)
    _process_db_file(db_file, project_path)

def _run_command(cmd, cwd=None, exit_on_failure=True):
    retcode = subprocess.call(cmd, cwd=cwd)
    if retcode != 0 and exit_on_failure:
        print("Running {} command failed!".format(cmd))
        os._exit(-1)
    return retcode

def _generate_db_for_qmake_project(project_path):
    _run_command(['qmake'], project_path)
    _run_command(['make', 'clean'], project_path)
    _run_command(['bear', 'make'], project_path)

def _generate_db_for_cmake_project(project_path):
    _run_command(['cmake', '-DCMAKE_EXPORT_COMPILE_COMMANDS=1'], project_path)

def _move_file_to_db(project_path):
    dirname = os.path.dirname
    basename = os.path.basename
    root_dir = dirname(dirname(__file__))
    project_name = basename(project_path)
    db_project_dir = os.path.join(root_dir, 'db', project_name)
    if not os.path.exists(db_project_dir):
        os.makedirs(db_project_dir)
    src_file = os.path.join(project_path, 'compile_commands.json')
    dest_file = os.path.join(db_project_dir, 'compile_commands.json')
    shutil.move(src_file, dest_file)
    return dest_file

def _process_db_file(db_file, project_path):
    '''
    _process_db_file processes the generated db file, replace the local project
    path with a fixed one, '/sources/dde-dock' .e.g.
    '''
    project_name = os.path.basename(project_path)
    with open(db_file, 'r+') as _file:
        content = _file.read()
        content = content.replace(project_path, \
                                  os.path.join('/sources/', project_name))
        _file.seek(0)
        _file.truncate()
        _file.write(content)

def check_dep_tools():
    retcode = _run_command(['which', 'bear', 'qmake', 'cmake', 'make'])
    if retcode != 0:
        print('required tools not found.')
        os._exit(-1)

def main():
    if (len(sys.argv) != 2):
        print_usage_and_exit()

    # project_path should be absolute path, _process_db_file relies on this.
    project_path = os.path.abspath(sys.argv[1])
    build_sys = guess_build_system(project_path)
    if build_sys:
        generate_db_for_project(project_path, build_sys)
    else:
        print("Oops, don't know your build system.")

if __name__ == "__main__":
    main()
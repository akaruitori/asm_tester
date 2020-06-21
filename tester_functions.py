# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    tester_functions.py                                :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dtimeon <dtimeon@student.42.fr>            +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2020/06/15 13:46:13 by dtimeon           #+#    #+#             #
#    Updated: 2020/06/16 12:42:23 by student          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import os
import filecmp
from subprocess import run, PIPE
from shutil import copy as copy_file
from platform import system
from time import time

import tester_config as tc


def run_program(program, file, file_copy_name, measure_time):
    if not os.path.isfile(file):
        file_copy_name = file
    else:
        copy_file(file, file_copy_name)
    run_time = 0.0
    if measure_time:
        run_time = time()
    output = run(f"./{program} {file_copy_name}",
                 stdout=PIPE, stderr=PIPE, shell=True)
    if measure_time:
        run_time = time() - run_time
    return(output.returncode, (output.stdout + output.stderr).decode('utf-8'),
           run_time)


def compare(file_1, file_2, filename="", name="tested",
            comparing_with_original=False):
    if not filecmp.cmp(file_1, file_2):
        print('\r', flush=True, end='')
        print(tc.red, '*' * 82, tc.color_clear, ' ' * 42)
        if comparing_with_original:
            print(f" Binary by {name} program differs "
                  f"with original '{file_2}'")
        else:
            print(f" With '{filename}' binary files differ")
        print(tc.red, '*' * 82, tc.color_clear, "\n")


def print_output(output, name="tested"):
    print(f" {name.capitalize()} program returned error, output:")
    print(' ', output.replace('\n', '\n '), sep='')


def test_both_programs(file_path, file_to_compare=None, print_errors=False,
                       measure_time=False):
    tested_code, tested_output, tested_time = run_program(
                                                tc.tested_asm,
                                                file_path,
                                                tc.temp_tested_asm_file,
                                                measure_time)
    school_code, school_output, school_time = run_program(
                                                tc.school_asm,
                                                file_path,
                                                tc.temp_school_asm_file,
                                                measure_time)

    if tested_code == 0 and school_code == 0:
        compare(tc.temp_tested_bin_file, tc.temp_school_bin_file,
                filename=file_path)
        if file_to_compare:
            compare(tc.temp_tested_bin_file, file_to_compare,
                    comparing_with_original=True)
            compare(tc.temp_school_bin_file, file_to_compare, name="school",
                    comparing_with_original=True)
    elif (print_errors or tested_code != school_code):
        print('\r', flush=True, end='')
        print(tc.blue, '*' * 82, tc.color_clear, ' ' * 42)
        if file_to_compare:
            file_path = file_to_compare
        if tested_code != school_code:
            print(f" For file '{os.path.basename(file_path)}' exit codes "
                  f"differ: {tested_code} and {school_code}")
        if (tested_code != 0 and print_errors):
            print_output(tested_output)
        if (school_code != 0 and print_errors):
            print_output(school_output, name="school")
        print(tc.blue, '*' * 82, tc.color_clear, "\n")
    return (tested_time, school_time)


def test_program_on_binary(file_path, print_errors=False):
    code, output, _ = run_program(tc.tested_asm, file_path,
                                  tc.temp_tested_bin_file, False)
    if code != 0 and print_errors:
        color = tc.blue if code == 1 else tc.red
        print('\r', flush=True, end='')
        print(color, '*' * 82, tc.color_clear, ' ' * 42)
        print(f" Tested program returned {code} while converting binary file "
              f"'{os.path.basename(file_path)}', output:")
        print(' ', output.replace('\n', '\n '), sep='')
        print(color, '*' * 82, '\n', tc.color_clear)
    elif code == 0:
        copy_file(tc.temp_tested_asm_file, tc.generated_asm_file)
        test_both_programs(tc.generated_asm_file,
                           file_to_compare=file_path,
                           print_errors=print_errors)


def gather_files(tests_dirs):
    files = []
    try:
        for tests_dir in tests_dirs:
            for file in os.listdir(tests_dir):
                file_path = f"{tests_dir}/{file}"
                files.append(file_path)
    except FileNotFoundError as error:
        print(f"Tests directory not found: {error}")
    return(files)


def count_mentions(output, program):
    mentions = output.count(f"/{program}")
    return(mentions)


def is_leaking_linux(output):
    return(tc.no_leaks_line not in output)


def is_leaking_mac(output, program):
    return(count_mentions(output, program) > 1)


def has_memory_errors_linux(output):
    return(tc.no_errors_line not in output)


def has_memory_errors_mac(output, program):
    return(count_mentions(output, program) > 1)


def print_valgrind_result(asm_leaking, asm_has_errors, output, program, file):
    if asm_leaking:
        print('\r', flush=True, end='')
        print(tc.red, '*' * 82, tc.color_clear)
        print(f" Found memory leaks in {program} with file '{file}':\n")
        print(' ' + output.replace('\n', '\n '))
        print(tc.red, '*' * 82, tc.color_clear)
    if asm_has_errors:
        print('\r', flush=True, end='')
        print(tc.red, '*' * 82, tc.color_clear)
        print(f" Found memory errors in {program} with file '{file}':\n")
        print(' ' + output.replace('\n', '\n '))
        print(tc.red, '*' * 82, tc.color_clear)


def check_valgrind_output(output, program, file):
    sep = output.find(tc.separator_line)
    memory_errors_output = output[:sep]
    leaks_output = output[sep:]
    if system() == 'Linux':
        asm_leaking = is_leaking_linux(leaks_output)
        asm_has_errors = has_memory_errors_linux(output)
    elif system() == 'Darwin':
        asm_leaking = is_leaking_mac(leaks_output, program)
        asm_has_errors = has_memory_errors_mac(memory_errors_output, program)
    if asm_leaking or asm_has_errors:
        print_valgrind_result(asm_leaking, asm_has_errors, output,
                              program, file)


def run_leak_check(program, options, file):
    ext = os.path.splitext(file)[1]
    temp_file = f"{tc.valgrind_temp_basename}{ext}"
    if os.path.isfile(file):
        copy_file(file, temp_file)
    else:
        temp_file = file
    for option in options:
        if not option == "":
            option = f" -{option}"
        if system() == 'Linux':
            command = f"valgrind ./{program}{option} {temp_file}"
        elif system() == 'Darwin':
            valgrind_args = "valgrind  --leak-check=full --show-leak-kinds=all"
            command = f"{valgrind_args} ./{program}{option} {temp_file}"
        valgrind_output = run(command, stdout=PIPE, stderr=PIPE, shell=True)
        valgrind_output = valgrind_output.stderr.decode('utf-8')
        print_cur_task(f"Checking for leaks '{tc.some_color}"
                       f"{program}{option} {temp_file}{tc.color_clear}'")
        check_valgrind_output(valgrind_output, program, file)
    if os.path.isfile(temp_file):
        os.remove(temp_file)


def perf_check():
    print('\r', flush=True, end='')
    print(tc.green, "** Performance check **", tc.color_clear, ' ' * 100)
    print()
    for file in os.listdir(tc.large_files_dir):
        file_path = f"{tc.large_files_dir}/{file}"
        tested_time, school_time = test_both_programs(file_path,
                                                      measure_time=True)
        print(f"{file}:\ntested: ", tc.green, f"{tested_time:.3f} sec",
              tc.color_clear)
        print(f"school: ", tc.green, f"{school_time:.3f} sec",
              tc.color_clear, "\n")


def print_cur_task(task):
    print("\r", end="   ")
    print(f"{task}", " " * (125 - len(task)), end='', flush=True)


def remove_temp_files():
    for file in (tc.temp_school_asm_file,
                 tc.temp_school_bin_file,
                 tc.temp_tested_asm_file,
                 tc.temp_tested_bin_file,
                 tc.generated_asm_file,
                 tc.valgrind_temp_asm_file,
                 tc.valgrind_temp_bin_file):
        if os.path.exists(file):
            os.remove(file)

#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    tester.py                                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dtimeon <dtimeon@student.42.fr>            +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2020/06/13 15:48:49 by dtimeon           #+#    #+#             #
#    Updated: 2020/06/15 17:23:10 by dtimeon          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from argparse import ArgumentParser

import tester_functions as tf
from tester_functions import tc


if __name__ == "__main__":
    if tf.system() not in ('Linux', 'Darwin'):
        print("This platform is not supported yet")
        quit()

    parser = ArgumentParser()
    parser.add_argument("filenames", nargs="*", type=str,
                        help="specify files to test")
    parser.add_argument("-v", "--print_errors", action='store_true',
                        help="print program output in case of an error")
    parser.add_argument("-o", "--options", nargs="*", type=str,
                        help="list of options to check for memory leaks with")
    parser.add_argument("-t", "--check_time", action='store_true',
                        help="run performance check on big files")
    parser.add_argument("-e", "--no_leak_check", action='store_true',
                        help="express mode, no checks for leaks")
    parser.add_argument("-r", "--reversed_test", action='store_true',
                        help="Switch tested and school asm programs")
    args = parser.parse_args()

    if args.filenames:
        files = args.filenames
    else:
        files = tf.gather_files(tc.tests_dirs)

    options = ["", ]
    if args.options:
        options.extend(args.options)

    if args.reversed_test:
        tc.tested_asm, tc.school_asm = tc.school_asm, tc.tested_asm

    for file in files:
        if (not file.endswith('.cor') or tf.os.path.isdir(file)):
            tf.test_both_programs(file, print_errors=args.print_errors)
            tf.print_cur_task(f"Comparing results: '{tc.some_color}"
                              f"{file}{tc.color_clear}'")
        else:
            if not args.reversed_test:
                tf.test_program_on_binary(file, print_errors=args.print_errors)
                tf.print_cur_task(f"Checking disassmbler with '{tc.some_color}"
                                  f"{file}{tc.color_clear}'")
        if not args.no_leak_check:
            tf.run_leak_check(tc.tested_asm, options, file)
    if (args.check_time):
        tf.perf_check()
    print('\r', ' ' * 125, '\r', flush=True, end='')

    tf.remove_temp_files()

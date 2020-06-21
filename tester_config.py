# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    tester_config.py                                   :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dtimeon <dtimeon@student.42.fr>            +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2020/06/15 13:46:08 by dtimeon           #+#    #+#             #
#    Updated: 2020/06/16 12:16:03 by student          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

tested_asm = 'asm'
school_asm = 'test_asm/school_asm_linux'

temp_tested_asm_file = 'test_asm/temp_tested.s'
temp_school_asm_file = 'test_asm/temp_school.s'
temp_tested_bin_file = 'test_asm/temp_tested.cor'
temp_school_bin_file = 'test_asm/temp_school.cor'
generated_asm_file = 'test_asm/source_by_tested_program.s'
valgrind_temp_basename = 'test_asm/temp_file'
valgrind_temp_asm_file = 'test_asm/temp_file.s'
valgrind_temp_bin_file = 'test_asm/temp_file.cor'

tests_dirs = ['test_asm/assets/file_validation',
              'test_asm/assets/file_reading',
              'test_asm/assets/file_parsing',
              'test_asm/assets/file_parsing/incorrect']
large_files_dir = 'test_asm/assets/big_files'

no_leaks_line = 'no leaks are possible'
no_errors_line = '0 errors from 0 contexts (suppressed: 0 from 0)'
separator_line = " HEAP SUMMARY:"

blue = "\u001b[34;1m"
red = "\u001b[31;1m"
green = "\u001b[32;1m"
some_color = "\u001b[35;1m"
color_clear = "\033[0m"

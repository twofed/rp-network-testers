"""
    'KootNet Ethernet Testers' is a collection of scripts and programs
    to test Ethernet cables and or network routes.
    Copyright (C) 2018  Chad Ermacora  chad.ermacora@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import time
from operations_modules.config_primary import current_config
from operations_modules import file_locations
from operations_modules import app_variables
from operations_modules.app_generic_functions import get_subprocess_str_output, thread_function, write_file_to_disk
from operations_modules.hardware_access import hardware_access


def run_command(command_num):
    if command_num == 0:
        current_config.clear_button_counts(exception_button=0)
        start_mtr()
    elif command_num == 1:
        current_config.clear_button_counts(exception_button=1)
        start_iperf()
    elif command_num == 2:
        current_config.clear_button_counts(exception_button=2)
        display_tester_information()
    elif command_num == 3:
        hardware_access.display_message("Shutting Down\n\nPlease Wait 15 Seconds\nBefore Powering Down ...")
        thread_function(os.system, args="sleep 2 && shutdown now")


def start_all_tests():
    start_mtr()
    start_iperf()


def start_mtr():
    current_config.tests_running = True
    if current_config.button_1 < 1:
        try:
            print("\nStarting MTR CLI: " + current_config.get_mtr_command_str() + "\n")
            thread_function(hardware_access.display_message("Starting MTR Test\n\nPlease Wait ..."))
            temp_lines = get_subprocess_str_output(current_config.get_mtr_command_str()).strip().split("\n")
            temp_lines = temp_lines[1:]
            new_str = ""
            for line in temp_lines:
                new_str += line + "\n"
            app_variables.previous_mtr_start_text = "Ran at " + time.strftime("%d/%m/%y - %H:%M") + "\n(DD/MM/YY - HH:MM)\n\n"
            app_variables.previous_mtr_results = new_str.strip()[:-2]
            print("MTR CLI Done\n")
        except Exception as error:
            print("MTR Command Error: " + str(error))
        current_config.tests_running = False
        save_mtr_results_to_file()
        hardware_access.display_message(hardware_access.get_mtr_message(app_variables.previous_mtr_results))
        current_config.button_1 = 1
    else:
        hardware_access.display_message("Secondary Button 1")
        current_config.clear_button_counts()


def start_iperf():
    current_config.tests_running = True
    if current_config.button_2 < 1:
        try:
            print("\nStarting iPerf 3 CLI: " + current_config.get_iperf_command_str())
            thread_function(hardware_access.display_message("Starting iPerf3 Test\n\nPlease Wait ..."))
            app_variables.previous_iperf_start_text = "Ran at " + time.strftime("%d/%m/%y - %H:%M") + "\n(DD/MM/YY - HH:MM)\n\n"
            raw_iperf = get_subprocess_str_output(current_config.get_iperf_command_str())[2:-2]
            app_variables.previous_iperf_results = raw_iperf
            print("iPerf 3 CLI Done\n")
        except Exception as error:
            print("iPerf Command Error: " + str(error))
        current_config.tests_running = False
        save_iperf_results_to_file()
        hardware_access.display_message(hardware_access.get_iperf_message(app_variables.previous_iperf_results))
        current_config.button_2 = 1
    else:
        hardware_access.display_message("Secondary Button 2")
        current_config.clear_button_counts()


def save_mtr_results_to_file():
    text_time_sec = str(time.time()).split(".")[0]
    new_file_location = "/test_results/kootnet_ethernet_results-mtr-" + text_time_sec + ".txt"
    write_file_to_disk(file_locations.script_folder_path + new_file_location,
                       app_variables.previous_mtr_start_text + app_variables.previous_mtr_results)


def save_iperf_results_to_file():
    text_time_sec = str(time.time()).split(".")[0]
    new_file_location = "/test_results/kootnet_ethernet_results-iperf-" + text_time_sec + ".txt"
    write_file_to_disk(file_locations.script_folder_path + new_file_location,
                       app_variables.previous_iperf_start_text + app_variables.previous_iperf_results)


def display_tester_information():
    date_now = time.strftime("%d/%m/%y")
    time_now = time.strftime("%H:%M")
    if current_config.button_3 < 1:
        text_msg = hardware_access.get_sys_info_message()
        print(text_msg)
        thread_function(hardware_access.display_message(text_msg))
        current_config.button_3 = 1
    else:
        text_msg = "Date: " + date_now + " (D/M/Y)\nTime: " + time_now + "\n\nDEV Upgrade\nPlease Wait ..."
        thread_function(hardware_access.display_message(text_msg))
        thread_function(os.system, args="bash " + file_locations.http_upgrade_script + " dev")
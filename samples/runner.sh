#!/bin/bash

# Supports multiple test runner implementations

# Override test folder and mock server port by setting environment variables
# export test_folder=sample_tests
# export test_port=8888

#python3 -m tornado.test.runtests api_tester.py -v
#nosetests api_tester.py --verbosity=3
export test_folder="../samples/tests"

nohup python3 api/test_api.py 2>&1>/dev/null &
# Storing the background process' PID.
bg_pid=$!

cd ../api_tester
python3 -m unittest api_tester.py -v

# Also possible to run as a main function and pass commandline options
# usage: api_tester.py [-h] [--port PORT] --folder FOLDER [--version]
# python3 api_tester.py -f sample_tests -p 8888

kill -9 $bg_pid
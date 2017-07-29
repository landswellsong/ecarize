#
# Copyright 2017 Oleksiy Protas
# Copyright 2017 Ecognize.me OÜ
#
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
#

from time import time, sleep

def run(fd, pids, delay, discovery_mode):
    """
    Requests pids from the fd stream infinitely spaced out with at least
    delay milliseconds.

    If discovery_mode is on, exits after the first run.
    """
    while True:
        # Starting the timer
        start = time()

        # Requesting all the pids, converting to string representation
        for pid in pids:
            print('01' + hex(pid).upper()[2:], file=fd, end='\r')

        # Checking if we need to continue
        if discovery_mode:
            break

        # Stopping the timer
        time_left = delay - 1000 * ( time() - start )

        # Sleeping the leftover
        if time_left > 0:
            sleep()

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

from inspect import signature

def bit_decoder(base_pid):
    """
    Generates a function to decode 4 bytes of PID support information into
    a tuple of numerical PIDs starting from base_pid.
    """
    return lambda A, B, C, D: tuple(base_pid + i*8 + j
        for i, b in enumerate((A,B,C,D))
        for j in range(8)
        if (1<<(7-j)) & b)

if __name__ == '__main__':
    # Example from Wikipedia
    foo = bit_decoder(1)
    print(foo(0xBE, 0x1F, 0xA8, 0x13))

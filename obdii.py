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

def parse(pid, fd):
    """
    Reads the response to pid from the connection object fd and converts it into
    a meaningful value.

    Don't try to read PIDs that this function doesn't support because of the
    variable length of the responses.

    Extensions should go here, please follow the template. The amount of data
    bytes to read is deremined by the number of arguments to the formula.

    https://en.wikipedia.org/wiki/OBD-II_PIDs
    """
    # Determining the formula to used
    formula = {
        # PIDs supported
        0x00: bit_decoder(0x01),
        0x20: bit_decoder(0x21),
        0x40: bit_decoder(0x41),

        # Calculated engine load, %
        0x04: lambda A: A / 2.55,

        # Engine coolant temperature, °C
        0x05: lambda A: A - 40,

        # Fuel pressure, kPa
        0x0A: lambda A: 3 * A,

        # Intake manifold absolute pressure, kPa
        0x0B: lambda A: A,

        # Engine RPM
        0x0C: lambda A, B: ( 256 * A + B ) / 4,

        # Vehicle speed, km/h
        0x0D: lambda A: A,

        # Timing advance, °
        0x0E: lambda A: A / 2 - 64,

        # Intake air temperature, °C
        0x0F: lambda A: A - 40,

        # MAF air flow rate, g/s
        0x10: lambda A, B: ( 256 * A + B ) / 100,

        # Throttle position, %
        0x11: lambda A: A / 2.55,
    }[pid]

    # Determining how much data we need to read
    n_to_read = len(signature(formula).parameters)

    # Reading from the descriptor and passing through the formula
    v = fd.read(n_to_read)

    return formula(*v)


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
    foo = bit_decoder(0x01)
    if foo(0xBE, 0x1F, 0xA8, 0x13)) != ( 0x01, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x13, 0x15, 0x1C, 0x1F, 0x20):
        print("Bit decoder is broken")

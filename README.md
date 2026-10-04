# Arduino Oscilloscope

## Overview

A project where Arduino and Python are used to make a graph of voltage vs time.

Built with Arduino UNO. Potentiometer is wired to 5V and ground, and is used to change the voltage. Result from potentiometer is wired to analog input `A0`. The UNO is connected to a Windows PC by USB.

## Specifications

Samples from 0-5V, with a resolution of 10 bits and about 4.9mV. Input error of about ±1 count on static input. Default sampling interval is 50ms (20 Hz), set deliberately low for readability.

## Design decisions

The Arduino sketch schedules the reading of analog voltage so that the sample interval of each serial datapoint is consistent. Using a difference with `micros()` means that the processing time of each read doesn't build up on each other and make inaccurate time readings, like using `delay()` would.

Matplotlib is used because of my familiarity from prior programming classes, so bug fixing and program design would be more straightforward.

A `deque` is used to store values, as FIFO functionality is required, and is time complexity O(1) instead of O(n) with an array made to function the same way.

`println()` has an inefficiency. It takes 10 bits for UART to transmit 1 byte, because it needs a start and stop bit. `println()` uses ASCII, and in ASCII every char gets its own byte. So, to transmit `357`, it takes 50 bits, for `3`, `5`, `7`, `\r`, `\n`. Whereas just transmitting as binary 357 would be `0000000101100101` in 2 bytes. The wire only takes whole bytes, which is why it's padded to 2 bytes.

We run at 115200 baud (bits per second), and at 10 bits/byte that is 11,520 bytes/sec. We need 5 bytes for every sample, so 11,520 bytes/sec divided by 5 bytes per sample makes 2,300 samples per second, while the ADC can handle 9,600.

`println()` was used to make the output readable in the Serial Monitor to verify the hardware, not to make the most efficient possible program.

Switching to binary would roughly increase sampling by 2.5x but would cost using the Serial Monitor to debug, and require a framing scheme to distinguish where each sample starts/ends.

## Issues encountered

`next` was initialized to `0`, but `micros()` is already several thousand by the time the sketch runs. The first comparison therefore saw a huge elapsed time and fired repeatedly until `next` caught up to the present, producing a burst of samples at startup. Fixed by setting `next = micros()` in `setup()` so the schedule starts from the current time.

## Setup

Requires Python 3 and the Arduino IDE.

1. Upload `scope.ino` to the Arduino Uno
2. Wire a potentiometer: outer legs to 5V and GND, wiper to `A0`
3. Install dependencies: `pip install pyserial matplotlib`
4. Set the `PORT` variable in `osc.py` to your board's port (`COM9` on my machine)
5. Close the Arduino Serial Monitor, then run `python osc.py`

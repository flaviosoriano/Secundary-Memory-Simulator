# Cache Memory Simulator

## Project Overview
This project implements a **Cache Memory Simulator** that simulates a single-level cache memory system. The simulator processes memory accesses from a given input file, fills cache lines as needed, and tracks the number of **HITS** and **MISSES** encountered during execution. The simulator determines whether a memory block is already present in the cache (**HIT**) or needs to be fetched from main memory (**MISS**). It also decides in which cache line a memory block should be stored.

The simulator does **not** handle real data storage; it only manages cache line placement and tracking.

## Objectives
The primary goal of this project is to provide hands-on experience with:
- **Direct Mapping**
- **Set Associative Mapping**
- **Fully Associative Mapping**

These concepts are crucial for understanding how different mapping methods impact cache efficiency and performance.

## Simulator Specifications
The simulator is implemented in **Python**, allowing the use of any necessary additional libraries. The program is executed via the command line and will be tested in a Linux environment. It is strongly recommended to test the program on a Linux machine before submission to avoid unexpected failures due to system differences.

### Program Execution
The main program should be named `simulador.py` and executed with the following command format:

```bash
python3 simulador.py <cache_size> <line_size> <group_size> <input_file>
```

#### Command-line Parameters:
1. **cache_size**: Total cache size in bytes (e.g., `4096` for 4KB).
2. **line_size**: Size of each cache line in bytes (e.g., `1024` for 1KB).
3. **group_size**: Number of lines per group (1 for direct mapping, full associativity for complete mapping).
4. **input_file**: Path to the file containing memory access addresses.

#### Example Execution:
```bash
python3 simulador.py 4096 1024 1 memory_accesses.txt
```

### Fixed Simulator Parameters
The simulator assumes the following fixed parameters:
- **32-bit address space**
- Addresses refer to bytes, not words
- **FIFO (First In First Out)** page replacement policy
- Lines in a set are stored sequentially in the cache
- Cache contains fewer than 1000 lines

## Input File Specification
The simulator receives a text file containing a sequence of memory addresses to be accessed. Each address is represented in **hexadecimal format**, prefixed with `0x` and consists of exactly **8 uppercase hexadecimal digits**.

### Example Input File:
```
0xDEADBEEF
0x00000000
0x12345678
0xDEADBEEF
```

The simulator processes these addresses in sequence and determines whether they result in a **HIT** or **MISS**.

## Output Specification
The simulator will generate an output file named `output.txt` that contains the state of the cache lines after each memory access, followed by the total count of HITS and MISSES.

### Output Format Example (for a 4KB cache, 1KB lines, full associativity):
```
====================
Index Valid Tag
000   1    0xDEADBC00
001   1    0x00000000
002   1    0x12345400
====================
HITS: 1
MISSES: 3
```

#### Explanation of Output Fields:
- **Index:** Represents the physical position of the cache line.
- **Valid Bit:** Indicates if the line contains valid data (1 = valid, 0 = invalid).
- **Tag:** 32-bit hexadecimal block identifier, formatted in uppercase.
- **HITS & MISSES:** Total count of memory access outcomes.

### Address Processing:
To calculate the block identifier, the simulator removes:
- The least significant bits representing the **offset** within a cache line.
- Additional bits for set indexing (if applicable).

#### Example Calculations:
For address `0xDEADBEEF`:
- Binary: `11011110101011011011111011101111`
- Ignoring the least significant 10 bits (for 1KB line size): `11011110101011011011110000000000`
- Resulting Block Tag: `0xDEADBC00`

For address `0x12345678`:
- Binary: `00010010001101000101011001111000`
- Resulting Block Tag: `0x12345400`

For address `0x00000000`, the block tag remains the same: `0x00000000`

If set associativity is greater than 1, additional bits for identifying sets will also be removed.

## Testing
It is essential to test the simulator under various configurations and input files to ensure correctness.

## Requirements
- Python 3.x
- Linux environment (recommended for final testing)

## How to Run
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Run the simulator:
   ```bash
   python3 simulador.py 4096 1024 1 input.txt
   ```
3. Check the generated `output.txt` file for results.

## License
This project is licensed under the MIT License.

## Authors
Caio Grossi, Flávio Soriano, Luísa Gontijo


# Computer Networks Assignment 3

## Directory Structure

```
.
├── Q1
│   ├── 1a_1.py
│   ├── 1a_2.py
│   ├── 1b.py
│   ├── h2_dump.txt
│   ├── h8_dump.txt
│   └── ping_output.txt
├── Q2
│   ├── 2.py
│   ├── output_a.txt
│   ├── output_b.txt
│   └── output_c.txt
├── Q3
│   ├── distance_vector.c
│   ├── node0.c
│   ├── node1.c
│   ├── node2.c
│   ├── node3.c
│   └── simulation
└── README.md
```

---

## Overview

This project consists of three main parts:
- **Q1**: Network simulations using Mininet with varying configurations.
- **Q2**: Simulation of NAT with STP and iperf3 bandwidth testing.
- **Q3**: Implementation of a distance vector routing protocol in C across 4 nodes.

---

## Prerequisites

- Mininet installed (`sudo apt install mininet`)
- iperf3 (`sudo apt install iperf3`)
- Python 3.9 and above
- `gcc` for compiling C files (for Q3)

---

## Q1: Mininet Topology Tests

Located in the `Q1` folder.

### 1. `1a_1.py`
- A ring topology with 4 switches and 8 hosts.
- Hosts are connected with 5ms delay; switch links have 7ms.
- Runs ping tests between specific pairs.

### 2. `1a_2.py`
- Same topology as `1a_1.py`, but includes:
  - **tcpdump** on h2 and h8 to capture ARP/ICMP traffic.
  - Saves output to `h2_dump.txt`, `h8_dump.txt`, and `ping_output.txt`.

### 3. `1b.py`
- Uses `OVSController` and enables STP on all switches.
- Verifies connectivity with the same ping tests as `1a_1.py`.

#### How to Run
```bash
cd Q1
sudo python3 1a_1.py      # or 1a_2.py or 1b.py
```

---

## Q2: NAT and Performance Testing

Located in the `Q2` folder.

### `2.py`
- Implements a NAT using `h9` with:
  - Internal hosts: h1, h2 (subnet 10.1.1.x)
  - External hosts: h3-h8 (subnet 10.0.0.x)
- Uses iptables on h9 for NAT.
- Includes:
  - Ping tests from internal to external and vice versa.
  - Bandwidth tests using iperf3 between various nodes.
- Results are saved in:
  - `output_a.txt`, `output_b.txt`, `output_c.txt`

#### How to Run
```bash
cd Q2
sudo python3 2.py
```

---

## Q3: Distance Vector Routing in C

Located in the `Q3` folder.

### Files:
- `node0.c` to `node3.c`: Logic for each router.
- `distance_vector.c`: Shared logic and initialization.
- `simulation`: Binary to simulate the DV algorithm (assumed precompiled or to be compiled).

#### How to Compile
```bash
cd Q3
gcc node0.c node1.c node2.c node3.c distance_vector.c -o simulation
```

#### How to Run
```bash
./simulation
```

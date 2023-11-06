# MicroNet

MicroNet is a robust networking stack designed specifically for microcontrollers and embedded systems. It enables these devices to connect and communicate over networks using standard protocols, despite the constraints of limited computing resources.

## Features

### Comprehensive Protocol Support
MicroNet offers implementations for essential network protocols, facilitating a variety of network operations:
- **Ethernet**: Basic network communication via Ethernet frames.
- **ARP**: Address Resolution Protocol for mapping network addresses to physical hardware.
- **IP**: Internet Protocol for routing packets across network boundaries.
- **TCP**: Transmission Control Protocol for reliable, ordered, and error-checked delivery of a stream of packets on the network.
- **UDP**: User Datagram Protocol for simpler message-based connectionless communication.
- **DHCP**: Dynamic Host Configuration Protocol for dynamic IP address assignment and network configuration.

### Modularity
- **Layered Architecture**: Organized in a clear layered structure, mirroring the OSI model which allows for separation of concerns and easier debugging.
- **Protocol Independence**: Each protocol implementation is independent, allowing users to include only what is necessary for their application, saving space and resources.
- **Driver Support**: Includes support for popular network controller hardware like the ENC28J60, with the ability to extend support for additional hardware.

### Easy Integration
- **Simple Interface Setup**: With a few lines of code, set up a network interface and configure IP settings automatically using DHCP.
- **Network Configuration**: Easily retrieve and manage network configuration details such as IP address, netmask, gateway, and DNS settings.

### Embedded System Friendly
- **Low Resource Requirement**: Designed to be resource-efficient, MicroNet works well on devices with limited memory and processing power.
- **Microcontroller Compatibility**: Compatible with common microcontroller boards, enabling them to participate in network communication.

## Getting Started

### Prerequisites
Ensure you have Python installed on your system. MicroNet is compatible with Python 3.x.

### Installation
Clone the repository and install MicroNet using Python's setup tools:

```bash
git clone https://github.com/yourusername/micronet.git
cd micronet
python setup.py install
```

### Quickstart Guide

To initialize a network interface and begin sending or receiving data, follow these steps:

```python
from micronet.micronet import inet
from micronet.drivers import ENC28J60

# Initialize your network interface controller
device = ENC28J60()

# Create a network interface object
network_interface = inet.interface(device)

# Obtain network configuration via DHCP
network_config = inet.dhcp('my-device-hostname', device)

# After running DHCP, your device will be assigned an IP address,
# and you can begin sending or receiving data on the network.
```

## Examples

For a hands-on demonstration of MicroNet in action, refer to the provided `example.py` script and the `example.ipynb` Jupyter notebook. These examples guide you through basic setup, sending data, and receiving data over the network.

## Project Structure

The project is organized as follows:
- `micronet/`: The main package containing all the core networking stack functionality.
  - `Protocols/`: Implementation of various network protocols layered as per networking standards.
  - `drivers/`: Contains drivers for networking hardware, such as the ENC28J60 Ethernet controller module.
  - `micronet.py`: The main module providing interfaces for network communication.

## Support

For support, please open an issue in the GitHub repository issue tracker.

We hope MicroNet empowers you to build the next generation of connected devices!


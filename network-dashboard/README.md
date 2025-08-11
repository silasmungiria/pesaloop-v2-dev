# Network Traffic Analysis Dashboard

This project is a real-time **Network Traffic Analysis Dashboard** built using Streamlit and Scapy. It captures network packets, processes them, and displays key metrics and visualizations in an interactive web interface.

---

## Features

- **Real-Time Packet Capture:** Continuously captures network packets using Scapy.
- **Dashboard Visualizations:**
  - Protocol distribution pie chart.
  - Packets timeline as a line chart.
  - Top source IP addresses bar chart.
- **Metrics Display:**
  - Total number of packets captured.
  - Capture duration.
- **Recent Packet View:** Displays the last 10 packets with essential details.
- **Auto-Refresh:** Periodically refreshes the data to update the dashboard.

---

## Prerequisites

### System Requirements

- **Operating System:** Linux, macOS, or Windows (with administrator privileges).
- **Python Version:** Python 3.7 or higher.

### Python Libraries

Install the following Python packages:

- `streamlit`
- `pandas`
- `plotly`
- `scapy`

To install these dependencies, run:

```bash
pip install streamlit pandas plotly scapy
```

### Additional Tools (Windows Only)

- Install [Npcap](https://nmap.org/npcap/), a packet capture driver required for Scapy.

---

## Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd network-dashboard
```

### Activate Virtual Environment

Create and activate a virtual environment (optional but recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Run the Dashboard

Run the following command in the terminal:

```bash
streamlit run dashboard.py
```

### Access the Dashboard

After running the command, Streamlit will provide a local URL (e.g., `http://localhost:8501`) to access the dashboard in your web browser.

---

## How It Works

1. **Packet Capture:**

   - The application uses Scapy's `sniff` function to capture network packets.
   - Captured packets are processed in real time to extract essential details like source, destination, protocol, and size.

2. **Data Processing:**

   - Packet data is stored in a thread-safe list and converted to a Pandas DataFrame for analysis.
   - Only the most recent 10,000 packets are stored to optimize memory usage.

3. **Visualizations:**
   - Protocol distribution is shown as a pie chart.
   - Packets per second are visualized as a line chart.
   - Top source IPs are displayed as a bar chart.

---

## File Structure

```
network-dashboard/
├── dashboard.py      # Main application script
├── requirements.txt  # Dependencies
└── README.md         # Project documentation
```

---

## Usage Notes

### Windows

1. Install [Npcap](https://nmap.org/npcap/) for Scapy to function correctly.
2. Run PowerShell as an Administrator to ensure sufficient privileges for packet sniffing.
3. Run the following commands:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   streamlit run dashboard.py
   ```

### macOS/Linux

1. Ensure you have the necessary permissions to sniff network packets (usually requires root privileges).
2. Run the following commands:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   streamlit run dashboard.py
   ```
3. If additional permissions are needed, prepend the command with `sudo`:
   ```bash
   sudo streamlit run dashboard.py
   ```

---

## Troubleshooting

### Common Errors

- **`sudo` Command Not Found (Windows):**

  - This error occurs because `sudo` is a Unix-specific command. Use `streamlit run dashboard.py` without `sudo` on Windows.

- **Scapy Errors (Windows):**

  - Ensure Npcap is installed and configured correctly.

- **Permission Denied (macOS/Linux):**

  - Run the script with `sudo` to grant the necessary permissions for packet sniffing.

- **Port Already in Use:**
  - Streamlit might conflict with another service on port `8501`. Use the `--server.port` flag to specify a different port:
    ```bash
    streamlit run dashboard.py --server.port 8502
    ```

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- **Streamlit:** For providing an intuitive library to build data dashboards.
- **Scapy:** For powerful network packet processing capabilities.
- **Plotly:** For creating interactive visualizations.

---

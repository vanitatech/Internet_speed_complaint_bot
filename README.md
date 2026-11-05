# Internet Speed Complaint Bot

This Selenium script measures download and upload speeds at Speedtest.net. If either measurement is below the thresholds configured in `main.py` (currently 1000 Mbps down and 1000 Mbps up), it signs in to the configured Y account and posts a complaint.

## Requirements

- Python 3.8 or newer
- Google Chrome or Chromium
- Selenium and python-dotenv

Install the Python dependencies:

```bash
python -m pip install selenium python-dotenv
```

Selenium Manager can locate or download a compatible browser driver. You need a working Chrome or Chromium installation and internet access.

## Configuration

Create a `.env` file next to `main.py`:

```dotenv
Y_EMAIL=your-account-email
Y_PASSWORD=your-account-password
```

Use credentials for an account you are authorized to use. The script can publish a post if the speed test is below either threshold, so check the threshold and generated message before running it.

## Run

From this directory, run:

```bash
python main.py
```

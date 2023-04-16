*PingPong

PingPong is a Python script that pings a specified website to test its response time, and sends an email notification if the website is down or if the response time is too slow.

Requirements:
- Python 3.x
- speedtest-cli module
- smtplib module

Installation:
1. Clone this repository
2. Install the required modules using pip: `pip install speedtest-cli` and `pip install secure-smtplib`
3. Configure the script by modifying the constants at the beginning of main.py
4. Run the script using `python main.py`

Usage:
- The script will automatically run every `ping_interval` seconds (default is 300 seconds, or 5 minutes).
- If the website response time is greater than `max_response_time` seconds (default is 10 seconds), or if the website is down (i.e. response time is None), the script will send an email notification to the specified email address.

Author:
- [Your Name]

License:
- This project is licensed under the MIT License. See the LICENSE file for details.
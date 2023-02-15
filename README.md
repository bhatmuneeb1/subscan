# Subscan

As an information security professional, the process of manually performing reconnaissance on a target domain to discover subdomains and check for subdomain takeover vulnerabilities can be a time-consuming and tedious task. That's why I decided to create this Subdomain Reconnaissance Tool to automate the process and make it more efficient.

This tool combines the power of multiple subdomain enumeration tools like Sublist3r, Assetfinder, Subfinder, and Amass, which helps in finding a comprehensive list of subdomains. Additionally, the tool checks for live subdomains using both httprobe and httpx, making sure that only the active subdomains are considered for the subdomain takeover check. The tool also checks for subdomain takeover vulnerabilities using three different tools, namely SubOver, Subzy and Subjack, which provides a thorough and reliable assessment of the target domain's security posture.

By creating this tool, I wanted to provide a quick and efficient way to perform reconnaissance on a target domain and help fellow security professionals save time and effort. This tool is not only user-friendly but also highly effective in discovering subdomains and potential subdomain takeover vulnerabilities. I hope this tool will be useful to the community.

# Installation

1. Clone the Subscan repository to your local machine using the following command:

```git clone https://github.com/yourusername/subscan.git```

2. Change your current directory to the subscan folder:

```cd subscan```

3. Install the required dependencies by running the following command:

```pip install -r requirements.txt```

4. You're ready to use Subscan!

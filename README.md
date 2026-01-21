# Purple Team Nmap Automation

**An offensive–defensive Purple Team project focused on automating Nmap scans with Python, improving scan readability through XML-to-HTML transformation, and integrating scan output into IDS/IPS workflows for detection and response.**

This project was completed as part of a collaborative cybersecurity bootcamp assignment.
This repository contains **my individual contributions and implementations** related to **Nmap automation and scan result visualization**.

---

## Table of Contents

1. [Overview / How It Works](#overview--how-it-works)
2. [Project Context](#project-context)
3. [Features](#features)
4. [Automation Workflow](#automation-workflow)
5. [Project Structure](#project-structure)
6. [Tech Stack](#tech-stack)
7. [Usage](#usage)
8. [Defensive Integration](#defensive-integration)
9. [Code Quality & Design](#code-quality--design)
10. [Future Improvements](#future-improvements)

---

## Overview / How It Works

This project focuses on **automating network reconnaissance** while ensuring scan output is **organized, readable, and suitable for defensive monitoring**.

Instead of relying on static cron jobs or manual scans, Python scripts are used to:

* Run configurable or predefined Nmap scans
* Capture scan results in XML format
* Convert XML output into clean, human-readable HTML using XSLT
* Timestamp and store results for traceability
* Support repeated scans for monitoring network changes over time

The resulting output can be reviewed manually or correlated with IDS tools such as **Snort**, **Splunk**, or **Security Onion** for detection and alerting.

---

## Project Context

This was a **Purple Team project**, combining:

### Offensive Goals

* Automate reconnaissance using Nmap
* Reduce manual scanning overhead
* Improve scan result clarity and consistency

### Defensive Goals

* Detect scanning activity using IDS/IPS tools
* Correlate Nmap activity with firewall and log data
* Visualize suspicious behavior and alert on it

My primary responsibility was the **offensive automation and scan visualization pipeline**.

---

## Features

* **Interactive Nmap Automation**

  * User-defined targets, scan options, output filenames, and scan intervals

* **Preconfigured Scan Profiles**

  * Quick execution of extensive scans using safe default options

* **Source IP / Interface Spoofing**

  * Optional interface selection and spoofing support for testing detection systems

* **XML-to-HTML Transformation**

  * Converts raw Nmap XML output into readable, styled HTML reports using XSLT

* **Timestamped Output**

  * Prevents overwriting scans and enables historical comparison

* **Organized Scan Storage**

  * Centralized folder structure for consistent scan artifact management

---

## Automation Workflow

### End-to-End Flow

1. **User runs a scan script**

   * Chooses target, scan options, and output filename

2. **Nmap executes**

   * Scan results are saved as XML

3. **XSLT transformation**

   * XML is converted into formatted HTML for readability

4. **Artifacts stored**

   * Both XML and HTML are saved with timestamps

5. **Defensive correlation**

   * Results can be analyzed alongside IDS logs and alerts

This approach improves visibility while preserving raw data for forensic analysis.

---

## Project Structure

```
purple-team-nmap-automation/
├── README.md
├── offense/
│   ├── nmap.py              # Interactive Nmap automation script
│   ├── scanmap.py           # Preconfigured quick scan wrapper
│   ├── spoofscan.py         # Scan with source IP / interface options
│   └── nmap_to_html.xslt    # XML → HTML transformation stylesheet
├── slides/
│   └── Purple_Team_Project.pdf
└── examples/
    └── sample_scan_output/
```

---

## Tech Stack

### Automation & Reconnaissance

* **Python** – Core automation language
* **Nmap** – Network scanning and service enumeration
* **XSLT** – XML transformation for report generation

### Defensive Tooling (Project Context)

* **Snort** – IDS / IPS detection
* **UFW** – Host-based firewall
* **Splunk** – Log aggregation and alerting
* **Security Onion** – IDS monitoring with Zeek and Suricata

---

## Usage

### Run an Interactive Scan

```bash
python offense/nmap.py
```

You will be prompted for:

* Target host or network
* Scan options
* Output filename
* Scan frequency (optional)

---

### Run a Preconfigured Scan

```bash
python offense/scanmap.py
```

Executes a predefined scan profile for fast reconnaissance.

---

### Run a Spoofed Scan

```bash
python offense/spoofscan.py
```

Allows selection of network interface and source IP options for detection testing.

---

## Defensive Integration

Although this repository focuses on automation, it was designed to integrate with defensive systems:

* **Snort**

  * Detects SYN scans and aggressive probing
* **UFW**

  * Logs blocked and allowed traffic for correlation
* **Splunk**

  * Alerts on repeated or anomalous login and access activity
* **Security Onion**

  * Visualizes scan behavior using Zeek and Suricata logs

This provided real-world visibility into how reconnaissance appears from a defensive perspective.

---

## Code Quality & Design

* Modular script design for easy extension
* Clear separation between scanning logic and output formatting
* Human-readable reports without sacrificing raw data
* Designed for reproducibility and monitoring rather than one-off scans

---

## Future Improvements

Planned enhancements include:

* [ ] Unified CLI interface with argument parsing
* [ ] Export scan summaries as CSV or JSON
* [ ] Automatic diffing between scan runs
* [ ] Dockerized environment for repeatable execution
* [ ] Deeper integration with SIEM platforms

---

> **Note:** This repository reflects my individual contributions within a collaborative Purple Team project.
> The included scripts and configurations demonstrate the automation and visualization components I implemented.

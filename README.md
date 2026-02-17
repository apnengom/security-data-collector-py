##Security Data Collector & Auth System
#🛡️ Project Overview
This project is a Modular Security Framework designed for the secure capture, labeling, and structuring of security event datasets. Unlike a simple logger, this system implements an active defense layer (WAF/IDS) at the entry point and prepares data for high-level forensic analysis using Big Data tools.

Developed with a focus on Software Architecture and Blue Teaming, the system is optimized for resilience, even in resource-constrained environments (tested on mobile ARM environments and x86 desktops).

#🏗️ Architecture & Design Patterns
The system follows a strict Separation of Concerns (SoC), divided into 6 distinct layers as defined in the project's Technical Structure:

*Interfaces (GUI): Decoupled views using the Mediator Pattern.

*API/Connection: Flask-based REST API.

*Business Logic: Core operations and session management.

*Security Layer: Real-time payload inspection and signature analysis.

*Database: Structured storage in SQLite with referential integrity.

*Analysis: Forensics and reporting via sqlite3.

*Key Technical Decisions:
Mediator Pattern: Implemented in AppController to manage navigation between Login, Register, and Dashboard without circular dependencies.

*Memory Resilience: Advanced cleanup using after_cancel loops in Tkinter to prevent memory leaks and zombie processes in low-RAM devices (Samsung A207).

*Async Networking: Multi-threaded client requests to ensure a non-blocking UI during server synchronization.

#🔒 Security Features
*This system acts as a First Line of Defense:

*Payload Inspection: Automatic detection of common attack vectors:

*SQL Injection (SQLi): Pattern matching for malicious keywords and escape characters.

*Cross-Site Scripting (XSS): Sanitization of HTML tags and script injections.

*Fingerprinting: Each event captures the client's "Digital Footprint" (IP + User-Agent Hash) for attribution.

*Severity Scoring: Events are not just logged; they are classified by risk level for the Analytic Domain.

#📊 Data Science & Forensics (PySpark)
The project is designed to bridge the gap between Operations and Analytics.

Structured Datasets: Data is exported in Parquet/CSV formats, ready for ML training.

Time-Window Analysis: Using PySpark's Window functions to detect "Burst Traffic" and Brute Force patterns across distributed IPs.

#🚀 Getting Started
Prerequisites
Python 3.12+
## 💾 Maintenance & Utility Scripts
* `requirements.txt`: Managed dependency list for environment reproducibility.
* `backup.py`: Database recovery tool. It generates a full SQL dump of the operational database to ensure data persistence and portability.

Java 8+ (Required for PySpark analysis)

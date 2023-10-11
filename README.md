# Web Scraping with Python

This Python script is used for web scraping data from a website of Unand University's lecturers' directory.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Functionality](#functionality)
- [Code Explanation](#code-explanation)
- [License](#license)

## Overview

This script scrapes data of lecturers from the Unand University directory website. The data includes information such as name, NIP, NIDN, gender, status, position, unit, faculty, rank, and the highest education level attained by the lecturers. The script navigates through the pages and profiles to extract this data and saves it to a CSV file for further analysis or use.

## Prerequisites

Before running the script, ensure you have the following prerequisites:

1. Python 3 installed on your system.
2. Required Python libraries (`requests`, `BeautifulSoup`, `csv`).
3. Active internet connection to fetch web content.

You can install the necessary libraries using pip:

```bash
pip install requests beautifulsoup4

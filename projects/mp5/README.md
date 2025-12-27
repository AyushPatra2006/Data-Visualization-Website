# Data Visualization Website

A Flask-based web application for exploring, visualizing, and serving datasets through interactive pages and APIs.

## Overview
This project provides a data-driven website that allows users to browse a dataset, download it via a JSON API, and view analytical visualizations. The application also includes A/B testing to optimize user engagement and email subscription with server-side validation.

## Features
- **Data Browsing**
  - Full dataset rendered as an HTML table
  - JSON API endpoint for programmatic access
  - Per-IP rate limiting to prevent abuse
- **A/B Testing**
  - Two homepage variants tested to optimize donation click-through rates
  - Automatically selects the best-performing version
- **Email Subscription**
  - Regex-based email validation
  - Persistent subscriber storage
- **Data Visualization Dashboard**
  - Multiple SVG plots generated using Matplotlib
  - Query-string–driven visualizations for comparative analysis

## Tech Stack
- **Backend:** Python, Flask
- **Data Processing:** Pandas
- **Visualization:** Matplotlib (SVG)
- **Frontend:** HTML, JavaScript (jQuery)

## Example Routes
- `/browse.html` – View dataset as an HTML table  
- `/browse.json` – Download dataset in JSON format (rate-limited)  
- `/visitors.json` – List of JSON API visitors  
- `/dashboard*.svg` – Dynamic SVG visualizations  

## Notes
This project focuses on clean API design, data visualization, and experimentation-driven optimization.

<a name="readme-top"></a>


<div align="center">
  <p align="center">
    <a href="https://www.youtube.com/@nqkdev">View Demo</a>
    ·
    <a href="https://github.com/nqkhanh2002/VINBIGDATA-CTAI-Weather-Forecast/issues">Report Bug</a>
    ·
    <a href="https://github.com/nqkhanh2002/VINBIGDATA-CTAI-Weather-Forecast/pulls">Request Feature</a>
  </p>
</div>
<div align="center">
  <img src="source/img/vinbigdata_banner.webp">
</div>
<h1 align="center">VINBIGDATA CTAI WEATHER FORECAST</h1>
<div align="center">
  <img src="source/img/topic_banner.png">
</div>
## Overview
This project is part of VINBIGDATA's Machine Learning initiative, focusing on weather forecasting using advanced machine learning techniques. This repository is maintained by Group 2 and includes all necessary code and dependencies to set up and run the project.

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/nqkhanh2002/VINBIGDATA-CTAI-Weather-Forecast.git
cd VINBIGDATA-CTAI-Weather-Forecast
```

### 2. Create a Virtual Environment
To maintain the consistency of dependencies, create a virtual environment for the project:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment
Activate the virtual environment using the following command:

- On Windows:
  ```bash
  .\.venv\Scripts\activate
  ```

- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

### 4. Install Required Dependencies
Install all necessary dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 5. Setup Kaggle API
Ensure you have your Kaggle API credentials stored in a `.json` file. Then, set up the Kaggle dataset download:

```bash
py .\source\crawl\download_kaggle_dataset.py
```

### 6. Update the Requirements
After making changes to the code or adding new dependencies, make sure to update the `requirements.txt` file to reflect the current state of the environment:

```bash
pip freeze > requirements.txt
```

## Running the Project
With everything set up, you can now run the scripts, develop models, and perform any required tasks as specified in the project scope.
# AIGC Answer Verification System

This project is a web application designed to upload CSV files, generate AI responses, and compare them with standard answers. The application uses Flask as the web framework and integrates various tools to provide AI-generated answers and their confidence scores.

## Project Structure

AGICFinal/
│
├── ai_match.py
├── app.py
├── data/
├── pycache/
├── static/
│ └── style.css
├── templates/
│ ├── index.html
│ ├── upload.html
│ ├── history.html
│ └── history2.html
├── uploads/
├── nohup.out
└── requirements.txt

## Files and Directories

- `ai_match.py`: Contains the logic for matching AI responses with standard answers.
- `app.py`: The main Flask application that handles routes and integrates various functionalities.
- `data/`: Directory to store data files.
- `__pycache__/`: Directory for Python cache files.
- `static/`: Directory for static files like CSS.
  - `style.css`: Stylesheet for the web application.
- `templates/`: Directory for HTML templates.
  - `index.html`: Main page of the application.
  - `upload.html`: Page for uploading CSV files.
  - `history.html`: Page for viewing history records.
  - `history2.html`: Additional history page.
- `uploads/`: Directory to store uploaded files.
- `nohup.out`: File to store logs when running the app with `nohup`.
- `requirements.txt`: File listing all the dependencies required for the project.

## Installation

### Prerequisites

- Python 3.6 or higher
- Virtualenv

### Steps

1. **Clone the repository**:

   ```bash
   git clone <[repository-url](https://github.com/zzhzhhhh/AIGCFinal)>
   cd AGICFinal
2.**install some modules**:
  pip install requests
  pip install openai
  pip install pandas
  pip install flask
  pip install nlkt
3.**complie and run it**
 cd app.py
 python app.py

 ## Usage

### Upload CSV File

1. Go to the **Upload CSV File** page.
2. Select a CSV file and click **Upload**.

### View History Records

1. Go to the **View History Records** page.
2. Use the provided tools to fetch AI answers and compare results.

### Export Data

1. Click on **Export Data** to download the results in CSV format.


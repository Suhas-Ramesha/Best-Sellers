# Amazon Bestselling Books Analysis with Python

In this article, I’m going to introduce you to a data science project on **Amazon Bestselling Books Analysis** using Python. The dataset consists of Amazon’s 50 Best Books between 2009 and 2019 – categorized into fiction and non-fiction using Goodreads. With a total of 550 books, this project dives into data preparation, visualization, and analysis.

## Demo

You can view the live demo of the Streamlit dashboard here:  
[Streamlit Demo](https://best-sellers-cre7gx3kmprgrcyvj9appjt.streamlit.app/)


## Project Overview

This project covers:
- **Data Loading & Preprocessing:**  
  Renaming columns, correcting inconsistent author names, and computing new metrics such as the length of book names and the percentage of punctuation.
- **Data Visualization:**  
  Visualizations include:
  - Distribution of genres for unique books (donut pie chart)
  - Yearly genre distribution across two time periods (2009–2013 and 2014–2019)
  - Top authors for Fiction and Non-Fiction categories
  - Top 20 best-selling authors analysis based on appearances, unique books, and total reviews


## Installation

To run this project locally, follow these steps:

### 1. Clone the Repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

###2. Create a Virtual Environment (optional but recommended):

```bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

###3. Install the Dependencies:

```bash
Copy
Edit
pip install -r requirements.txt
```
The minimal requirements.txt for this project is:

```txt
Copy
Edit
streamlit>=1.0
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.12.0
```

###4. Download and add the Dataset:

You can download the dataset from Kaggle:
[Amazon Top 50 Bestselling Books (2009-2019) - Kaggle](https://www.kaggle.com/sootersaalu/amazon-top-50-bestselling-books-2009-2019/download)

After downloading, place the file bestsellers with categories.csv in the project directory.
###5. Run the App:

```bash
Copy
Edit
streamlit run app.py
```

###About the Code
The main script app.py contains the following sections:

Data Loading & Preprocessing:
Functions to load the CSV file and preprocess the data (e.g., renaming columns, correcting author names, and computing new features).

Visualization Functions:
Functions to create different plots such as:

Donut pie chart showing genre distribution
Yearly genre distribution across two different periods
Bar charts for top authors and unique book counts

Streamlit App Layout:
A sidebar to select between various visualizations and a main area that displays the corresponding analysis.

###Acknowledgments
This project is based on the dataset of Amazon’s best selling books from 2009 to 2019.
Special thanks to all the contributors and the community for their continuous support.

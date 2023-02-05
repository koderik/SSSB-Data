# Welcome to SSSB-Data!
This personal website contains a tool that scrapes the maximum queue days data for all apartments on the SSSB.se website using Selenium, BeautifulSoup4, and chromedriver. The collected data is then uploaded to a PostgreSQL database.

## Features
A webpage built with Flask and HTML that displays the queue days information using some JavaScript.
A tool made with Tableau that allows you to upload PDFs and calculate your grade point average.
## Getting Started
To run the website locally, you'll need to have the following software installed on your computer:

* Python 3.x
* Selenium
* BeautifulSoup4
* Flask
* chromedriver
* PostgreSQL

Clone the repository and install the dependencies by running the following command in your terminal:


```
pip install -r requirements.txt
```
Running the Tool
To run the tool, execute the following command in your terminal:

```
python3 app.py
```
The website will be available at http://localhost:5000.

## Note
* Please make sure that you have the chromedriver executable in your PATH.
* You'll need to set up the PostgreSQL database and configure the database settings in the code.
* You might need to set ```force_https=False``` in ```app.py``` to run locally
## Visit the Website
The website is available online at http://SSSB.tech.

## Conclusion
With this tool, you can easily scrape the maximum queue days data for all apartments on the SSSB.se website and display it in a user-friendly format. The tool also provides a way to calculate your grade point average, making it a versatile tool for personal use.




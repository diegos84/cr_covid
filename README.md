# CR COVID Guide
___
  ## Project

  Provide solutions for tourists looking to visit Costa Rica safely during the pandemic. These include information about the requirements for entry into the country from abroad, live statistics about COVID's impact in Costa Rica vs. any country in the world, a collection of the most recent news in english about COVID-19 in Costa Rica and a license plate lookup tool to aid with the country's vehicular restriction.

  ## Ramp-up
  1. CD into the project root and create a virtual environment: `python3 -m venv env`
  1. Activate the virtual environment: `. env/bin/activate`
  1. Install dependencies: `pip3 install -r requirements.txt`
  1. Create a file called *project.db* inside the *application* directory.
  1. Set the following environment variables inside your virtual environment:

  >Use/create a gmail account for setting the EMAIL_USER and EMAIL_PASS environment variables
  
  ```bash
  export FLASK_APP=application/__init__.py
  export SECRET_KEY= enter a secret key of your choosing
  export EMAIL_USER= your gmail user
  export EMAIL_PASS= your gmail's password
  export SQLALCHEMY_DATABASE_URI=sqlite:///project.db
  ```
  6. Run flask at the root of the project: `flask run`

  ## Features
  
  #### 1. Statistics comparison tool to help understand the situation in Costa Rica by comparing it to the visitor's country of choice.

 ![Stats comparison tool](application/static/readme/stats.png?raw=true "Stats comparison tool")
 
  <br />
  
  #### 2. Collection of news articles in english about COVID-19 in Costa Rica only. News scrapped from The Tico Times website.

  ![News scrapper](application/static/readme/news.png?raw=true "News scrapper")
  
  <br />
  
  #### 3. License plate lookup tool to aid the visitor understand the vehicular restriction in Costa Rica.

  ![License plate lookup tool](application/static/readme/licenseplates.png?raw=true "License plate lookup tool")

  ## Academic value

  #### Back-end
  The project was developed as a package using Python's framework Flask. It includes a registration process in order to use a database and different types of forms for complexity and security features like password encryption and password reset via automated email using a link with an embedded token. Its configuration settings have been created into a class to allows using inheritance when setting up different configurations if needed. The stats comparison tool makes an API call (using Postman), the license plate lookup tool heavily relies on Jinja2 templating engine and the news articles are scrapped using the Beautiful Soup library.
  <br />
  ### Front-end
  The project relies on Bootstrap for its styling. It also uses additional features like smooth scrolling for navigation, fixed background image and opening embedded links in separate tabs.

  ## Credits
  
* This project was created as a final project for [CS50 Introduction to Computer Science](https://cs50.harvard.edu/x/2020/) course, where I learned most of the things I'm putting into practice here.
* The project also relies heavily on [Corey Shafer's YouTube tutorials](https://www.youtube.com/user/schafer5) for Flask web development.
* The news scrapping comes courtesy of [The Tico Times](https://ticotimes.net/).

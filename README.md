Features
- Parse sentences input by the user.
- Display the parsing result on the web page.
- Backend parsing logic implemented in Python.


Running the Application
1. Set environment variables
 On Windows:
 set FLASK_APP=app.py
 set FLASK_ENV=development
 On Unix or MacOS:
 export FLASK_APP=app.py
 export FLASK_ENV=development
2. Run the Flask application
 flask run
 This will start the server on http://127.0.0.1:5000/.
3. Access the web application
 Open a web browser and navigate to http://127.0.0.1:5000/ to use the application.
Usage
1. Enter a sentence in the input field on the webpage.
2. Click the "Parse Sentence" button.
3. The parsing result will be displayed below the input field.
Sentence Parsing Web Application

Project Structure
- app.py: Flask application entry point.
- parser/: Contains the Python module for parsing logic.
 - __init__.py: Makes Python treat the directories as containing packages.
 - parser_1.py: The Python script containing parsing logic.
 - parser.ebnf: The EBNF grammar file.
- templates/: HTML files for the frontend.
 - index.html: The main webpage template.
- static/: Contains CSS and JavaScript files.
 - /css/style.css: (Optional) CSS styles for your HTML page.
 - /js/script.js: JavaScript file to handle frontend logic.

# Section 261-262: First webserver with python
#
# To run again the server:
#       1. Activate the venv:
#               C:\Users\Angel\Desktop\python_workspace\webDevelopment_udemy\vent\Scripts>activate.bat
#       2. Export as variable the name of the python script containing the server:
#               > set FLASK_APP=01_261_first_webServer.py
#               (optional) > set FLASK_ENV=development
#       3. Go to: C:\Users\Angel\Desktop\python_workspace\webDevelopment_udemy\
#               > flask run
#
# Useful links
#   - Python virtual environments https://realpython.com/python-virtual-environments-a-primer/
#   -       https://stackoverflow.com/questions/1783146/where-in-a-virtualenv-does-the-custom-code-go
#   -       https://docs.python.org/3/library/venv.html
#   - Flask documentation: https://flask.palletsprojects.com/en/1.1.x/
#           - Python has an http.Server in the standard library: but not recommended for production
#           - Instead use a framework as Flask (kitchen that all ingredients and tools for cooking)
#           - Django is a bigger framework: Flask is cleaner and smaller
#           - For Flask it is recommended to create a virtual environment:
#                       https://flask.palletsprojects.com/en/2.0.x/quickstart/
#                       - python3 -m venv venv
#                       - The 2nd argument is the location to create the venv. Generally, you can just
#                           create this in your project and call it venv. Venv will create a virtual
#                           Python installation in the venv folder
#                       - As I am using Pycharm for each project a venv folder is automatically created
#                       - In the video, the instructor deletes the venv folder and sets the venv at the
#                           project root:  python3 -m venv C:\Users\Angel\Desktop\python_workspace\webDevelopment_udemy
#                       - Although both methods work, having the venv folder inside your project folder
#                           is the standard
#               - Activate the environment -> run the bin inside venv:  . venv/bin/activate
#                   - How to activate venv inside pycharm? https://stackoverflow.com/questions/22288569/how-do-i-activate-a-virtualenv-inside-pycharms-terminal
#                       I follow the instructions at run:  C:\Users\Angel\Desktop\python_workspace\webDevelopment_udemy\venv\Scripts\activate.bat
#                       but this does not seem to make a difference
#                   > THIS INSTRUCTIONS OF PYCHARM ARE FROM 2022 https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env
#                       Windows ->   Shell=cmd.exe   -> C:\> <venv>\Scripts\activate.bat
#                          SOLUTION: I activate env from outside PyCharm -> in cmd -> It shows <venv>
#
#       - Install Flask:  pip3 install flask
from html import escape

from flask import Flask, render_template, url_for, redirect, request
import random
import csv

app = Flask(__name__)
print(__name__)


@app.route('/')
def hello_world():
    return 'Hello you are becoming a great expert!'


# you need to export the a variable FLASK_APP=01_261_first_webServer.py
#   in cmd:   set FLASK_APP=01_261_first_webServer.py
# then at cmd: ...\webDevelopment_udemy> flask run
#                       > this works because the venv is active.
#                               > another option would be:  python -m flask run
#       Gives a warning: dev. server!
# running on http://127.0.0.1:5000/
# IMPORTANT: to run in development mode: so that code changes refresh in browser automatically:
#       set FLASK_ENV=development

# Section 264: Flask RENDERING TEMPLATES: https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates
@app.route('/blog')
def blog():
    return 'These are my thoughts on blogs'


@app.route('/blog/2020/dogs')
def blog_entry():
    return 'This is my dog in year 2020'


# 264 RENDER A HTML USING RENDER_TEMPLATE:
# Important: flask requires template folder!
@app.route('/rendered-template1')
def rendered_template1():
    # Section 267: Templating engine
    #       > Jinja (template engine): https://en.wikipedia.org/wiki/Jinja_(template_engine)
    #       > https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
    # next instruction gets printed in cmd server console
    print("Example of url_for: " + url_for('static', filename='heart_one_in_one.ico'))
    return render_template('index2.html')
    # CLARIFIED/SOLVED -> IT SEEMS IF THE ROUTE IS /blog/rendered-template1,
    #                 THEN FLASK EXPECTS THE TEMPLATES TO BE UNDER /blog/templates...
    #   -> Solution: in those cases, use url_for at the html (See def hello user below)
    #          Creating a folder <subpath>/static/files(e.g. js, css) does not work


number_of_visits = 0


@app.route('/aboutme')
def rendered_template2(number_of_visits=number_of_visits):
    # number_of_visits=0
    # number_of_visits=number_of_visits+1
    #       Challenge: how do I update a variable at a higher scope! -> persistence
    #               -> Ideal: do a call to a db (counter storage) at this place
    number_of_visits = random.randint(0, 9999)
    return render_template('about0.html', novisits=number_of_visits)


# SECTION 266: Adding a favicon: https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
# Free ico (favicons:) https://icon-icons.com/
# You just need to add <link rel="shortcut icon" href="{{ url_for('static', filename='heart_one_in_one.ico') }}"> to the html
#               this is equivalent to:  <link rel="shortcut icon" href="static/heart_one_in_one.ico">.
#                       See above about templating engine
# No need to add python code for this (although there is a variation that uses it, see Flask documentation


# TO LEARN MORE: FLASK TEMPLATE TUTORIAL https://pythonbasics.org/flask-tutorial-templates/


# SECTION 267 URL parameters and variable rules
#  https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules
@app.route('/hellouser/<username>/<int:post_id>')
def hello_user(username=None, post_id=None):
    return render_template('index3.html', name=username, post_id=post_id)


@app.route('/pay/<float:amountToPay>')
def storeAmountToPay(amountToPay=None):
    # the line after return gets rendered as a plain html
    # Float format uses  . as decimal separator
    return 'Amount to pay: %f' % amountToPay


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after path
    return 'Subpath: %s' % escape(subpath)


# SECTION 278. MIME TYPES  https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
#     Browsers use mime type (not the file extension) to determine the type of file
#     Examples: application/javascript, text/html, text/css...
#     Star Wars API integrations:  swapi.co
#       > Nothing to program here, just an explanation of what an api is, and that an API method
#               does not need to return html, most of them return json

# SECTION 279: BUILDING A PORTFOLIO
#       Free html5/css3 free templates: http://www.mashup-template.com/templates.html
#           use the "universe" template -> Download option: html
#           > Steps to use the template:
#               - Remove unnecesary files. see file my-readme.txt
#               - move html files to templates folder
#               - move css, js, and assets folder to static folder
#               - Rename references to .css, .js and ico to contain static
#               - Create an app route and set the html inside render_tempalte
# @app.route('/cool-template/')
@app.route('/universe')
def use_cool_template():
    # return redirect(url_for('/universe/index.html'))
    # return redirect('http://localhost:5000/universe/index.html')
    return render_template('index_entry.html')


# TODO: Investigate / Research -> How to do a redirection from /universe to /universe/index.html
#           so that it is not necessary to duplicate index_extry.html? Maybe with a script?

"""
Section 273: REFACTORING -> THESE BLOCKS CAN BE REPLACED WITH JUST ONE METHOD: see below 
@app.route('/universe/index.html')
def use_cool_template1():
    return render_template('index.html')
    # REMEMBER: As this pages are relative to universe, the css, js need to use url_for

@app.route('/universe/works.html')
def use_cool_template2():
    return render_template('works.html')

@app.route('/universe/about.html')
def use_cool_template3():
    return render_template('about.html')

@app.route('/universe/contact.html')
def use_cool_template4():
    return render_template('contact.html')

@app.route('/universe/components.html')
def use_cool_template5():
    return render_template('components.html')

@app.route('/universe/work.html')
def use_cool_template6():
    return render_template('work.html')
"""


@app.route('/universe/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


# SECTION 271: FREE HTML TEMPLATES
# The web is full of free website templates that you can use! In the videos, we learned about http://www.mashup-template.com/templates.html, but there are many other ones. For example, some of my favourite ones include:
# New: https://html5up.net/ (This is the best)
# Creative Tim Templates https://www.creative-tim.com/bootstrap-themes/ui-kit?direction=asc&sort=price

# SECTION 274: REQUEST DATA -> FORMS
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#accessing-request-data
@app.route('/universe/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            print(data)
            # write_to_textfile(data)
            write_to_csv(data)
            # read_from_csv() # -> Esto da fallo!! fichero abierto?
            return redirect('/universe/thankyou.html')
        except:
            return 'Problem saving to database csv'
    else:
        return 'something went wrong'


def write_to_textfile(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        message = data["message"]
        subject = data["subject"]
        file = database.write(f'\n{email},{subject},{message}')


# SECTION 278. USE OF EXCEL / CSV FILES !!
# https://docs.python.org/3/library/csv.html
# Section 279 -> Quick fix: newline -> About the new line in csv:
#       Heads up! In the previous video we added a parameter newline='' to the csv.writer().
#       But instead, we should add it to our open statement like this:
#               # with open('database.csv', newline='', mode='a') as database2:
# You can learn more about it here.
#   -> BUENO, parece que hay un prblema con el tema del newline, pero soy pragmatico:
#       al definir el csv le anado al final un retorno de carro en la cabecera y resuelto!
#       y para que al escribir nuevas lineas solo se introduzca CRLF es necesario poner
#       el parametro newline='' en with(open) -> newline='' en csv.writer da fallo!
def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database_csv:
        email = data["email"]
        message = data["message"]
        subject = data["subject"]
        csv_writer = csv.writer(database_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow([email, subject, message])


# Additional: este lo hago yo -> leer csv file : https://docs.python.org/3/library/csv.html
def read_from_csv():
    with open('database.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        print("---- START READING CSV FILE-----")
        lines = []
        for row in reader:
            stringline = ', '.join(row)
            print(stringline)
            lines.append(stringline)
        print("-----END READING CSV FILE------")
        return lines


@app.route('/universe/read_csv_database')
def read_csv_file():
    lines = str(read_from_csv())
    # return 'Subpath: %s' % escape(subpath)
    return 'csv contents: %s ' % lines

# SECTION 283: DEPLOY WWW IN PYTHONANYWHERE!
#    Portfolio result:    https://github.com/aneagoie/portfo
#   https://www.idkrtm.com/what-is-the-python-requirements-txt/ -> list of dependencies...
#   https://help.pythonanywhere.com/pages/Flask/
#   project link: http://andrein.pythonanywhere.com/
#   Logo makers: https://zerotomastery.io/resources/7
# Files to upload to pythonanywhere:
#      database.csv, server.py, static folder, templates folder
#      not necessary: bin, include, lib -> are for the venv
# To get a file with the necessary dependencies:
#       pip freeze > requirements.txt
            # click==8.1.3
            # colorama==0.4.6
            # Flask==2.2.2
            # itsdangerous==2.1.2
            # Jinja2==3.1.2
            # MarkupSafe==2.1.1
            # Werkzeug==2.2.2
#       Important: run it at the console of PyCharm!
#               it I run it at cmd windows cosole then I get the
#               dependencies of the boto3 project...
#
# I copy the required fields to folder deployment_upload_pythonany
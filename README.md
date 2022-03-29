


README.md


Money LAWNdering
This app creates a marketplace for property owners to list jobs such as lawn mowing and snow removal, and for workers to find work and build a clientele.

Workspace layout
The Money LAWNdering web app will be stored in this repository

Documentation and resources for this project will be kept in the “docs” folder. This will include use case diagrams, the project plan, database diagrams, and more as the project progresses.

The actual web app building project will be kept in the folder “app”

Version-Control procedures
Collaborators should have a forked repository of the app in Andrew’s account of the project “6-CS3450”, in their Github. Each collaborator should clone the forked repository. Before each meeting, collaborators should submit a pull request so we can monitor progress and discuss issues.

Tool Stack description and setup procedure
Django - this will probably be the most convenient and simple way to approach this web app as Django already comes with a built in SQLite database. Because this app won’t need a large database and since we all know Django, this seemed like the most obvious choice.

Python - We will use Python v3.9 as this is what Django uses and it is what we are all most familiar with from taking CS2610.

Bootstrap - We will use this as the front-end Javascript framework for our site, as well as for styling our entire site.


Build instructions
Clone the project in git bash:
	$ git clone https://github.com/andrewObrien98/6-CS3450
Migrate in bash:
	$ python manage.py migrate
Finally to get it up and running:
	$ python manage.py runserver
Go to the location:
	Type localhost:8000/moneyLawndering in browser to see the app running

Unit Testing Instructions
Unit tests will cover all use cases laid out in the use case diagrams. These will be able to be found in the unittests.py file. The unit test class will prompt the user to select which use cases should be executed. After the user has made a selection it will display the results.

Systems Testing Instructions
Start by running an instance of the web app by first entering the correct repository and then entering the following:
	$ python manage.py runserver
Now that the app is running open up your browser and type into the address bar:
	localhost:8000/moneyLawndering
After you can login using the following credentials
	Username: admin
	Email: admin@example.com
	Password: password

With these credentials you will have access to all admin-related actions in the app.

Other development notes, as needed
Packages: Names should be in lowercase_with_underscores
Classes: Names should be in CamelCase
Interfaces: Names should be in CamelCase
Methods: Names should be in lowerCamel
Variables: Names should be in lowerCamel
Constants: Names should be in UPPERCASE_WITH_UNDERSCORES


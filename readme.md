# IL-Hub: Contextual Profile API for Federated Systems

## CM3070 – Final Project

Repository for final project for the BSc in Computer Science at Univerity of London.
This project simulates a university environment where client apps consume personalized students' profile. 

Major features:
* Students can generate different profiles depending the app context while preserving legal/personal data in private.
* The called Il-Hub stores the different profiles built by each student.
* Social login (Google) included.
* The system uses OAuth2 capabilities to communicate between IL-Hub and app clients so that clients do not manage passwords nor usernames. A single UUID identificator is uses as main identifier between IL-Hub and clients.
* Simulated demo apps (Blog and Online Library) were created to demonstrate functionality.
* A full logging system that allow auditability process and transparency about sensitive data usage.


### Dependencies and Requirements
The whole project was developed using **WSL** over **Windows 11** and **Python 3.12.3**. *requirements.txt* contains all detailed libraries and packages.

### Unpackage and run app (local server)
**IMPORTANT: The project must run over Unix systems for a proper functioning. You must install WSL in case using Windows.**

 1. Create the environment:  `python3 -m venv .venv`
 2. Activate the environment: `source .venv/bin/activate`
 3. Install dependencies: `pip install -r requirements.txt`
 4. Run server locally: `python3 manage.py runserver`
 5. Navigate to IL-Hub: `http://127.0.0.1:8000/hub/`


 ### Testing
 Run the testing suite:

 ```python3 manage.py test```


 
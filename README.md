# Bandersnatch Monster Cards

### Business Value




### Tech Stack
- Logic: Python 3.8
- API Framework: Flask
- Templates: Jinja2
- Structure: HTML5
- Styling: CSS3
- Database: MongoDB
- Graphs: Altair
- Machine Learning: Scikit-Learn
- Demo App Hosting: Replit.com
- Database Hosting: MongoDB.com
- Landing Page Hosting: Carrd.co

### Primary Features by URL
- `/`: Splash Page
- `/data`: Tabular Data
- `/view`: Dynamic Visualizations
- `/model`: Interactive Machine Learning Model

### Development Goals
1. Sprint 1: Database Operations - Loom Video
	- Develop a database interface class
	- Create random data
	- Populate the database with at least 1000 datapoints
2. Sprint 2: Dynamic Visualizations
	- Notebook exploration
	- Chart function
	- API integration
3. Sprint 3: Machine Learning Model
	- Notebook exploration
	- Machine Learning interface class
	- Model serialization (save and open)
	- API model integration
4. Sprint 4: Deployment
   	- Deploy Demo to Replit
5. Sprint 5: Landing Page
	- Create Landing Page on Cardd
	- Add AI created Monster images

### Challenges



### OS Specific Notes: Gunicorn is not Windows compatible!
- Windows users should not use the `run.sh` shell script, as it depends on gunicorn.
- Windows users should use `py -m app.main` to start the app with Flask acting as the server.
- Mac and Linux users can use `./run.sh` script or type the command directly `python3 -m gunicorn app.main:APP`.
- Feel free to modify the shell scripts to suit your needs, these are intended to run locally.
- In any case you should not modify the Procfile, this is the run script for the remote server.

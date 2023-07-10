# LearnQuest - Backend

Welcome to the backend part of LearnQuest! This README.md file provides instructions on how to install and run the backend server for the project. 

## Installation

Please follow the steps below to install and set up the backend using Docker:

1. Clone the repository to your local machine using the following command:

   ```
   git clone git@github.com:abuwho/LearnQuest.git
   ```

2. Navigate to the project's `backend` directory:

   ```
   cd LearnQuest/backend
   ```

3. Run the following commands with Docker: 
   ```
   docker build -t learnquest-backend .
   ```
   ```
   docker run -p 8080:8080 learnquest-backend
   ```

4. Open the api endpoints on [localhost://8080](http://localhost:8080) or [http://127.0.0.1:8080](http://127.0.0.1:8080)

Congratulations! You have successfully installed the backend server for the LearnQuest project. 


## How to create a superuser from Docker desktop
1. Please go to the "containers" tab and find the running container.
2. Enter the following commands as in the picture:
```
python manage.my createsuperuser
```
![Create Superuser](/backend/docs/images/create-superuser-from-docker-terminal.png)
3. Go to http://127.0.0.1:8080/admin to access the admin panel


## Additional Notes

- Make sure to keep your dependencies up to date by periodically running `pip install -r requirements.txt` to install the latest versions of the packages.

- For production deployments, make sure to configure the project accordingly (e.g., updating `settings.py`, setting up a production database, configuring static file serving).

- If you encounter any issues or have questions, please don't hesitate to reach out to the backend developers or create an issue in the repository.

# LearnQuest - Backend

Welcome to the backend part of LearnQuest! This README.md file provides instructions on how to install and run the backend server for the project. 

## Installation

Please follow the steps below to install and set up the backend:

1. Clone the repository to your local machine using the following command:

   ```
   git clone git@github.com:abuwho/LearnQuest.git
   ```

2. Navigate to the project's `backend` directory:

   ```
   cd LearnQuest/backend
   ```

3. Create a virtual environment (`venv`) to isolate project dependencies and activate the virtual environment: (OPTIONAL)

   ```
   python3 -m venv venv
   ```
    - Activating the virtual environment
        - For Windows
            ```
            source venv/Scripts/Activate
            ```

        - For macOS and Linux:

            ```
            source venv/bin/activate
            ```

4. Install the required Python dependencies:

   ```
   pip install -r requirements.txt
   ```

Congratulations! You have successfully installed the backend server for the LearnQuest project. 

## Running the Backend Server

To start the backend server, follow these steps:

1. Make sure the virtual environment is activated.

2. Run the following command:

   ```
   python manage.py runserver
   ```

   The development server should now start running locally on `http://127.0.0.1:8000/`.

3. Open your web browser and visit `http://127.0.0.1:8000/` to access the project.

## Additional Notes

- Make sure to keep your dependencies up to date by periodically running `pip install -r requirements.txt` to install the latest versions of the packages.

- For production deployments, make sure to configure the project accordingly (e.g., updating `settings.py`, setting up a production database, configuring static file serving).

- If you encounter any issues or have questions, please don't hesitate to reach out to the backend developers or create an issue in the repository.

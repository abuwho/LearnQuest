# LearnQuest
Welcome to LearnQuest, an open-source project aimed at creating a comprehensive collection of educational resources for various subjects. This project encourages collaboration and contributions from the community to help make quality education accessible to all.

### Introduction
LearnQuest aims to provide a platform for sharing educational materials, including lecture notes, assignments, and projects. The project's goal is to foster collaboration and knowledge exchange, enabling students and educators to access a wide range of high-quality resources.

### The Application in Action

- View the deployed application on [Vercel](https://learnquest.vercel.app)

![Homepage screenshot](https://i.ibb.co/4N06RyW/image.png)

- View the API specification on [Vercel](https://learnquest-backend.vercel.app/)

![API screenshot](https://i.ibb.co/rxLH3y4/image.png)


### Instructions to Run on Your Local Machine

1. Clone the repository: 
    ```
    git clone https://github.com/abuwho/LearnQuest.git
    ```
2. Go to project root directory
    ```
    cd LearnQuest
    ```
3. Create environment variables for docker
    ```
    touch docker-backend.env
    ```

4. Add database credentials to `docker-backend.env`
    ```
    DATABASE_HOST=
    DATABASE_PASSWORD=
    ```

5. Run `docker-compose` command to run the backend and the frontend together:
    ```
    docker-compose up
    ```


### Contributing
Contribute to the project by following some rules: 
- Make changes on a separate branch (*e.g.* `feature/<feature-name>`): 
    ```
    git branch <feature/feature-name>
    ```
    ```
    git checkout <feature/feature-name>
    ```
- Commit and push changes to the remote branch
    ```
    git add .
    ```
    ```
    git commit -m "A very descriptive commit message"
    ```
    ```
    git push origin feature/<feature-name>
    ```
- Open a pull request on the main repository's `main` branch.

### License 
To be added soon

### Acknowledgements
To be added soon
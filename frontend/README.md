# LearnQuest - Frontend

Welcome to the frontend part of LearnQuest! This README.md file provides instructions on how to install and run the backend server for the project. 

## Getting Started

### 1. Running on local machine:
- Install the necessary dependencies:
    ```bash
    npm install
    ```
- (Optional) Add environment variable (if you are running the backend on Docker): 
    ```bash
    touch .env
    ```
    ```bash
    echo NEXT_PUBLIC_API_BASE_URL=http://localhost:8080 > .env
    ```
- Run the development server: 
    ```bash
    npm run dev
    # or
    yarn dev
    # or
    pnpm dev
    ```
- Open **[http://localhost:3000](http://localhost:3000)** with your browser to see the result.

### 2. Using Docker: 

- Make sure you are in the frontend directory (`LearnQuest/frontend`)
- Build the docker image: 
    ```
    docker build -t learnquest-frontend -f Dockerfile .
    ```
- Run the container: 
    ```
    docker run --env-file .env.docker -p 3030:3030 learnquest-frontend
    ```
- Go to **[localhost:3030](http://localhost:3030/)** with your browser to see the result.




## Deployed on Vercel

The application is deployed on [Vercel](https://learnquest.vercel.app)

![Homepage screenshot](https://i.ibb.co/4N06RyW/image.png)
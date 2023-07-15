# Use an official Node.js runtime as the base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /frontend

# Copy the package.json and package-lock.json files to the container
COPY package*.json /frontend/

# Install the project dependencies
RUN npm install

# Copy the project files to the working directory
COPY . /frontend/

# Expose the port that the application will run on
EXPOSE 3030

# Set the command to run the application
CMD ["npm", "run", "dev", "--", "-p", "3030"]
# Use Node.js LTS version as base image
FROM node:lts-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY bank-app/ .   

# Build your app
RUN npm run build

# Expose the port your app runs on
EXPOSE 3000

# Set the command to run your app
CMD ["npm", "start"]

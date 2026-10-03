# Use Node.js Alpine as the base image for a lightweight container
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package files first to leverage Docker layer caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application
COPY . .

# Set environment variables for build time (NEXT_PUBLIC_* vars are inlined into
# the client bundle by `next build`, so they must be present here, not just at
# container runtime via env_file/environment in docker-compose.yml)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the Next.js application
RUN npm run build

# Start the application
CMD ["npm", "start"]

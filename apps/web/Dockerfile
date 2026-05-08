FROM oven/bun:latest

WORKDIR /app

# Copy package files
COPY package.json bun.lockb ./

# Install dependencies
RUN bun install

# Copy source code
COPY app/ ./app/
COPY components/ ./components/
COPY lib/ ./lib/
COPY stores/ ./stores/
COPY types/ ./types/
COPY next.config.js ./
COPY tailwind.config.js ./

# Build the application
RUN bun run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["bun", "run", "start"]

# Build Frontend
FROM node:18 as frontend-builder
WORKDIR /app/web
COPY web/package.json web/package-lock.json* ./
RUN npm install
COPY web/ .
RUN npm run build

# Runtime Backend
FROM python:3.9-slim
WORKDIR /app

# Install dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY server ./server

# Copy built frontend
COPY --from=frontend-builder /app/web/dist ./server/static

# Expose port
EXPOSE 8000

# Run command
CMD ["python", "server/app/main.py"]

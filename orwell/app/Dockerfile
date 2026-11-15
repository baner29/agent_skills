FROM node:22-slim

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=8080
ENV GOOGLE_GENAI_USE_VERTEXAI=True
ENV GOOGLE_CLOUD_LOCATION=global
ENV GOOGLE_CLOUD_PROJECT=banercorp-web
ENV GEMINI_MODEL=gemini-3.8-flash

COPY package*.json ./
RUN npm install --omit=dev

COPY server.js banned.json banned-ai-words.md ./
COPY public ./public

EXPOSE 8080
CMD ["node", "server.js"]

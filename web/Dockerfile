

FROM node:20-alpine
WORKDIR /app
RUN npm -g i serve@14
COPY static /app/static
EXPOSE 5173
CMD ["serve","-l","5173","static"]

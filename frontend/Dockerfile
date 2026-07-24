# use the official nginx Alpine image for a lightweight web server
FROM nginx:alpine

# remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# copy our frontend code to Nginx serving directory
COPY ./index.html /usr/share/nginx/html/

# expose the port 80 for web traffic
EXPOSE 80

# set the entry point for the container
CMD ["nginx", "-g", "daemon off;"]
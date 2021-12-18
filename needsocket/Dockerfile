
FROM node:latest
WORKDIR /home/needdeliver/prod/needsocket
ADD . /home/needdeliver/prod/needsocket
ADD package.json /home/needdeliver/prod/needsocket
RUN ls -al
#RUN npm cache clean --force
#RUN npm -g config set user root
#RUN npm set progress=false
#RUN rm -rf node_modules
#RUN npm list -g --depth=0
#RUN npm i -g npm-check-updates
#RUN npm install -g @angular/cli@latest
RUN npm install
#RUN npm run build
CMD ["node", "app.js"]

# production environment
#FROM nginx:1.13.9-alpine
#RUN rm -rf /etc/nginx/conf.d
#COPY conf /etc/nginx
#COPY --from=needsocket /home/needdeliver/prod/needsocket/dist /usr/share/nginx/html
#COPY --from=needsocket /home/needdeliver/prod/needsocket/public /usr/share/nginx/html/public
#workdir /usr/share/nginx/html
#RUN ls -al
#CMD ["nginx", "-g", "daemon off;"]



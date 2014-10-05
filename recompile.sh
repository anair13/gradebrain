export MONGO_USERNAME="gradebrain"
export MONGO_PASSWORD="calhacks2014"
export RAILS_ENV=production
rvm use 2.0.0
bundle exec rake assets:precompile
sudo killall nginx
sudo /opt/nginx/sbin/nginx

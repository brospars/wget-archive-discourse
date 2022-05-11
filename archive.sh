if [ -f .env ]
then
  echo "Load .env"
  export $(cat .env | xargs)
fi

# Archive using wget
wget  --recursive --level=10 \
      --no-verbose \
      --page-requisites \
      --convert-links \
      --adjust-extension \
      --compression=auto \
      --reject='*.js,*.rss' \
      --ignore-tags=script \
      --reject-regex "/search" \
      --no-if-modified-since \
      --no-check-certificate \
      --execute robots=off \
      --random-wait \
      --wait=0.3 \
      --user-agent="Googlebot/2.1 (+http://www.google.com/bot.html)" \
      --no-cookies \
      --no-host-directories \
      --no-directories \
      --header "Cookie: $DISCOURSE_COOKIE" \
      --directory-prefix=export/$DISCOURSE_NAME \
      "$DISCOURSE_URL"

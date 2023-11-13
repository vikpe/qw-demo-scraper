DIRNAME=${1}

if [ -z "$DIRNAME" ]
then
      echo "\$DIRNAME is empty"
      exit 1
fi

# sha256
find $DIRNAME -type f -name '*.mvd' -exec sha256sum '{}' \; > $DIRNAME/demos.sha256

# mvdparser
(
  cd mvdparser
  find ../$DIRNAME -type f -name '*.mvd' -exec ./mvdparser_linux_amd64 {} \;
)

# compress
find $DIRNAME -type f -name '*.mvd' -exec gzip -f -k '{}' \;

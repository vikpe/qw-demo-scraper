# sha256
find demos -type f -name '*.mvd' -exec sha256sum '{}' \; > demos/demos.sha256

# mvdparser
(
  cd mvdparser
  find ../demos -type f -name '*.mvd' -exec ./mvdparser_linux_amd64 {} \;
)

# compress
find demos -type f -name '*.mvd' -exec gzip -f -k '{}' \;

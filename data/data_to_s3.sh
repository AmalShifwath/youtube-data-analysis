for file in *; do
  country="${file:0:2}"
  if [[ $file == *.json ]]; then
    aws s3 cp "$file" "s3://amal-de-youtube-analysis-raw-dev/raw_statistics_json/$file"
  elif [[ $file == *.csv ]]; then
    aws s3 cp "$file" "s3://amal-de-youtube-analysis-raw-dev/raw_statistics_csv/$country/$file"
  fi
done
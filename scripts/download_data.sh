#!/bin/bash
mkdir -p data
base_url="https://football-data.co.uk/mmz4281"
# Seasons: 2526 (Current), 2425, 2324, 2223, 2122, 2021, 1920, 1819, 1718, 1617
seasons=("2526" "2425" "2324" "2223" "2122" "2021" "1920" "1819" "1718" "1617")

for season in "${seasons[@]}"; do
    url="${base_url}/${season}/E0.csv"
    output="data/${season}_E0.csv"
    echo "Downloading $season from $url..."
    curl -s -o "$output" "$url"
    
    # Check if file is valid (not 404 HTML page)
    if grep -q "<!DOCTYPE html>" "$output"; then
        echo "Error: $season not found (404)"
        rm "$output"
    else
        echo "Saved to $output"
    fi
    
    sleep 1 # Be nice to the server
done
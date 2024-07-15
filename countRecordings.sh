#!/bin/bash

# Function to recursively count files
count_files() {
    local dir=$1
    local count=0

    # Count files in the current directory
    for file in "$dir"/*; do
        if [ -f "$file" ]; then
            count=$((count + 1))
        elif [ -d "$file" ]; then
            # If it's a directory, recursively count files in it
            count=$((count + $(count_files "$file")))
        fi
    done

    echo $count
}

# Check if the directory argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Call the function with the provided directory
total_count=$(count_files "$1")

echo "Total number of files: $total_count"

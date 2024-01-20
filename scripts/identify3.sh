#!/bin/bash

height_option=false
width_option=false
filesize_option=false

while getopts "hws" opt; do
    case $opt in
        h)
            height_option=true
            ;;
        w)
            width_option=true
            ;;
        s)
            filesize_option=true
            ;;
        *)
            echo "Invalid option"
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [-h|-w|-s] <input_file>"
    exit 1
fi

input_file="$1"

# Get the first line
first_line=$(head -n 1 "$input_file")

# Initialize the header
header=""

# Build the header based on selected options
if $height_option; then
    header+="Height"
fi

if $width_option; then
    if [ -n "$header" ]; then
        header+=",Width"
    else
        header="Width"
    fi
fi

if $filesize_option; then
    if [ -n "$header" ]; then
        header+=",Filesize"
    else
        header="Filesize"
    fi
fi

# Echo the header
echo "$header"

# Skip the first line
sed '1d' "$input_file" | while IFS= read -r line; do
    if [ "$line" == "null" ]; then
        echo "null,null,null"
    else
        # Check if the file extension is gif
        if [[ "$line" == *.gif ]]; then
            echo "null,null,null"
        else
            # Initialize output variables
            height_output=""
            width_output=""
            filesize_output=""

            # Get information based on selected options
            if $height_option; then
                height_output=$(identify -format "%h" "$line" 2>/dev/null)
            fi

            if $width_option; then
                width_output=$(identify -format "%w" "$line" 2>/dev/null)
            fi

            if $filesize_option; then
                filesize_output=$(identify -format "%B\n" "$line" 2>/dev/null)
            fi

            # Print the results
            echo "$height_output,$width_output,$filesize_output"
	    sleep 1
        fi
    fi
done

#!/bin/bash

# Endpoint URL
base_url="https://welovetheart.optimism.io/wp-json/wp/v2"
post_type="mint"
media_endpoint="$base_url/media"
output_file="posts_data.csv"

get_next_page_url() {
    local current_page=$1
    local collection_cb_class=$2
    local collection_cb_method=$3
    local offset=$4
    local next_page=$5
    local collection_container=$6
    local ppp=$7

    local next_page_url="https://welovetheart.optimism.io/wp-json/MINTER/v1/pagination?offset=$((ppp * (next_page - 1)))&current_page=$((current_page))&next_page=$((current_page + 1))&ppp=$ppp&collection_cb_class=$collection_cb_class&collection_cb_method=$collection_cb_method&collection_container=$((current_page))"

    echo "$next_page_url"
}


# Function to get the featured image URL
get_featured_image_url() {
    media_id=$1
    image_url=$(curl -s "$media_endpoint/$media_id" | jq -r '.source_url')
    echo $image_url
}

# Function to get category name by ID
get_category_name() {
    case $1 in
        10) echo "AI Art" ;;
        11) echo "Generative Art" ;;
        12) echo "Music" ;;
        13) echo "1of1s" ;;
        *) echo "Unknown Category" ;;
    esac
}

# Function to get platform name by ID
get_platform_name() {
    case $1 in
        2) echo "Manifold" ;;
        3) echo "Sound.xyz" ;;
        4) echo "Mint.fun" ;;
        5) echo "OpenSea" ;;
        6) echo "Decent" ;;
        7) echo "Titles" ;;
        8) echo "Highlight" ;;
        14) echo "Holograph" ;;
        15) echo "Zora" ;;
        16) echo "Stability AI" ;;
        17) echo "Base" ;;
        *) echo "Unknown Platform" ;;
    esac
}


# Initialize the output file with headers
echo "\"ID\", \"Post Title\", \"Rendered Content\", \"Featured Image URL\", \"Categories\", \"Platforms\", \"NFT Link\"" > $output_file

page=1
max_pages=704 # For testing, limit to 5 pages. Adjust as needed.

while [ $page -le $max_pages ]; do
    base_url_v1=$(get_next_page_url $page "Mints" "get_as_cards" -10 $page $page 10)
    response=$(curl -s "$base_url/$post_type?page=$page")
    response_v1=$(curl -s "$base_url_v1")
    nft_links=$(echo $response_v1 | jq -r '.' | grep -oP "href='https[^\']*'" | awk -F "'" '{print $2}')
    nft_links_array=($nft_links)

    # Check if response is empty
    if [ -z "$response" ] || [ "$response" == "[]" ]; then
        break
    fi

    # Process each post
    counter=0
    while IFS= read -r post && [ "$counter" -lt 9 ]; do
    #while IFS= read -r post || [ -n "$post" ]; do
        id=$(echo $post | jq -r '.id')
        title=$(echo $post | jq '.title.rendered')
        content=$(echo $post | jq '.content.rendered' | sed 's/<[^>]*>//g')
        featured_media=$(echo $post | jq -r '.featured_media')

        # Get featured image URL
        if [ "$featured_media" != "null" ]; then
            image_url=$(get_featured_image_url $featured_media)
        else
            image_url="No Image"
        fi

        categories=$(echo $post | jq '.mint_category[]' | while read id; do get_category_name $id; done | paste -sd ',' -)
        platforms=$(echo $post | jq '.platform[]' | while read id; do get_platform_name $id; done | paste -sd ',' -)
	nft_link=${nft_links_array[$counter]}
	#echo $base_url_v1
	#echo "$nft_links"
	#echo "$nft_links_array"
	
        echo "\"$id\", $title, $content, \"$image_url\", \"$categories\", \"$platforms\", \"$nft_link\"" >> "$output_file"
	#echo "$counter"
	#echo
	echo "$id, $title, $nft_link"
	#echo "$title"
	#echo "$content"
	#echo "$image_url"
	#echo "$categories"
	#echo "$platforms"
	#echo "$nft_link"
	#echo "-------------------"

        ((counter++))
    done <<< "$(echo "$response" | jq -c '.[]')"
    sleep $((RANDOM % 9))

    ((page++))
done


import argparse
import textwrap
import csv
import subprocess
from PIL import Image, ImageDraw, ImageFont
import html

def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

def generate_qr_code(nft_link, output_filename):
    subprocess.run(['qrencode', '-o', output_filename, nft_link])

def create_image(post_title, rendered_content, qr_code_filename, output_filename, platforms):
    # Create a blank white image
    image = Image.new('RGB', (512, 512), 'white')
    draw = ImageDraw.Draw(image)

    # Load fonts (change the paths according to your system)
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    description_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

    try:
        # Load QR code image
        qr_code = Image.open(qr_code_filename)
    except FileNotFoundError:
        print(f"No QR code found for {output_filename}. Skipping to the next row.")
        return

    # Decode HTML entities in title and description
    post_title = html.unescape(post_title)
    rendered_content = html.unescape(rendered_content)
    
    # Replace escaped characters with their literal equivalents
    post_title = post_title.replace(r'\n', '\n').replace(r'\t', '\t')
    rendered_content = rendered_content.replace(r'\n', '\n').replace(r'\t', '\t')
    
    # Wrap title text
    wrapped_title = textwrap.fill(post_title, width=20)
    
    # Draw wrapped title
    draw.text((20, 20), wrapped_title, fill='black', font=title_font)
    
    # Wrap description text
    wrapped_description = textwrap.fill(rendered_content, width=40)
    
    # Draw wrapped description
    draw.text((20, 100), wrapped_description, fill='black', font=description_font)

    # Load platforms image based on the "Platforms" value
    platforms_to_images = {
        'Decent': 'Decent.png',
        'Highlight': 'Highlight.png',
        'Holograph': 'Holograph.png',
        'Manifold': 'Manifold.png',
        'Mint_fun': 'Mint_fun.png',
        'Opensea': 'Opensea.png',
        'Sound': 'Sound.png',
        'Titles': 'Titles.png',
        'Zora': 'Zora.png',
    }

    if platforms in platforms_to_images:
        platforms_image_path = platforms_to_images[platforms]
        platforms_image = Image.open(platforms_image_path)

        # Resize the platforms image by 50%
        platforms_image = platforms_image.resize((int(platforms_image.width * 0.5), int(platforms_image.height * 0.5)))

        # Composite platforms image to the top right
        image.paste(platforms_image, (image.width - platforms_image.width - 20, 20))

    # Composite QR code to the bottom right
    image.paste(qr_code, (image.width - qr_code.width - 20, image.height - qr_code.height - 20))

    # Save the final image
    image.save(output_filename)

def main():
    parser = argparse.ArgumentParser(description="Read values from a CSV file and generate image with text, QR code, and composite image.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    try:
        data = read_csv(args.csv_file)
        for row in data:
            id_value = row['ID']
            post_title = row['Post Title']
            rendered_content = row['Rendered Content']
            nft_link = row['NFT Link']
            platforms = row['Platforms']

            # Generate QR code
            qr_code_filename = f"{id_value}_qrcode.png"
            generate_qr_code(nft_link, qr_code_filename)

            # Generate image
            output_filename = f"{id_value}_metadata.png"
            create_image(post_title, rendered_content, qr_code_filename, output_filename, platforms)

            print(f"Generated image with metadata for ID {id_value} and saved to {output_filename}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

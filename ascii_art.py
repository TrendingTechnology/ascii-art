import argparse

from PIL import Image
from utils import image_to_ascii
from weight import weigh_chars


def main(args):
    image = Image.open(args.image)

    width, height = image.size
    if args.width and args.height:
        width = args.width
        height = args.height
    elif args.width and not args.height:
        height = int(height * (args.width / width))
        width = args.width
    elif args.height and not args.width:
        width = int(width * (args.height / height))
        height = args.height

    if args.chars:
        with open(args.chars, 'r') as f:
            chars = f.read().replace('\n', '')
    else:
        chars = ' .\',:;+*?%S#@'
    weighted_chars = weigh_chars(chars, args.invert, args.normalize)

    # Generate ASCII art from image
    ascii_art = image_to_ascii(image, width, height, weighted_chars)

    # Output ASCII art
    if args.output:
        with open(args.output, 'wb') as f:
            f.write(ascii_art.encode('utf-8'))
        print('\nASCII art saved to ' + args.output, end='\n\n')

    # Print to console if small enough
    if width <= 150 and height <= 150:
        print(ascii_art)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Convert your favorite image into ASCII art')
    parser.add_argument('image', type=str,
                        help='Path to image from which ASCII art will be generated')
    parser.add_argument('-o', '--output', type=str,
                        help='Path to generated ASCII art')
    parser.add_argument('--width', type=int,
                        help='Character width of ASCII art')
    parser.add_argument('--height', type=int,
                        help='Character height of ASCII art')
    parser.add_argument('--chars', type=str,
                        help='Path to characters to be seen in ASCII art')
    parser.add_argument('--invert', action='store_true',
                        help='Whether the ASCII output color is inverted')
    parser.add_argument('-n', '--normalize', action='store_true',
                        help='Whether the weights of the provided ASCII characters are normalized')
    args = parser.parse_args()

    # Run program
    main(args)

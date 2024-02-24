import argparse
from bing_image_creator.bing_image_creator import BingImageCreator


def main():
    parser = argparse.ArgumentParser(description='CLI for Bing Image Creator')
    parser.add_argument('prompts', nargs='+', help='Prompts for image generation')
    parser.add_argument('--cookie', '-c', help='_U cookie value for authentication')
    parser.add_argument('--save-folder', '-s', default='images', help='Folder to save generated images')
    args = parser.parse_args()

    # Instantiate BingImageCreator with command-line arguments
    image_creator = BingImageCreator(args.prompts, args.cookie, args.save_folder)
    image_creator.run()


if __name__ == "__main__":
    main()

from setuptools import setup, find_packages

setup(
    name='bing_image_creator',
    version='3.9',
    description='Batch generate images with Bing Image Creator (powered by DALL-E 3) using SeleniumBase',
    author='Long Nguyen',
    author_email='meapwork@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'seleniumbase',
        'piexif',
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'bing_image_creator = bing_image_creator:main',
        ],
    },
)

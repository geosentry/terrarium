from setuptools import setup, find_packages

import pathlib
here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="terrarium",
    version="0.2.3",

    description='Earth Engine & GIS tooling Python Package for the GeoSentry Platform.',
    long_description=long_description, 
    long_description_content_type='text/markdown', 

    url='https://github.com/geosentry/terrarium',
    project_urls={ 
        'Bug Reports': 'https://github.com/geosentry/terrarium/issues',
        'Source': 'https://github.com/geosentry/terrarium',
    },

    author='Manish Meganathan',
    author_email='meganathan.manish@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    keywords='geosentry, terrarium, earthengine, GIS',

    packages=find_packages(),
    python_requires='>=3.8, <4',
    install_requires=[
        'earthengine-api==0.1.271',
        'googlemaps==4.4.5',
        'google-api-core==1.30.0',
        'google-cloud-secret-manager==2.5.0',
        'Shapely==1.7.1',
        'pyproj==3.1.0',
        'area==1.1.1'
    ],   
)
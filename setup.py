import os
from setuptools import setup

dependencies = ['gpiozero']

if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    dependencies += ['RPi.GPIO', 'spidev']
elif os.path.exists('/sys/bus/platform/drivers/gpio-x3'):
    dependencies += ['Hobot.GPIO', 'spidev']
else:
    dependencies += ['Jetson.GPIO']

setup(
    name='rpi-ai-thermocontrol',
    version='1.0.0',
    description='Temperature control system for AI module cooling',
    long_description='A Raspberry Pi based temperature monitoring and fan control system for AI module cooling',
    author='Ionut-Alexandru Banica',
    author_email='ionut.alexandru.banica@gmail.com',
    python_requires='>=3.9',
    package_dir={'': 'thermocontrol'},
    packages=['thermocontrol', 'thermocontrol.services'],
    install_requires=dependencies,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'Operating System :: POSIX :: Linux',
        'Environment :: No Input/Output Interaction',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Hardware',
        'Topic :: System :: Monitoring',
    ],
)

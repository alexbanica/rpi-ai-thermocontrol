from setuptools import find_packages, setup

setup(
    name="rpi-ai-thermocontrol",
    version="2.0.0",
    description="Temperature control system for AI module cooling",
    long_description="A Raspberry Pi based temperature monitoring and fan control system for AI module cooling",
    author="Ionut-Alexandru Banica",
    author_email="ionut.alexandru.banica@gmail.com",
    python_requires=">=3.9",
    packages=find_packages(include=["thermocontrol", "thermocontrol.*"]),
    install_requires=["gpiozero", "PyYAML"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Environment :: No Input/Output Interaction",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
    ],
)

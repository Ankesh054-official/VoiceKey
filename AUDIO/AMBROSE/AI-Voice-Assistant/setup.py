from setuptools import setup, find_packages


# from platforms.desktop.main import start

def find_long_description():
    with open('README.md', 'r') as f:
        return f.read()


def find_requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().split("\n")


setup(
    name='ASSISTANT',
    version='1.0.0',
    author='ANKESH',
    author_email='ankeshsharma@pm.me',
    description='The AI Voice Assistant project aims to deliver a'
                ' sophisticated virtual assistant that revolutionizes'
                ' the way users interact with technology, offering'
                ' unparalleled convenience, efficiency, and personalized'
                ' assistance through natural language understanding and speech recognition capabilities.',
    long_description=find_long_description(),
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/ankesh054/assistant/src/main/AUDIO/AMBROSE/AI-Voice-Assistant/',
    packages=find_packages(),
    install_requires=find_requirements(),
    entry_points={
        'console_scripts': [
            'assistant-launch = platforms.desktop.main:start',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.12.2',
        'Operating System :: WINDOWS',
    ],
)

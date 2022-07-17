from setuptools import setup
import sdist_upip

setup(    
    cmdclass={'sdist': sdist_upip.sdist},
    name='micropython-micronet',
    packages=['micronet'],
    description='MicroPython library for networking',
    long_description_content_type="text/markdown",
    long_description="MicroPython library for networking",
    url='https://github.com/yeranosyanvahan/micronet',
    author='Vahan Yeranosyan',
    author_email='vahan@yeranosyanvahan.com',
    maintainer='Vahan Yeranosyan',
    maintainer_email='vahan@yeranosyanvahan.com',
    license='MIT',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'License :: OSI Approved :: MIT License',
    ],
    setuptools_git_versioning={
        "enabled": True,
    },
    setup_requires=["setuptools-git-versioning"],

)

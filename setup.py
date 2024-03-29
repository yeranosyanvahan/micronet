from setuptools import setup,find_packages

setup(    
    name='micropython-micronet',
    packages=find_packages(),
    
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
        'License :: MIT License',
    ],
    setuptools_git_versioning={
        "enabled": True,
    },
    setup_requires=["setuptools-git-versioning"],

)

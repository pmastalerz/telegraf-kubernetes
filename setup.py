import setuptools

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()


setuptools.setup(
    name='telegraf-kubernetes',
    description='Plugin for Telegraf for gathering statistics from Kubernetes',
    version='0.0.1',
    author='Pawel Mastalerz',
    author_email='pawel@mastalerz.info',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    install_requires=read_file('requirements.txt').splitlines(),
    scripts=['telegraf-kubernetes.py'],
    )

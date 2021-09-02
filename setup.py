import setuptools

install_reqs_path = 'environment/install_requirements.txt'

read_me = """ Quantum Hardware Abstraction Layer package. """

about_info = {}
with open("qhal/__about__.py") as f:
    exec(f.read(), about_info)


def read_requirements_txt(file_name: str):
    with open(file_name) as f:
        input_lines = f.read().splitlines()

    # Remove trailing/leading whitespace, empty lines and comments
    sanitised = map(str.strip, input_lines)
    sanitised = list(filter(lambda x: not str.startswith(x, '#'), sanitised))
    sanitised = list(filter(None, sanitised))

    return sanitised


setuptools.setup(
    name="qhal",
    packages=setuptools.find_packages(include=['qhal', 'qhal.*']),
    version=about_info['__version__'],
    author="ISCF Steering committee",
    author_email=about_info['__email__'],
    description=about_info['__short_description__'],
    long_description=read_me,
    long_description_content_type='text/markdown',
    copyright=about_info['__copyright__'],
    license=about_info['__license__'],
    url=about_info['__url__'],
    platforms=about_info['__platforms__'],
    test_suite="test",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
    ],
    install_requires=read_requirements_txt(install_reqs_path),
    python_requires='==3.8.*'
)

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='kharon',
      version='0.1.5.14',
      description='Simplifying hardware/iot development with a Django style batteries-included framework',
      url='https://github.com/RedRussianBear/kharon',
      author='Mikhail Khrenov, Sahil Kochar, Shriyash Upadhyay',
      author_email='mkhrenov34@gmail.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='BSD',
      packages=['kharon'],
      package_data={'kharon': ['*', 'project_templates/*']},
      entry_points={
          'console_scripts': ['kharon=kharon.command_line:kharon'],
      },
      zip_safe=False, install_requires=['pyserial'])

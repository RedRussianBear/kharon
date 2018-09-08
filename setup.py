from setuptools import setup

setup(name='kharon',
      version='0.1.2.5',
      description='Simplifying hardware/iot development with a Django style batteries-included framework',
      url='https://github.com/RedRussianBear/kharon',
      author='Mikhail Khrenov, Sahil Kochar, Shriyash Upadhyay',
      author_email='mkhrenov34@gmail.com',
      license='BSD',
      packages=['kharon'],
      package_data={'kharon': ['*', 'projecttemplates/*']},
      zip_safe=False)

from setuptools import setup

setup(name='st_dbconf',
      version='0.1',
      description='DB stuff for skatetrax',
      url='http://github.com/kami-nashi/st_dbconf',
      author='Ashley Young',
      author_email='burning.rose85@gmail.com',
      license='MIT',
      packages=['st_dbconf'],
      install_requires=[
          'pymysql',
      ],
      zip_safe=False)
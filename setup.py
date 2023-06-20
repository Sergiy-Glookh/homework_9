from setuptools import setup, find_namespace_packages

setup(name='home_work_9_virtual_assistant_SG',
      version='0.0.1',
      description='User contact management',
      long_description=open('README.md', 'r', encoding='utf-8').read(),
      long_description_content_type='text/markdown',      
      python_requires='>=3.11',  
      classifiers = ["Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                    ],
      url='https://github.com/Sergiy-Glookh/homework_9',
      author='Sregiy Glookh',
      author_email='sglookh@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),    
      entry_points={'console_scripts': ['virtual-assistant = virtual_assistant.main:main']}
      )
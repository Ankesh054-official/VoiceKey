## Setup Guide:
> **`Documented everything encountered in development process (e.g. dependency, project issues, etc.).`**

<hr>

## Table Of Content:
1. [Create A Virtual Environment](#create-a-virtual-environment)
2. [Packaging And Distribution](#packaging-and-distribution)
3. [How To Create A setup File](#how-to-create-a-setup-file)
<hr>

#### Create A Virtual Environment:
Before doing anything we should create a virtual environment in project directory. So, that dependency should not conflict with gloal packages.

**Windows/Linux:**

Run below command in project directory to create a virtual environment.

`> python -m venv <virtual-environment-name>`
>**venv** is a built-in module in Python that allows you to create lightweight, isolated Python environments. These environments are similar to virtual environments created by tools like Virtualenv

#### Packaging And Distribution:

To make a Python project into a standalone software application, developers typically go through a process known as packaging and distribution. This involves organizing the project's code and dependencies into a format that can be easily installed and run on users' systems. Here's a general overview of the steps involved:

1. **Organize Your Project Structure:**
   Ensure your project has a well-structured directory layout. This includes separating code into modules, organizing assets, and having clear documentation.

2. **Create a Setup Script:**
   Create a `setup.py` script using Python's setuptools or another packaging tool like Poetry or Flit. This script defines metadata about your project (e.g., name, version, dependencies) and instructions for building and installing it.

3. **Define Dependencies:**
   List all required dependencies in the `setup.py` script or in a `requirements.txt` file. Ensure that your project's dependencies are properly declared to ensure smooth installation on users' systems.

4. **Write Documentation:**
   Provide clear documentation for your project, including installation instructions, usage guidelines, and any other relevant information. You can use tools like Sphinx to generate documentation from docstrings and Markdown files.

5. **Package Your Project:**
   Use the `setup.py` script to create a distributable package for your project. This can be done using the `sdist` command for source distributions or `bdist` commands for built distributions (e.g., wheel, executable).

6. **Test Your Package:**
   Before distributing your package, thoroughly test it to ensure that it works as expected on different platforms and environments. Consider using automated testing frameworks like pytest to validate your project's functionality.

7. **Choose a Distribution Method:**
   Decide how you want to distribute your software to users. Options include uploading your package to the Python Package Index (PyPI), creating binary installers for specific platforms, or distributing your software through package managers like pip or conda.

8. **Publish Your Package:**
   If you're distributing your package through PyPI, create an account and upload your package using tools like twine. Make sure to follow PyPI's guidelines for naming, versioning, and licensing your package.

9. **Handle Platform-Specific Considerations:**
   If your project relies on platform-specific features or dependencies, ensure that these are properly documented and handled. You may need to provide separate distributions or instructions for different platforms.

10. **Continuous Integration and Deployment (CI/CD):**
    Set up CI/CD pipelines to automate the process of building, testing, and deploying your software. This ensures that your package remains consistent and up-to-date with each code change.

By following these steps, you can package your Python project into a standalone software application that can be easily installed and run by users. Remember to maintain your project over time by updating dependencies, addressing bugs, and incorporating user feedback.

#### How To Create A setup File:
Creating a setup script for a Python project involves using setuptools, a package that helps to package, distribute, and install Python projects. Here's a step-by-step guide to creating a setup script:

1. **Install setuptools:**
   If you haven't already installed setuptools, you can install it using pip:
   ```
   pip install setuptools
   ```

2. **Create a `setup.py` file:**
   In your project directory, create a file named `setup.py`. This file will contain the metadata and instructions for building and distributing your project.

3. **Write the setup script:**
   Open `setup.py` in a text editor and write the setup script. Here's a basic example:

   ```python
   from setuptools import setup, find_packages

   setup(
       name='your_project_name',
       version='1.0.0',
       packages=find_packages(),
       install_requires=[
           'dependency1',
           'dependency2',
           # Add more dependencies as needed
       ],
       entry_points={
           'console_scripts': [
               'your_script_name = your_package.module:main_function',
           ]
       },
       # Metadata
       author='Your Name',
       author_email='your@email.com',
       description='Description of your project',
       url='https://github.com/yourusername/your_project',
       license='MIT',
   )
   ```

   Replace placeholders like `your_project_name`, `dependency1`, `dependency2`, `Your Name`, `your@email.com`, `Description of your project`, `https://github.com/yourusername/your_project` with actual values relevant to your project.

4. **Understand the parameters:**
   - `name`: The name of your project.
   - `version`: The version of your project.
   - `packages`: A list of Python packages to include in the distribution.
   - `install_requires`: A list of dependencies required by your project.
   - `entry_points`: Specify any console scripts or entry points.
   - `author`, `author_email`, `description`, `url`, `license`: Metadata about your project.

5. **Add project files:**
   Make sure that all project files and directories are organized properly within your project directory.

6. **Build the distribution package:**
   Open a terminal or command prompt, navigate to your project directory, and run the following command to build the distribution package:
   ```
   python setup.py sdist bdist_wheel
   ```

   This command will create a `dist` directory containing the distribution package files.

7. **Distribute your package:**
   You can distribute your package by uploading it to PyPI (Python Package Index) or by sharing the distribution package files directly. If you plan to upload to PyPI, you may need to register an account and follow the PyPI documentation for uploading packages.

8. **Optional: Test the distribution package:**
   Before distributing your package, you may want to test it locally by installing it in a virtual environment:
   ```
   pip install dist/your_project_name-1.0.0.tar.gz
   ```

   Replace `your_project_name-1.0.0.tar.gz` with the actual name of your distribution package file.

By following these steps, you can create a setup script for your Python project and package it for distribution. This allows users to easily install and use your project using tools like pip.
from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'henry_model_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf') + glob('urdf/*.xacro') + glob('urdf/*.gazebo')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name, package_name, 'henry_interface_api'), glob('henry_interface_api/*.py') + glob('henry_interface_api/*.png')),
    ],
    install_requires=['setuptools', 'pillow', 'openai'],
    zip_safe=True,
    maintainer='cass',
    maintainer_email='cass@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'start_hri = henry_model_pkg.henry_interface_api.HRI_api:main'
        ],
    },
)

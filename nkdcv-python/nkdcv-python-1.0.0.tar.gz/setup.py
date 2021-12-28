from distutils.core import setup

setup(
    name='nkdcv-python',
    packages=['nkdcv'],
    version='1.0.0',
    license='MIT',
    description='This is a Computer Vision package that makes its easy to run Image processing and AI functions.',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    url='https://github.com/khanhduy1407/nkdcv-python',
    keywords=['ComputerVision', 'HandTracking', 'FaceTracking', 'PoseEstimation'],
    install_requires=[
        'opencv-python',
        'mediapipe',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

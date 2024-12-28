**Sample data can be found in /data/smallerData**

### Code Overview
The core functionality includes:
1. Loading and preprocessing DICOM files.
2. Feature detection using Shi-Tomasi corner detection
3. Optical flow computation using the Lucas-Kanade method
4. Parallelization to speed up execution
5. Visualization of the motion analysis as animated GIFs


#### Install libraries:
    $ pip install pydicom
    $ pip install pydicom matplotlib
    $ pip install opencv-python-headless numpy

### Files:
- notebook/final.py: contains the code in notebook format (not parallelized)
- src/optical_flow.py: sequential optical flow program
- src/parallel_optical_flow.py: parallel optical flow program
- src/benchmark.py: benchmarking for all performances
- data/smallerData.zip: uzip this to run

### Usage:

#### Independent Runs:
**Sequential:**

\$ python src/optical_flow.py data/smallerData

**Parallel:**

\$ python src/parallel_optical_flow.py data/smallerData

**Run All (Benchmarking)**

\$ python src/benchmark.py data/smallerData



### Code References:

Motion Estimation with Optical Flow:
	- https://nanonets.com/blog/optical-flow/

Optical Flow in OpenCV:
    - https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html

Feature Detection Using Shi-Tomasi Corner Detection:
    - https://docs.opencv.org/4.x/d4/d8c/tutorial_py_shi_tomasi.html

Feature Detection Implementation:
    - https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga1d6bb77486c8f92d79c8793ad995d541

<p align="center">
  <img src="images/monkey.png" alt="Logo" />
</p>

**Gribber Status:**

Gribber hasn't been extensively tested and hasn't been tested since 2023. However, it does work. I may need to make some changes to improve usability.

Perhaps, in the future, it could be developed into a Python package!

Gribber is actively being developed! Please contribute if you want to help improve Gribber!!!

**Gribber Overview:**

Gribber utilizes [Herbie](https://github.com/blaylockbk/Herbie) to automate the download and extraction of meteorological model data. The process involves two main steps:

1. **Downloading Data:**
   - Gribber uses Herbie to fetch meteorological model data from online sources.
   - It downloads data for specific model levels and variables that are of interest.

2. **Extracting Data:**
   - After downloading, Gribber can processes the data to extract the relevant information.
   - It focuses on the specific model levels and variables you are interested in, making the data ready for analysis.

**How to run Gribber:**

1. First we need to install the required packages. Sometimes it is difficult to install these packages, especially on Windows.

   Right now, the easiest way to install all the required packages and dependencies is with Conda from conda-forge.

   This command will install herbie-data and eccodes (the hardest packages to install): 
   `conda install -c conda-forge herbie-data`

   Both herbie-data and eccodes are absolutely essential and there is no path forward without these packages.
An optional package is wgrib2. This package is not currently used by Gribber, but I would like it to be used in the future.
This package might be very difficult to install on Windows.
2. Now that the packages are installed, run the program from the main.py file. Don't worry about updating the code now.
We will do that later. After running the program, execution will likely fail as expected. However, this step generates the
default config.toml file. On Windows, it will be here: C:\Users\<YourUsername>\.config\herbie

   On Linux it will be in the home directory:

   ~/.config/herbie/config.toml

   You can edit this file as needed. Right now, Gribber is only designed to handle HRRR data. We really want it to be able
to handle RRFS data.
3. Now we only need to modify the code in the input file. Maybe later we can fix this, so we only need to modify the
control.txt file. We just need to change 2 variables:
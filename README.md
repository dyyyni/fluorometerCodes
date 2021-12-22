<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Project Optonome Codes</h3>

  <p align="center">
    This repository is used for the development of a water quality measuring device used in the following Tampere University project. https://projects.tuni.fi/optonome/about/
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#optonome_V1">License</a></li>
    <li><a href="#optonome_V2">License</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Hello! This repository is used for the development of a water quality measuring device used in the following Tampere University project.
https://projects.tuni.fi/optonome/about/

If you are working with the Python interface of nidaqmx or Pulsar this repository and the codes might be of use.\
nidaqmx : https://nidaqmx-python.readthedocs.io/en/latest/# \
Pulsar  : https://www.ophiropt.com/laser--measurement/software/com-object

All the best\
-Daniel


### Built With

* [Python](https://www.python.org/)

<!-- OPTONOME_V1 -->
## Optonome_V1
This is a remnant from the codes before I combined everything into optonome_V2.
Could prove useful, if you need a starting point for a new application.

<!-- OPTONOME_V2 -->

## Optonome_V2
This folder contains the modular program used to drive the application.

### Dependencies
(1) 
Make sure you have the [numpy](https://numpy.org/install/) library installed.
```
python -m pip install numpy
```
(2)
Install the [nidaqmx]https://www.ni.com/fi-fi/support/downloads/drivers/download.ni-daqmx.html#428058 drivers for the analog-to-digital converter.
(3)
Install the nidaqmx python library with
```
python -m pip install nidaqmx
```

### Use
After installing the depencies.
(1) Plug in the PMT
(2) Turn on the LED
(3) Connect the analog-to-digital converter via usb

The program should be used from the command line. Easiest way to do this is to navigate to the folder where the program files are resided and run the command:

```
python driver.py
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Daniel Luoma - [@danyluoma](https://twitter.com/danyluoma) - daniel.luoma@tuni.fi

Project Link: [https://github.com/dyyyni/fluorometerCodes](https://github.com/dyyyni/fluorometerCodes)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/dyyyni/PythonScriptsFunctions.svg?style=for-the-badge
[license-url]: https://github.com/dyyyni/PythonScriptsFunctions/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/luomadaniel

![Praetorian logo (dark)](praetorian_dark.png#gh-dark-mode-only) ![Praetorian logo (light)](praetorian_light.png#gh-light-mode-only) ![ICCS logo](iccs.png)

##

![IOP Integrated](https://img.shields.io/static/v1?logo=mongodb&label=&labelColor=black&message=IOP%20Integrated&color=47A248&style=flat-square)
![DSS Integrated](https://img.shields.io/static/v1?logo=semantic-ui-react&label=&labelColor=black&message=DSS%20Integrated&color=35BDB2&style=flat-square)

This work makes up the **backend** of the system developed by ICCS for the Task 6.4 of the Praetorian H2020 Project.

| BACKEND (Python 3)|
|:---:|
| Praetorian H2020 Project |
| Work Package 6: Response Coordination |
|Task 4: Integration with Social Media |


## Table of Contents
1. [Modules](#Modules)
1. [Usage](#Usage)
1. [Project Tree](#Project-Tree)
1. [Miscellaneous](#Miscellaneous)

## Modules

The system consists of three modules:

### Threat Detector (Social Media Security Threat Detection)

A real-time security threat detection system that monitors the entirety
of Twitter for posts that arouse suspicion regarding data breaches,
cybersecurity vulnerabilities and potential terrorist threats on the
Critical Infrastructures that pertain to the PRAETORIAN project.

### Crisis Observatory (Crisis Observation: Identification of informative social media posts during crises)

A multimodal classification technique to both image and text elements of
a tweet, in order to automatically detect those that contain valuable
information quickly and effectively.

### Post Recommendator (Recommendation of customizable social media posts targeting the public during crises)

After receiving an incident report, this module generates a prefilled social media
post based on carefully crafted templates, and offers it to the security officer,
who can then optionally edit it and post it.

## Usage

**Normal launch:**

`docker run -d --name praetorian_modules --log-driver local --network host -t uphilld/praetorian:modules`

**Print help:**

`docker run -it --name praetorian_modules --log-driver local --network host -t uphilld/praetorian:modules help`

## Project Tree

    $root
    ├ build
    │    ├ credentials.env
    │    └ models
    ├ common
    └ docs

## Miscellaneous

Shield badges provided by [Shields.io](https://shields.io/).

[⇯ Back to Top](#Table-of-Contents)
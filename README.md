# valoro-task

## High-level Description

## Design

Take it as eaxmple: 

* The system is divided into 3 separate layers, each in it's own top-level directory:
    1. Data Layer: contains the database
    1. Application Layer: contains the back-end of the system which handles access to database and stats calculation
    1. GUI Layer: contains the user interface of the system
* We decided not to make the system password protected for the following reasons:
    1. It was not specifically required from the "client"
    1. We didn't feel it's necessary, considering that nobody will actually use this system
* A relational database, sqlite, is used in the data layer. At first, we were inclined to just use a simple `csv` file to keep track of the records, but then decided that it's time to try something outside our comfort zone.
* The system is written as a `Language you used` library. The rationale behind choosing `Language you used` is obvious. And the decision to make it into a library is just a convenience for us as developers and for any potential user to facilitate the setup process.

## Installation

We assume that if you're reading this, then you already have the source code downloaded and ready. If that's not the case, request the code from one of us, or if you have access to the `github` repository, clone it as follows:
* `git clone https://github.com/geekahmed/valoro-task.git`

We recommend that you make a virtual environment to install the library in first. But this is completely optional.

1. cd to the directory containing the setup script `setup.(extension)`
1. Run `pip install .`

Make sure that `pip3` is used not `pip2`. On unix systems you can use `pip3 install .`. On windows, make sure that `python 3.x` is the one included in the system `PATH`.

## Usage

1. cd to the high-level directory of the software `/valoro-task`.
2. Run `git code to open the file on cd` to run the system.

Make sure the `language you used` is used.

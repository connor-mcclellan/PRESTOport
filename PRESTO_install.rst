Introduction
************
    
    * Leading characters in code blocks (like ``$`` or ``>``) should always be
      ignored. Never paste them (or anything before them) into a terminal.
    * Terminal commands are in ``bash``. They will start with 
      ``user@machine:~$``, or just ``$`` for short.
    * Your current working directory will always be displayed before the ``$``
      in ``bash``. Ensure you're in the right directory before running
      commands, as this is a potential cause of improper installation.
    * Unless otherwise specified, "Type X" can be interpreted to mean ''Type
      X and press enter'' for all single-line terminal commands.

Setting up packages
*******************

FFTW 3.X (From Source)
----------------------

.. note ::

    This first set of instructions is *excessively* verbose in 
    order to avoid confusion. The rest of the instructions aren't as 
    mind-numbingly specific, but are still thorough. If you experience 
    difficulty on any of the later steps, revisit this section to get a handle
    on the basics of locating download links and installing packages.


We will install FFTW from a tarball that can be downloaded from the
FFTW website.

1. Go to http://www.fftw.org/
2. Click on the Download page link at the top
3. Right click on the http download link and copy it. It should look something like 
   **http:** `fftw-3.3.8.tar.gz <http://www.fftw.org/fftw-3.3.8.tar.gz>`_ on 
   the page, and your copied link should be something like 
   http://www.fftw.org/fftw-3.3.8.tar.gz

   .. note::

       If you're installing a different FFTW version than 3.3.8, be sure to 
       replace the version numbers in all the following terminal commands 
       and path names.

4. Open a terminal window. To make sure you're in your home directory, type 
   ``cd`` and press enter
5. Use ``wget`` to download the tarball. Type:

    ::

        user@machine:~$ wget http://www.fftw.org/fftw-3.3.8.tar.gz

   .. note::

       If Step 5 above spits out something like::
            
           wget: command not found

       then ``wget`` isn't installed on your computer. It *should* come 
       pre-installed for most distributions of Linux, but if it is not, install it
       with ::
            
           user@machine:~$ sudo apt-get install wget

       This can be repeated for most other common packages that may not be 
       installed on your machine by default.

6. Unpack the tarball by typing::

    user@machine:~$ tar -xvzf fftw-3.3.8.tar.gz

7. Remove the tarball with::
    
    user@machine:~$ rm fftw-3.3.8.tar.gz

8. Move the FFTW directory to ``/usr/local/`` by typing::

    user@machine:~$ sudo mv fftw-3.3.8 /usr/local/

   You may need to enter your password to complete this action.

9. Change to the directory we just moved by typing::

    user@machine:~$ cd /usr/local/fftw-3.3.8/

10. Now we need to build FFTW. Do::

        user@machine:/usr/local/fftw-3.3.8$ ./configure --enable-float --enable-sse --enable-shared --enable-single --prefix=/usr/local && sudo make install

   .. note::

       If you don't have a C compiler installed on your system by default, you 
       will likely get this error message when trying to build FFTW::

           configure: error: no acceptable C compiler found in $PATH

       Just as before, install ``gcc`` by doing::
        
           $ sudo apt-get install gcc

       and pressing enter when prompted. After this, you should be able to run
       the command in Step 10 to configure FFTW.

   If this runs without any errors, FFTW has been successfully installed. But,
   we're not finished yet---we need to set the environment variable, so your
   system knows where to find FFTW.

11. Use your favorite text editor to open up your ``.bashrc`` file. This is 
    stored in your home directory, ``~/`` (short for ``/home/<your username>``
    ). Here, I use ``gedit`` to open this file with::

       user@machine:~$ gedit ~/.bashrc

    At the very bottom of this file, insert this text::

        export FFTW3F_DIR='/usr/local/fftw-3.3.8'

    Save and close the ``~/.bashrc`` file.


PGPLOT
------

Thankfully, we don't have to install PGPLOT from source. We will use the Ubuntu
packages.

1. Update the package lists, then install xorg-dev and gfortran::

    $ sudo apt-get update
    $ sudo apt-get install xorg-dev
    $ sudo apt-get install gfortran

   .. note ::

    To make sure our Fortran compiler installed correctly, try::
        
        $ gfortran

    in your terminal (excluding the bash ``$`` sign, of course). If you get::

        gfortran: fatal error: no input files
        compilation terminated.

    then ``gfortran`` has successfully installed.

2. Manually add the apt repository that contains pgplot5 for Ubuntu::

    $ sudo gedit /etc/apt/sources.list

   Add "multiverse" to the end of each of the lines below. The finished 
   result should contain *at least*::

    deb http://archive.ubuntu.com/ubuntu/ bionic main restricted universe multiverse
    deb http://security.ubuntu.com/ubuntu/ bionic-security main restricted universe multiverse
    deb http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted universe multiverse

   There may be a better way to do this, but it works!

2. Install pgplot5::

    $ sudo apt-get install pgplot5

3. Set environment variables for PGPLOT. Insert the following lines in the same
   ``.bashrc`` file as before, under the FFTW environment variable.

   ::

    $ gedit ~/.bashrc

   Insert these lines::

        export PGPLOT_DIR='/usr/lib/pgplot5'
        export PGPLOT_DEV='/Xserve'

   Then, source your ``.bashrc`` file to make sure the updates are loaded into
   your current terminal session.

   ::

    $ source ~/.bashrc


TEMPO
-----

TEMPO handles the pulsar timing data analysis for PRESTO. Its installation is
fairly straightforward---we just need to clone the repository from GitHub
and build it.

1. Change into some installation directory and clone the repository. I like
   to do this in the home directory, but you can really do it wherever::

    $ cd ~
    $ git clone http://git.code.sf.net/p/tempo/tempo 

   Once it clones, we can start following the installation instructions in the 
   README file.

   .. note ::

    You may need to install ``git``, if it is not already present on your 
    system. Do::

        $ sudo apt install git

    and then try again, if you get the error message "``Command 'git' not found``".

2. Change into the cloned directory. TEMPO has to use the ``csh`` shell to 
   build some of its files, and it may not be installed on our system. Install 
   it with::

    $ sudo add-apt-repository universe
    $ sudo apt-get update
    $ sudo apt-get install csh

   The first of these lines adds the repository where ``csh`` is stored, so that
   ``apt`` knows where to find it when you request an installation. The second 
   line updates ``apt``'s package list, and the third installs ``csh``.

3. We will also need ``autoconf`` to prepare the make files. Install it with

   ::

    $ sudo apt-get install autoconf


4. Now, when we run ``prepare``, our system will be able to use ``csh`` as 
   specified in the script. From the ``~/tempo`` directory, do::

    $ ./prepare
    $ ./configure
    $ sudo make
    $ sudo make install

5. Don't forget to set the TEMPO environment variable!

   ::

    $ gedit ~/.bashrc

   Insert a line under your other environment variables that points to the 
   ``~/tempo`` source directory. **IMPORTANT**: make sure to replace 
   "``<your username>``" below with your actual username!

   ::

    export TEMPO='/home/<your username>/tempo'

   .. note ::

    This variable will be different if you installed TEMPO somewhere other than 
    your home directory. Navigate to the recently installed ``tempo`` directory
    and do::

        $ pwd

    to make sure the directory that's printed matches with what you
    set as the environment variable.


GLIB
----

All we need to do here is install the Ubuntu GLIB dev package. The rest should
come default with Ubuntu.

1. Use apt-get to install the package.

   ::

    $ sudo apt-get install libglib2.0-dev

As Scott Ransom states, on Linux machines GLIB is almost certainly already on 
your system, but you can check in ``/usr/lib`` and ``/usr/include/glib*`` to 
be sure.

CFITSIO
-------

Here we install CFITSIO from source (website: https://heasarc.gsfc.nasa.gov/fitsio/)

1. Use ``wget`` to download the tarball, then unpack it. Let's place it in the 
   home directory for convenience.

   ::

    $ cd ~
    $ wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.47.tar.gz
    $ tar -zxvf cfitsio-3.47.tar.gz
    $ rm cfitsio-3.47.tar.gz

2. ``cd`` into the newly created cfitsio directory and build it.

   ::

    $ cd cfitsio-3.47
    $ ./configure --prefix=/usr/local
    $ make
    $ make install

   **IMPORTANT**: if ``configure``'s ``--prefix`` flag is not set, your system
   won't be able to find your installation of cfitsio.

3. Now add another path environment variable so your system knows where to find
   cfitsio. Again, if you installed it in a different directory than your home
   directory, make the necessary changes to the lines below.

   ::

    $ gedit ~/.bashrc

   Insert this line::

    export CFITSIO_DIR='/home/<your username>/cfitsio-3.47'

   replacing "``<your username>``" with your actual username.

PRESTO
******

Finally, we can install PRESTO. First, clone the repository to 
``/usr/local/``. You will need root privileges to do this, so use 
``sudo``.

1. Clone the repository to ``/usr/local/``.

   ::

    $ cd /usr/local/
    $ sudo git clone https://github.com/scottransom/presto.git
    $ cd presto

2. Set the PRESTO environment variables before building it. Again, edit your
   ``~/.bashrc``::

        $ gedit ~/.bashrc

   and add the following lines to the end (**NOTE:** Don't forget to replace <your username> in the second line)::

        export PRESTO='/usr/local/presto'
        export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/include:/usr/local/fftw-3.3.8:/usr/share/glib-2.0:/home/<your username>/cfitsio-3.47:/usr/local/presto/include"
        export PATH="/usr/local/presto/bin:$PATH"
        export PYTHONPATH="/usr/local/presto/lib/python"
        export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/presto/lib"

   replacing the appropriate fields with wherever your 
   package installations are located.

   .. note ::

    If the ``PATH`` and ``PYTHONPATH`` environment variables already exist, 
    simply add on to them, separating new additions with a colon. For example::

        export PATH="/home/<your username>/anaconda3/bin:$PATH"

    becomes::

        export PATH="/home/<user>/anaconda3/bin:/usr/local/presto/bin:$PATH"

   Likewise, if you install PRESTO *before* installing Anaconda Python or 
   similar, you will need to add the Python environment variables to the 
   existing PATH and PYTHONPATH in order for your Python installation to work.

3. For some reason, even after setting the environment variables, the Makefile 
   can have trouble setting its PRESTO and PGPLOT paths. A temporary patch for 
   this is to add the PRESTO and PGPLOT paths to the Makefile manually. Open up
   the Makefile::

    $ cd /usr/local/presto/src
    $ sudo gedit Makefile

   Right above ``PRESTOLINK``, insert this line::

    PRESTO = /usr/local/presto

   And, right above ``PGPLOTLINK``, insert this line::

    PGPLOT_DIR = /usr/lib/pgplot5

4. After the fix in the previous step, we can run ``make makewisdom`` to get
   FFTW "acquainted" with our machine. We'll need super user privileges for 
   this.

   ::

    $ sudo make makewisdom

   With this, a very long computational process will begin as FFTW pokes around
   and does its thing.

5. Type::

    $ sudo make prep

   The terminal should return ``touch *_cmd.c`` with no errors, if all the
   previous steps have been done properly.

6. Make sure all the ``-dev`` packages are installed---we will need them in the
   next step.

   ::

    $ sudo apt-get install libcfitsio-dev
    $ sudo apt-get install libfftw3-dev
    $ sudo apt-get install libpng-dev

7. Build PRESTO::

    $ sudo make

8. Try this::

    $ exploredat

   If you get something like::

    usage:  exploredat datafilename

   then PRESTO has been installed successfully!


PRESTOport
----------

This analysis tool is used to format certain types of light curves for analysis
in PRESTO. We can run a simple test to make sure that PRESTO is working
properly. First, we clone PRESTOport.

1. Clone PRESTOport::

    $ git clone https://github.com/mccbc/PRESTOport.git

2. cd into the PRESTOport main directory and run ``example.py``. This script 
   contains a lot of documentation about how to use PRESTOport, so it's 
   highly recommended to look through it to understand how each of the commands
   are used.

    $ cd PRESTOport/
    $ python example.py

   .. note ::

        If you get any Python errors here, you may still be missing required
        packages in your Python installation. Install the packages mentioned in
        the error messages until the program runs successfully (these should be
        numpy, matplotlib, scipy, etc.)

3. Check out the example directory, where the output ``.dat`` and ``.inf`` 
   files should be generated from example light curves::

    $ cd example/
    $ ls

4. Moment of truth! Run an FFT on one of the output files::

    $ realfft 404850274.dat

5. If this runs successfully, try examining the FFT with ``explorefft``::

    $ explorefft 404850274.fft

   An interactive PGPLOT window should show up. Use the reference sheet printed
   in the terminal window to navigate around the plot and close it when you're
   finished.

6. You're done! Check out Scott Ransom's `pulsar finding tutorial <https://www.cv.nrao.edu/~sransom/PRESTO_search_tutorial.pdf>`_ for more info 
   about how to use PRESTO. 

   (A PRESTO guide for EvryScope and TESS light curves is coming
   soon. When I write it up, I'll be sure to link it here - CM, 30 Jul 2019)


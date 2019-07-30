Introduction
============

> -   Leading characters in code blocks (like `$` or `>`) should always
>     be ignored. Never paste them (or anything before them) into a
>     terminal.
> -   Terminal commands are in `bash`. They will start with
>     `user@machine:~$`, or just `$` for short.
> -   Your current working directory will always be displayed before the
>     `$` in `bash`. Ensure you're in the right directory before running
>     commands, as this is a potential cause of improper installation.
> -   Unless otherwise specified, "Type X" can be interpreted to mean
>     ''Type X and press enter'' for all single-line terminal commands.

Setting up packages
===================

FFTW 3.X
--------

FFTW can be installed using `apt-get` in Ubuntu, but this wouldn't give
us control over the path to which it installs, nor the config flags used
when building. So, we will install it from a tarball that can be
downloaded from the FFTW website.

1.  Go to <http://www.fftw.org/>
2.  Click on the Download page link at the top
3.  Right click on the http download link and copy it. It should look
    something like \*\*<http:**>
    [fftw-3.3.8.tar.gz](http://www.fftw.org/fftw-3.3.8.tar.gz) on the
    page, and your copied link should be something like
    <http://www.fftw.org/fftw-3.3.8.tar.gz>

    <div class="admonition note">

    If you're installing a different FFTW version than 3.3.8, be sure to
    replace the version numbers in all the following terminal commands
    and path names.

    </div>

4.  Open a terminal window. To make sure you're in your home directory,
    type `cd` and press enter
5.  Use `wget` to download the tarball. Type:

    >     user@machine:~$ wget http://www.fftw.org/fftw-3.3.8.tar.gz

<div class="admonition note">

If Step 5 above spits out something like:

    wget: command not found

then `wget` isn't installed on your computer. It *should* come
pre-installed for most distributions of Linux, but if it is not, install
it with :

    user@machine:~$ sudo apt-get install wget

This can be repeated for most other common packages that may not be
installed on your machine by default.

</div>

6.  Unpack the tarball by typing:

        user@machine:~$ tar -xvzf fftw-3.3.8.tar.gz

7.  Remove the tarball with:

        user@machine:~$ rm fftw-3.3.8.tar.gz

8.  Move the FFTW directory to `/usr/local/` by typing:

        user@machine:~$ sudo mv fftw-3.3.8 /usr/local/

    You may need to enter your password to complete this action.

9.  Change to the directory we just moved by typing:

        user@machine:~$ cd /usr/local/fftw-3.3.8/

10. Now we need to build FFTW. Do:

        user@machine:/usr/local/fftw-3.3.8$ ./configure --enable-float --enable-sse --enable-shared --enable-single --prefix=/usr/local && sudo make install

<div class="admonition note">

If you don't have a C compiler installed on your system by default, you
will likely get this error message when trying to build FFTW:

    configure: error: no acceptable C compiler found in $PATH

Just as before, install `gcc` by doing:

    $ sudo apt-get install gcc

and pressing enter when prompted. After this, you should be able to run
the command in Step 10 to configure FFTW.

</div>

If Step 10 runs without any errors, FFTW has been successfully
installed. But, we're not finished yet---we need to set the environment
variable, so your system knows where to find FFTW.

11. Use your favorite text editor to open up your `.bashrc` file. This
    is stored in your home directory, `~/` (short for
    `/home/<your username>` ). Edit this file with:

        user@machine:~$ gedit ~/.bashrc

    At the very bottom of this file, insert this text:

        export FFTW3F_DIR='/usr/local/fftw-3.3.8'

    Save and close the `~/.bashrc` file.

PGPLOT
------

Generally, these steps will follow the instructions found
[here](https://guaix.fis.ucm.es/~ncl/howto/howto-pgplot). We will be
installing PGPLOT from source, so first we need to make sure we have a
Fortran compiler and X11 (both required to compile pgplot).

1.  Update the package lists, then install xorg-dev and gfortran:

        $ sudo apt-get update
        $ sudo apt-get install xorg-dev
        $ sudo apt-get install gfortran

<!-- -->

2.  Download the PGPLOT tarball, found here:
    [pgplot5.2.tar.gz](ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot5.2.tar.gz)

        $ cd ~
        $ wget ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot5.2.tar.gz
        $ cd /usr/local/src
        $ sudo mv ~/pgplot5.2.tar.gz ./
        $ sudo tar -zxvf pgplot5.2.tar.gz
        $ sudo rm pgplot5.2.tar.gz

3.  Now that we've downloaded, extracted, and then removed the tarball,
    we can actually build PGPLOT. However, we're going to make a
    different directory in which to build it.

        $ sudo mkdir /usr/local/pgplot
        $ cd /usr/local/pgplot

4.  Copy the list of drivers from the downloaded directory to our
    installation directory, and edit it to remove the exclamation marks
    in front of the lines that contain /PS, /VPS, /CPS, /VCPS, and
    /XServe. These identifiers can be found under the "Code" column.

        $ sudo cp /usr/local/src/pgplot/drivers.list .
        $ sudo gedit drivers.list

    Then uncomment the lines for /PS, /VPS, /CPS, /VCPS, and /XServe.

5.  Now, we can create the makefile. Change directories to the
    installation directory (`/usr/local/pgplot`) and tell the source to
    build the necessary files.

        $ cd /usr/local/pgplot
        $ sudo /usr/local/src/pgplot/makemake /usr/local/src/pgplot linux g77_gcc_aout
        $ ls

    You should see a newly created `makefile` in the current directory,
    along some other files. We need to edit the `makefile` to make sure
    it uses the compiler we want it to when building: gfortran.

6.  Edit the makefile so that the default Fortran compiler is set to
    gfortran.

        $ sudo gedit makefile

    and change the line

        FCOMPL=g77

    to

        FCOMPL=gfortran

7.  Compile the source files.

        $ sudo make
        $ sudo make cpg
        $ sudo make clean
        $ ls

    Now you should see a bunch of PGPLOT demo files, if all went well.
    We still need to set the environment variables so your system knows
    where to find PGPLOT.

8.  Set environment variables for PGPLOT. Add the following lines to the
    same `.bashrc` file as before, under the FFTW environment variable.

        $ gedit ~/.bashrc

    And add these lines:

        export PGPLOT_DIR='/usr/local/pgplot'
        export PGPLOT_DEV='/Xserve'

    Then, source your `.bashrc` file to make sure the updates are loaded
    into your current terminal session.

        $ source ~/.bashrc

9.  To ensure PGPLOT is working properly, we can run one of the demos.
    Run this command from any directory in your machine:

        $ /usr/local/pgplot/pgdemo1

    and you should see a lovely `y = x^2` graph. Click back into your
    terminal and press `<RETURN>` to cycle through all the pages. When
    you're done, you can close out of the tiny "PGPLOT Server" window
    that shows up whenever you run PGPLOT.

TEMPO
-----

TEMPO handles the pulsar timing data analysis for PRESTO. Its
installation is fairly straightforward---we just need to clone the
repository from GitHub and build it.

1.  Change into some installation directory and clone the repository. I
    like to do this in the home directory, but you can really do it
    wherever:

        $ cd ~
        $ git clone http://git.code.sf.net/p/tempo/tempo 

    Once it clones, we can start following the installation instructions
    in the README file.

<!-- -->

2.  Change into the cloned directory. TEMPO has to use the `csh` shell
    to build some of its files, and it may not be installed on our
    system. Install it with:

        $ sudo add-apt-repository universe
        $ sudo apt-get update
        $ sudo apt-get install csh

    The first of these lines adds the repository where `csh` is stored,
    so that `apt` knows where to find it when you request an
    installation. The second line updates `apt`'s package list, and the
    third installs `csh`.

3.  We will also need `autoconf` to prepare the make files. Install it
    with

        $ sudo apt-get install autoconf

4.  Now, when we run `prepare`, our system will be able to use `csh` as
    specified in the script. From the `~/tempo` directory, do:

        $ ./prepare
        $ ./configure
        $ sudo make
        $ sudo make install

5.  Don't forget to set the TEMPO environment variable!

        $ gedit ~/.bashrc

    Insert a line under your other environment variables that points to
    the `~/tempo` source directory. **IMPORTANT**: make sure to replace
    "`<your username>`" below with your actual username!

        export TEMPO='/home/<your username>/tempo'

GLIB
----

All we need to do here is install the Ubuntu GLIB dev package. The rest
should come default with Ubuntu.

1.  Use apt-get to install the package.

        $ sudo apt-get install libglib2.0-dev

As Scott Ransom states, on Linux machines GLIB is almost certainly
already on your system, but you can check in `/usr/lib` and
`/usr/include/glib*` to be sure.

CFITSIO
-------

Here we install CFITSIO from source (website:
<https://heasarc.gsfc.nasa.gov/fitsio/>)

1.  Use `wget` to download the tarball, then unpack it. Let's place it
    in the home directory for convenience.

        $ cd ~
        $ wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.47.tar.gz
        $ tar -zxvf cfitsio-3.47.tar.gz
        $ rm cfitsio-3.47.tar.gz

2.  `cd` into the newly created cfitsio directory and build it.

        $ cd cfitsio-3.47
        $ ./configure --prefix=/usr/local
        $ make
        $ make install

    **IMPORTANT**: if `configure`'s `--prefix` flag is not set, your
    system won't be able to find your installation of cfitsio.

3.  Now add another path environment variable so your system knows where
    to find cfitsio. Again, if you installed it in a different directory
    than your home directory, make the necessary changes to the lines
    below.

        $ gedit ~/.bashrc

    and add this line:

        export CFITSIO_DIR='/home/<your username>/cfitsio-3.47'

    replacing "`<your username>`" with your actual username.

PRESTO
======

Finally, we can install PRESTO. First, clone the repository to
`/usr/local/`. You will need root privileges to do this, so use `sudo`.

1.  Clone the repository to `/usr/local/`.

        $ cd /usr/local/
        $ sudo git clone https://github.com/scottransom/presto.git
        $ cd presto

2.  Set the PRESTO environment variables before building it. Again, edit
    your `~/.bashrc`:

        $ gedit ~/.bashrc

    and add the following line to the end:

        export PRESTO='/usr/local/presto'
        export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/include:/usr/local/fftw-3.3.8:/usr/share/glib-2.0:/home/<your username>/cfitsio-3.47:/usr/local/presto/include"
        export PATH="/usr/local/presto/bin:$PATH"
        export PYTHONPATH="/usr/local/presto/lib/python"
        export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/presto/lib"

    replacing the appropriate fields in the second line with wherever
    your package installations are located.

<!-- -->

3.  For some reason, even after setting the environment variables, the
    Makefile can have trouble setting its PRESTO path. A temporary patch
    for this is to add the PRESTO and PGPLOT paths to the Makefile
    manually. Open up the Makefile:

        $ cd /usr/local/presto/src
        $ sudo gedit Makefile

    Right above `PRESTOLINK`, insert this line:

        PRESTO = /usr/local/presto

    And, right above `PGPLOTLINK`, insert this line:

        PGPLOT_DIR = /usr/local/pgplot

4.  After the fix in the previous step, we can run `make makewisdom` to
    get FFTW "acquainted" with our machine. We'll need super user
    privileges for this.

        $ sudo make makewisdom

    With this, a very long computational process will begin as FFTW
    pokes around and does its thing.

5.  Type:

        $ sudo make prep

    The terminal should return `touch *_cmd.c` with no errors, if all
    the previous steps have been done properly.

6.  Make sure all the `-dev` packages are installed---we will need them
    in the next step.

        $ sudo apt-get install libcfitsio-dev
        $ sudo apt-get install libfftw3-dev
        $ sudo apt-get install libpng-dev

7.  Build PRESTO:

        $ sudo make

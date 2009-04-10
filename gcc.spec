%define DATE 20090409
%define SVNREV 145816
%define gcc_version 4.4.0
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%define gcc_release 0.33
%define _unpackaged_files_terminate_build 0
%define multilib_64_archs sparc64 ppc64 s390x x86_64
%define include_gappletviewer 1
%ifarch %{ix86} x86_64 ia64 ppc ppc64 alpha
%define build_ada 1
%else
%define build_ada 0
%endif
%define build_java 1
%ifarch %{sparc}
%define build_cloog 0
%else
%define build_cloog 1
%endif
# If you don't have already a usable gcc-java and libgcj for your arch,
# do on some arch which has it rpmbuild -bc --with java_tar gcc41.spec
# which creates libjava-classes-%{version}-%{release}.tar.bz2
# With this then on the new arch do rpmbuild -ba -v --with java_bootstrap gcc41.spec
%define bootstrap_java %{?_with_java_bootstrap:%{build_java}}%{!?_with_java_bootstrap:0}
%define build_java_tar %{?_with_java_tar:%{build_java}}%{!?_with_java_tar:0}
%ifarch s390x
%define multilib_32_arch s390
%endif
%ifarch sparc64
%define multilib_32_arch sparcv9
%endif
%ifarch ppc64
%define multilib_32_arch ppc
%endif
%ifarch x86_64
%define multilib_32_arch i586
%endif

# java-1.5.0-gcj-compat related definitions

# convert an absolute path to a relative path.  each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%define abs2rel %{__perl} -e 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'

# python install location
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib().replace('%{_prefix}','',1)")}

# Java version information and alternatives priority
%define javaver         1.5.0
%define javabuildver    0
%define javadirname     java-%{javaver}-gcj-%{javaver}.%{javabuildver}
%define origin          gcj
%define priority        1500

# installation directory names corresponding to JPackage specifications
%define sdklnk          java-%{javaver}-%{origin}
%define jrelnk          jre-%{javaver}-%{origin}
%define sdkdir          java-%{javaver}-gcj-%{javaver}.%{javabuildver}
%define jredir          %{sdkdir}/jre
%define sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%define jrebindir       %{_jvmdir}/%{jrelnk}/bin
%define jvmjardir       %{_jvmjardir}/java-%{javaver}-gcj-%{javaver}.%{javabuildver}

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}
# libgcc, libgfortran, libmudflap and crtstuff have an exception which allows
# linking it into any kind of programs or shared libraries without
# restrictions.
License: GPLv3+ and GPLv2+ with exceptions
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_4-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: libgcc_post_upgrade.c
Source2: README.libgcjwebplugin.so
Source3: protoize.1
%define fastjar_ver 0.97
Source4: http://download.savannah.nongnu.org/releases/fastjar/fastjar-%{fastjar_ver}.tar.gz
Source5: generate-cacerts.pl
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
BuildRequires: binutils >= 2.17.50.0.17-3
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
%if %{build_java}
BuildRequires: /usr/share/java/eclipse-ecj.jar, zip, unzip
%if %{bootstrap_java}
Source10: libjava-classes-%{version}-%{release}.tar.bz2
%else
BuildRequires: gcc-java, libgcj
%endif
%endif
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.72
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_cloog}
BuildRequires: ppl >= 0.10, ppl-devel >= 0.10, cloog-ppl >= 0.15, cloog-ppl-devel >= 0.15
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
Requires: binutils >= 2.17.50.0.17-3
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
Obsoletes: libgnat < %{version}-%{release}
%endif
%if %{build_cloog}
Requires: cloog-ppl >= 0.15
%endif
Prereq: /sbin/install-info
AutoReq: true

Patch0: gcc44-hack.patch
Patch1: gcc44-build-id.patch
Patch2: gcc44-c++-builtin-redecl.patch
Patch3: gcc44-ia64-libunwind.patch
Patch4: gcc44-java-nomulti.patch
Patch5: gcc44-ppc32-retaddr.patch
Patch9: gcc44-pr33763.patch
Patch10: gcc44-rh330771.patch
Patch11: gcc44-rh341221.patch
Patch12: gcc44-java-debug-iface-type.patch
Patch13: gcc44-i386-libgomp.patch
Patch15: gcc44-sparc-config-detection.patch
Patch16: gcc44-libgomp-omp_h-multilib.patch
Patch20: gcc44-libtool-no-rpath.patch
Patch21: gcc44-cloog-dl.patch
Patch22: gcc44-raw-string.patch
Patch24: gcc44-atom.patch
Patch26: gcc44-power7.patch
Patch27: gcc44-power7-2.patch
Patch28: gcc44-pr38757.patch
Patch30: gcc44-pr39543.patch
Patch31: gcc44-libjava-i386.patch

Patch1000: fastjar-0.97-segfault.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%define _gnu %{nil}
%endif
%ifarch sparcv9
%define gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc
%define gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc
%define gcc_target_platform %{_target_platform}
%endif

%description
The gcc package contains the GNU Compiler Collection version 4.4.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.4 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Autoreq: true

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++ = %{version}-%{release}, %{_prefix}/%{_lib}/libstdc++.so.6
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1
Prereq: /sbin/install-info
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgomp
Summary: GCC OpenMP v3.0 shared support library
Group: System Environment/Libraries
Prereq: /sbin/install-info

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libmudflap
Summary: GCC mudflap shared support library
Group: System Environment/Libraries

%description -n libmudflap
This package contains GCC shared support library which is needed
for mudflap support.

%package -n libmudflap-devel
Summary: GCC mudflap support
Group: Development/Libraries
Requires: libmudflap = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libmudflap-devel
This package contains headers and static libraries for building
mudflap-instrumented programs.

To instrument a non-threaded program, add -fmudflap
option to GCC and when linking add -lmudflap, for threaded programs
also add -fmudflapth and -lmudflapth.

%package java
Summary: Java support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgcj = %{version}-%{release}
Requires: libgcj-devel = %{version}-%{release}
Requires: /usr/share/java/eclipse-ecj.jar
Prereq: /sbin/install-info
Autoreq: true

%description java
This package adds support for compiling Java(tm) programs and
bytecode into native code.

%package -n libgcj
Summary: Java runtime library for gcc
Group: System Environment/Libraries
Prereq: /sbin/install-info
Requires: zip >= 2.1
Requires: gtk2 >= 2.4.0
Requires: glib2 >= 2.4.0
Requires: libart_lgpl >= 2.1.0
%if %{build_java}
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: glib2-devel >= 2.4.0
BuildRequires: xulrunner-devel
BuildRequires: libart_lgpl-devel >= 2.1.0
BuildRequires: alsa-lib-devel
BuildRequires: libXtst-devel
BuildRequires: libXt-devel
%endif
Autoreq: true

%description -n libgcj
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%package -n libgcj-devel
Summary: Libraries for Java development using GCC
Group: Development/Languages
Requires: libgcj = %{version}-%{release}, %{_prefix}/%{_lib}/libgcj.so.10
Requires: zlib-devel, %{_prefix}/%{_lib}/libz.so
Requires: /bin/awk
Autoreq: false
Autoprov: false

%description -n libgcj-devel
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%package -n libgcj-src
Summary: Java library sources from GCC4 preview
Group: System Environment/Libraries
Requires: libgcj = %{version}-%{release}
Autoreq: true

%description -n libgcj-src
The Java(tm) runtime library sources for use in Eclipse.

%package -n java-%{javaver}-gcj
Summary: JPackage runtime compatibility layer for GCJ
Group:   Development/Languages

BuildRequires: gcc-java >= %{version}
BuildRequires: libgcj-src >= %{version}
# required for cacerts generation
BuildRequires: openssl
BuildRequires: python-devel
%if ! %{bootstrap_java}
# required for javadoc
BuildRequires: java-1.6.0-openjdk-devel
%endif
BuildRequires: unzip

# required for tools and libgcj.jar
Requires:         libgcj = %{version}
# required for directory structures
Requires:         jpackage-utils >= 1.7.3
# required for java.security symlink
Requires:         %{_prefix}/%{_lib}/security/classpath.security
%if ! %{bootstrap_java}
# required for javadoc symlink
Requires:         sinjdoc
%endif
# post requires alternatives to install tool alternatives
Requires(post):   %{_sbindir}/alternatives
# post requires gij to retrieve gcc version
Requires(post):   %{_bindir}/gij
# post rebuilds the gcj database
Requires(post):   %{_bindir}/rebuild-gcj-db
# rebuild-gcj-db requires gcj-dbtool
Requires(post):   %{_bindir}/gcj-dbtool
# rebuild-gcj-db requires findutils
Requires(post):   findutils
# postun requires alternatives to uninstall tool alternatives
Requires(postun): %{_sbindir}/alternatives
# postun requires gij to retrieve gcc version
Requires(postun): %{_bindir}/gij
# postun rebuilds the gcj database
Requires(postun): %{_bindir}/rebuild-gcj-db
# rebuild-gcj-db requires gcj-dbtool
Requires(postun): %{_bindir}/gcj-dbtool
# rebuild-gcj-db requires findutils
Requires(postun): findutils

# standard JPackage base provides
Provides: jre-%{javaver}-%{origin} = %{version}-%{release}
Provides: jre-%{origin} = %{version}-%{release}
Provides: jre-%{javaver} = %{version}-%{release}
Provides: java-%{javaver} = %{version}-%{release}
Provides: jre = %{javaver}
Provides: java-%{origin} = %{version}-%{release}
Provides: java = %{javaver}
# libgcj provides, translated to JPackage provides
Provides: jaas = %{version}-%{release}
Provides: jce = %{version}-%{release}
Provides: jdbc-stdext = %{version}-%{release}
Provides: jdbc-stdext = 3.0
Provides: jndi = %{version}-%{release}
Provides: jndi-cos = %{version}-%{release}
Provides: jndi-dns = %{version}-%{release}
Provides: jndi-ldap = %{version}-%{release}
Provides: jndi-rmi = %{version}-%{release}
Provides: jsse = %{version}-%{release}
Provides: java-sasl = %{version}-%{release}
Provides: jaxp_parser_impl = %{version}-%{release}
# java-gcj-compat base provides
Provides: java-gcj-compat = 1.0.79
Provides: java-1.4.2-gcj-compat > 1.4.2.0-40jpp.111

Obsoletes: java-1.4.2-gcj-compat <= 1.4.2.0-40jpp.111
Obsoletes: gnu-crypto <= 2.1.0-2jpp.1
Obsoletes: gnu-crypto-sasl-jdk1.4 <= 2.1.0-2jpp.1
Obsoletes: jessie <= 1.0.1-7

%description -n java-%{javaver}-gcj
This package installs directory structures, shell scripts and symbolic
links to simulate a JPackage-compatible runtime environment with GCJ.

%package -n java-%{javaver}-gcj-devel
Summary: JPackage development compatibility layer for GCJ
Group:   Development/Tools

# require libgcj-src for tools.jar symlink
Requires:         libgcj-src = %{version}
# require base package
Requires:         java-%{javaver}-gcj = %{version}-%{release}
# require ecj for ecj binary
Requires:         ecj >= 3.2.1
# require python for aot-compile
Requires:         python
# require gcc-java for gjavah binary
Requires:         gcc-java = %{version}
# post requires alternatives to install tool alternatives
Requires(post):   %{_sbindir}/alternatives
# post requires gcj to retrieve gcj header file locations
Requires(post):   %{_bindir}/gcj
# postun requires alternatives to uninstall tool alternatives
Requires(postun): %{_sbindir}/alternatives

# standard JPackage devel provides
Provides: java-sdk-%{javaver}-%{origin} = %{version}
Provides: java-sdk-%{javaver} = %{version}
Provides: java-sdk-%{origin} = %{version}
Provides: java-sdk = %{javaver}
Provides: java-%{javaver}-devel = %{version}
Provides: java-devel-%{origin} = %{version}
Provides: java-devel = %{javaver}
# java-gcj-compat devel provides
Provides: java-gcj-compat-devel = 1.0.79
Provides: java-1.4.2-gcj-compat-devel > 1.4.2.0-40jpp.111

Obsoletes: java-1.4.2-gcj-compat-devel <= 1.4.2.0-40jpp.111

%description -n java-%{javaver}-gcj-devel
This package installs directory structures, shell scripts and symbolic
links to simulate a JPackage-compatible development environment with
GCJ.

%package -n java-%{javaver}-gcj-src
Summary: Source files for libgcj
Group:   Development/Libraries

Requires:       java-%{javaver}-gcj = %{version}-%{release}
Requires:       libgcj-src = %{version}
# post requires gij to retrieve gcc version
Requires(post): %{_bindir}/gij

# java-gcj-compat src provides
Provides: java-1.4.2-gcj-compat-src > 1.4.2.0-40jpp.111

Obsoletes: java-1.4.2-gcj-compat-src <= 1.4.2.0-40jpp.111

%description -n java-%{javaver}-gcj-src
This package installs a src.zip symbolic link that points to a
specific version of the libgcj sources.

%if ! %{bootstrap_java}
%package -n java-%{javaver}-gcj-javadoc
Summary: API documentation for libgcj
Group:   Documentation

# require base package
Requires: java-%{javaver}-gcj = %{version}-%{release}

# standard JPackage javadoc provides
Provides: java-javadoc = %{version}-%{release}
Provides: java-%{javaver}-javadoc = %{version}-%{release}
# java-gcj-compat javadoc provides
Provides: java-1.4.2-gcj-compat-javadoc > 1.4.2.0-40jpp.111

Obsoletes: java-1.4.2-gcj-compat-javadoc <= 1.4.2.0-40jpp.111
Obsoletes: gnu-crypto-javadoc <= 2.1.0-2jpp.1

%description -n java-%{javaver}-gcj-javadoc
This package installs Javadoc API documentation for libgcj.
%endif

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Prereq: /sbin/install-info
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 95 support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Prereq: /sbin/install-info
Autoreq: true

%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development tools,
the documents and Ada 95 compiler.

%package -n libgnat
Summary: GNU Ada 95 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared libraries,
which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 95 libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat-devel
GNAT is a GNU Ada 95 front-end to GCC. This package includes libraries,
which are required to compile with the GNAT.

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch0 -p0 -b .hack~
%patch1 -p0 -b .build-id~
%patch2 -p0 -b .c++-builtin-redecl~
%patch3 -p0 -b .ia64-libunwind~
%patch4 -p0 -b .java-nomulti~
%patch5 -p0 -b .ppc32-retaddr~
%patch9 -p0 -b .pr33763~
%patch10 -p0 -b .rh330771~
%patch11 -p0 -b .rh341221~
%patch12 -p0 -b .java-debug-iface-type~
%patch13 -p0 -b .i386-libgomp~
%patch15 -p0 -b .sparc-config-detection~
%patch16 -p0 -b .libgomp-omp_h-multilib~
%patch20 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch21 -p0 -b .cloog-dl~
%endif
%patch22 -p0 -b .raw-string~
%patch24 -p0 -b .atom~
%patch26 -p0 -b .power7~
%patch27 -p0 -b .power7-2~
%patch28 -p0 -b .pr38757~
#%patch30 -p0 -b .pr39543~
%patch31 -p0 -b .libjava-i386~

# This testcase doesn't compile.
rm libjava/testsuite/libjava.lang/PR35020*

tar xzf %{SOURCE4}

%patch1000 -p0 -b .fastjar-0.97-segfault~

%if %{bootstrap_java}
tar xjf %{SOURCE10}
%endif

sed -i -e 's/4\.4\.1/4.4.0/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

%build

%if %{build_java}
# gjar isn't usable, so even when GCC source tree no longer includes
# fastjar, build it anyway.
mkdir fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
cd fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
../configure CFLAGS="$RPM_OPT_FLAGS" --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir}
make %{?_smp_mflags}
export PATH=`pwd`${PATH:+:$PATH}
cd ../../
%endif

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_java}
%if !%{bootstrap_java}
# If we don't have gjavah in $PATH, try to build it with the old gij
mkdir java_hacks
cd java_hacks
cp -a ../../libjava/classpath/tools/external external
mkdir -p gnu/classpath/tools
cp -a ../../libjava/classpath/tools/gnu/classpath/tools/{common,javah,getopt} gnu/classpath/tools/
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/common/Messages.properties gnu/classpath/tools/common
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/getopt/Messages.properties gnu/classpath/tools/getopt
cd external/asm; for i in `find . -name \*.java`; do gcj --encoding ISO-8859-1 -C $i -I.; done; cd ../..
for i in `find gnu -name \*.java`; do gcj -C $i -I. -Iexternal/asm/; done
gcj -findirect-dispatch -O2 -fmain=gnu.classpath.tools.javah.Main -I. -Iexternal/asm/ `find . -name \*.class` -o gjavah.real
cat > gjavah <<EOF
#!/bin/sh
export CLASSPATH=`pwd`${CLASSPATH:+:$CLASSPATH}
exec `pwd`/gjavah.real "\$@"
EOF
chmod +x `pwd`/gjavah
cat > ecj1 <<EOF
#!/bin/sh
exec gij -cp /usr/share/java/eclipse-ecj.jar org.eclipse.jdt.internal.compiler.batch.GCCMain "\$@"
EOF
chmod +x `pwd`/ecj1
export PATH=`pwd`${PATH:+:$PATH}
cd ..
%endif
%endif

CC=gcc
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac

CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="`echo $OPT_FLAGS | sed 's/ -Wall / /g'`" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
%if !%{build_ada}
	--enable-languages=c,c++,objc,obj-c++,java,fortran \
%else
	--enable-languages=c,c++,objc,obj-c++,java,fortran,ada \
%endif
%if !%{build_java}
	--disable-libgcj \
%else
	--enable-java-awt=gtk --disable-dssi --enable-plugin \
	--with-java-home=%{_prefix}/lib/jvm/%{javadirname}/jre \
	--enable-libgcj-multifile --enable-java-home --enable-aot-compile-rpm \
	--with-jvm-root-dir=\${prefix}/lib/jvm/%{javadirname} \
	--with-jvm-jar-dir=\${prefix}/lib/jvm-exports/%{javadirname} \
	--with-python-dir=%{python_sitelib} \
%if !%{bootstrap_java}
	--enable-java-maintainer-mode \
%endif
	--with-ecj-jar=/usr/share/java/eclipse-ecj.jar \
	--disable-libjava-multilib \
%endif
%if %{build_cloog}
	--with-ppl --with-cloog \
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
	--with-arch=i586 \
%endif
%ifarch x86_64
	--with-arch_32=i586 \
%endif
%ifarch s390 s390x
	--with-arch=z9-109 --with-tune=z10 \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

#GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
echo ====================TESTING=========================
( ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats\|ada'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/boehm-gc rpm.doc/fastjar rpm.doc/libffi rpm.doc/libjava
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}
sed -e 's,@VERSION@,%{gcc_version},' %{SOURCE2} > rpm.doc/README.libgcjwebplugin.so

for i in {gcc,gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd gcc/objc; for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
(cd boehm-gc; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar-%{fastjar_ver}; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libffi; for i in ChangeLog* README* LICENSE; do
	cp -p $i ../rpm.doc/libffi/$i.libffi
done)
(cd libjava; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
cp -p libjava/LIBGCJ_LICENSE rpm.doc/libjava/

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%if %{build_java_tar}
find libjava -name \*.h -type f | xargs grep -l '// DO NOT EDIT THIS FILE - it is machine generated' > libjava-classes.list
find libjava -name \*.class -type f >> libjava-classes.list
find libjava/testsuite -name \*.jar -type f >> libjava-classes.list
tar cf - -T libjava-classes.list | bzip2 -9 > $RPM_SOURCE_DIR/libjava-classes-%{version}-%{release}.tar.bz2
%endif

%install
rm -fr $RPM_BUILD_ROOT

perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/doc/html/api.html

cd obj-%{gcc_target_platform}

%if %{build_java}
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=$RPM_BUILD_ROOT%{_prefix} mandir=$RPM_BUILD_ROOT%{_mandir} \
  infodir=$RPM_BUILD_ROOT%{_infodir} install
%if %{build_java}
make DESTDIR=$RPM_BUILD_ROOT -C %{gcc_target_platform}/libjava install-src.zip
%endif
%if %{build_ada}
chmod 644 $RPM_BUILD_ROOT%{_infodir}/gnat*
%endif

FULLPATH=$RPM_BUILD_ROOT%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=$RPM_BUILD_ROOT%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

# fix some things
ln -sf gcc $RPM_BUILD_ROOT%{_prefix}/bin/cc
mkdir -p $RPM_BUILD_ROOT/lib
ln -sf ..%{_prefix}/bin/cpp $RPM_BUILD_ROOT/lib/cpp
ln -sf gfortran $RPM_BUILD_ROOT%{_prefix}/bin/f95
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
gzip -9 $RPM_BUILD_ROOT%{_infodir}/*.info*
ln -sf gcc $RPM_BUILD_ROOT%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > $RPM_BUILD_ROOT%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find $RPM_BUILD_ROOT%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/stdc++.h.gch dirs
# 1) there is no bits/stdc++.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf $RPM_BUILD_ROOT%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/stdc++.h.gch

%ifarch sparcv9 sparc64
ln -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target_platform}-gcc \
  $RPM_BUILD_ROOT%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64
ln -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target_platform}-gcc \
  $RPM_BUILD_ROOT%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find $RPM_BUILD_ROOT -name \*.la | xargs rm -f
%if %{build_java}
# gcj -static doesn't work properly anyway, unless using --whole-archive
# and saving 35MB is not bad.
find $RPM_BUILD_ROOT -name libgcj.a -o -name libgtkpeer.a \
		     -o -name libgjsmalsa.a -o -name libgcj-tools.a -o -name libjvm.a \
		     -o -name libgij.a -o -name libgcj_bc.a -o -name libjavamath.a \
  | xargs rm -f

mv $RPM_BUILD_ROOT%{_prefix}/lib/libgcj.spec $FULLPATH/
sed -i -e 's/lib: /&%%{static:%%eJava programs cannot be linked statically}/' \
  $FULLPATH/libgcj.spec
%endif

mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgcc_s.so.1 $RPM_BUILD_ROOT/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 $RPM_BUILD_ROOT/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 $RPM_BUILD_ROOT/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif

mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p $RPM_BUILD_ROOT%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -dD -xc /dev/null | grep __LONG_MAX__.*2147483647; then
  ln -sf POSIX_V6_ILP32_OFF32 $RPM_BUILD_ROOT%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 $RPM_BUILD_ROOT%{_prefix}/libexec/getconf/default
fi

%if %{build_java}
pushd ../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
make install DESTDIR=$RPM_BUILD_ROOT
popd

if [ "%{_lib}" != "lib" ]; then
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}/pkgconfig
  sed '/^libdir/s/lib$/%{_lib}/' $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/libgcj-*.pc \
    > $RPM_BUILD_ROOT%{_prefix}/%{_lib}/pkgconfig/`basename $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/libgcj-*.pc`
fi
%endif

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.2 libobjc.so
ln -sf ../../../libstdc++.so.6.* libstdc++.so
ln -sf ../../../libgfortran.so.3.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
ln -sf ../../../libmudflap.so.0.* libmudflap.so
ln -sf ../../../libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../libgcj.so.10.* libgcj.so
ln -sf ../../../libgcj-tools.so.10.* libgcj-tools.so
ln -sf ../../../libgij.so.10.* libgij.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.2 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.* libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.3.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
ln -sf ../../../../%{_lib}/libmudflap.so.0.* libmudflap.so
ln -sf ../../../../%{_lib}/libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../../%{_lib}/libgcj.so.10.* libgcj.so
ln -sf ../../../../%{_lib}/libgcj-tools.so.10.* libgcj-tools.so
ln -sf ../../../../%{_lib}/libgij.so.10.* libgij.so
%endif
fi
%if %{build_java}
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgcj_bc.so $FULLLPATH/
%endif
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libsupc++.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgfortran.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libobjc.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libmudflap{,th}.*a $FULLLPATH/

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-4.4.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-4.4.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-4.4.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-4.4.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-4.4.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-4.4.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-4.4.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-4.4.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
ln -sf ../../../../../lib64/libobjc.so.2 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.* | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.3.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflapth.so
%if %{build_java}
ln -sf ../`echo ../../../../lib/libgcj.so.10.* | sed s~/lib/~/lib64/~` 64/libgcj.so
ln -sf ../`echo ../../../../lib/libgcj-tools.so.10.* | sed s~/lib/~/lib64/~` 64/libgcj-tools.so
ln -sf ../`echo ../../../../lib/libgij.so.10.* | sed s~/lib/~/lib64/~` 64/libgij.so
ln -sf lib32/libgcj_bc.so libgcj_bc.so
ln -sf ../lib64/libgcj_bc.so 64/libgcj_bc.so
%endif
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libsupc++.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libgfortran.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libobjc.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libmudflap.a libmudflap.a
ln -sf ../lib64/libmudflap.a 64/libmudflap.a
ln -sf lib32/libmudflapth.a libmudflapth.a
ln -sf ../lib64/libmudflapth.a 64/libmudflapth.a
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.2 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.* | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.3.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflapth.so
%if %{build_java}
ln -sf ../`echo ../../../../lib64/libgcj.so.10.* | sed s~/../lib64/~/~` 32/libgcj.so
ln -sf ../`echo ../../../../lib64/libgcj-tools.so.10.* | sed s~/../lib64/~/~` 32/libgcj-tools.so
ln -sf ../`echo ../../../../lib64/libgij.so.10.* | sed s~/../lib64/~/~` 32/libgij.so
%endif
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libsupc++.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libgfortran.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libobjc.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libmudflap.a 32/libmudflap.a
ln -sf lib64/libmudflap.a libmudflap.a
ln -sf ../lib32/libmudflapth.a 32/libmudflapth.a
ln -sf lib64/libmudflapth.a libmudflapth.a
%if %{build_java}
ln -sf ../lib32/libgcj_bc.so 32/libgcj_bc.so
ln -sf lib64/libgcj_bc.so libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflap.a 32/libmudflap.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflapth.a 32/libmudflapth.a
%if %{build_java}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgcj_bc.so 32/libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adalib 32/adalib
%endif
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libmudflap.a -o -name libmudflapth.a \
		    -o -name libgcc.a -o -name libgcov.a \) -a -type f`
popd
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgfortran.so.3.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libmudflap{,th}.so.0.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libobjc.so.2.*

%if %{build_ada}
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > $RPM_BUILD_ROOT%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > $RPM_BUILD_ROOT%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/c?9

mkdir -p $RPM_BUILD_ROOT%{_prefix}/sbin
gcc -static -Os %{SOURCE1} -o $RPM_BUILD_ROOT%{_prefix}/sbin/libgcc_post_upgrade
strip $RPM_BUILD_ROOT%{_prefix}/sbin/libgcc_post_upgrade

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/{libffi*,libiberty.a}
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/{32,64}/libiberty.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libssp*
rm -f $RPM_BUILD_ROOT%{_prefix}/bin/gnative2ascii

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/lib*.so*
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/lib*.a
%else
%ifarch sparcv9 ppc
rm -f $RPM_BUILD_ROOT%{_prefix}/lib64/lib*.so*
rm -f $RPM_BUILD_ROOT%{_prefix}/lib64/lib*.a
%endif
%endif

%if %{build_java}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/java/gcj-endorsed \
	 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
chmod 755 $RPM_BUILD_ROOT%{_prefix}/share/java/gcj-endorsed \
	  $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version} \
	  $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
touch $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db

# versionless symbolic links
pushd $RPM_BUILD_ROOT%{_jvmdir}
   ln -s %{jredir} %{jrelnk}
   ln -s %{sdkdir} %{sdklnk}
popd
pushd $RPM_BUILD_ROOT%{_jvmjardir}
   ln -s %{sdkdir} %{jrelnk}
   ln -s %{sdkdir} %{sdklnk}
popd

# create relevant links in jre lib dir for backwards compatibility
pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib
for jarname in jaas jce jdbc-stdext jndi jndi-cos jndi-dns \
    jndi-ldap jndi-rmi jsse sasl; do
    ln -sf rt.jar $jarname.jar;
done
popd

# security directory and provider list
install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
  RELATIVE=$(%{abs2rel} %{_prefix}/%{_lib}/security \
    %{_jvmdir}/%{jredir}/lib/security)
  ln -sf $RELATIVE/classpath.security java.security
popd
# default security providers, provided by libgcj
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d
for provider in \
  1000-gnu.java.security.provider.Gnu \
  1001-gnu.javax.crypto.jce.GnuCrypto \
  1002-gnu.javax.crypto.jce.GnuSasl \
  1003-gnu.javax.net.ssl.provider.Jessie \
  1004-gnu.javax.security.auth.callback.GnuCallbacks
do
  cat > $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d/$provider << EOF
# This file's contents are ignored.  Its name, of the form
# <priority>-<provider name>, is used by post and postun scripts to
# rebuild the list of security providers in libgcj's
# classpath.security file.
EOF

done
# cacerts
%{__perl} %{SOURCE5}
install -m 644 cacerts $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security

# classmap database directory
install -dm 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj

# set up ecj link
RELATIVE=$(%{abs2rel} %{_prefix}/bin %{_jvmdir}/%{sdkdir}/bin)
ln -sf \
  $RELATIVE/ecj \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/bin/javac

# source zip
RELATIVE=$(%{abs2rel} %{_javadir} %{_jvmdir}/%{sdkdir})
ln -s \
  $RELATIVE/src-%{version}.zip \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/src.zip

#use fastjar instead of gjar
RELATIVE=$(%{abs2rel} %{_prefix}/bin %{_jvmdir}/%{sdkdir}/bin)
ln -sf \
  $RELATIVE/fastjar \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/bin/jar

# use sinjdoc if not bootstrapping
%if ! %{bootstrap_java}
ln -sf \
  $RELATIVE/sinjdoc \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/bin/javadoc
%endif

# arch dir for x86_64 should be x86_64, with amd64 being a link (to keep the 
# package backwards compatible)
%ifarch x86_64
if [ -d $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/amd64 ]; then

  mv $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/amd64 \
     $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/x86_64

  ln -s x86_64 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/amd64
fi
%endif

%if ! %{bootstrap_java}
# build and install API documentation
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/java-%{javaver}-gcj
pushd $RPM_BUILD_ROOT%{_javadocdir}
  ln -s java-%{javaver}-gcj java
popd
rm -rf docsbuild
mkdir docsbuild
pushd docsbuild
  echo ==== CHECK ZIP ====
  unzip -tq $RPM_BUILD_ROOT/usr/share/java/src-%{version}.zip || :
  echo ==== END CHECK ZIP ====
  if unzip -tq /usr/share/java/src-%{version}.zip
  then
    fastjar xvf /usr/share/java/src-%{version}.zip
    rm -rf gnu
    find ./ -name \*.java | xargs -n 1 dirname | sort | uniq \
      | sed -e "s/\.\///" | sed -e "s/\//\./" \
      | sed -e "s/\//\./" | sed -e "s/\//\./" \
      | sed -e "s/\//\./" | sed -e "s/\//\./" \
      | xargs %{_jvmdir}/java-openjdk/bin/javadoc -quiet \
      -d $RPM_BUILD_ROOT%{_javadocdir}/%{name} \
      -encoding UTF-8 -breakiterator \
      -linksource -splitindex -doctitle "GNU libgcj %{version}" \
      -windowtitle "GNU libgcj %{version} Documentation"
  else
    # Work around https://bugzilla.redhat.com/show_bug.cgi?id=404981
    touch $RPM_BUILD_ROOT%{_javadocdir}/%{name}/package-list
  fi
popd
%endif


%endif

install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man1/protoize.1
echo '.so man1/protoize.1' > $RPM_BUILD_ROOT%{_mandir}/man1/unprotoize.1
chmod 644 $RPM_BUILD_ROOT%{_mandir}/man1/unprotoize.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%post -n cpp
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :

%preun -n cpp
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%post gfortran
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :

%preun gfortran
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%post java
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :

%preun java
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%post gnat
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat_ugn_unw.info.gz || :
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :

%preun gnat
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn_unw.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p %{_prefix}/sbin/libgcc_post_upgrade

%post -n libstdc++ -p /sbin/ldconfig

%postun -n libstdc++ -p /sbin/ldconfig

%post -n libobjc -p /sbin/ldconfig

%postun -n libobjc -p /sbin/ldconfig

%post -n libgcj
/sbin/ldconfig
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :

%preun -n libgcj
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%postun -n libgcj -p /sbin/ldconfig

%post -n java-%{javaver}-gcj
alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre          jre          %{_jvmdir}/%{jrelnk} \
  --slave %{_jvmjardir}/jre       jre_exports  %{_jvmjardir}/%{jrelnk} \
  --slave %{_bindir}/keytool      keytool      %{jrebindir}/keytool \
  --slave %{_bindir}/rmiregistry  rmiregistry  %{jrebindir}/rmiregistry

alternatives \
  --install %{_jvmdir}/jre-%{origin} \
  jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{origin} \
  jre_%{origin}_exports %{_jvmjardir}/%{jrelnk}

alternatives \
  --install %{_jvmdir}/jre-%{javaver} \
  jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{javaver} \
  jre_%{javaver}_exports %{_jvmjardir}/%{jrelnk}

alternatives --install %{_javadir}/jaxp_parser_impl.jar \
  jaxp_parser_impl %{_javadir}/libgcj-%{version}.jar 20

{
  # Rebuild the list of security providers in classpath.security.
  # This used to be a standalone script, rebuild-security-providers,
  # provided by the Fedora version of jpackage-utils.  Now it is
  # inlined here and removed from Fedora's jpackage-utils for
  # compatibility with jpackage.org's jpackage-utils.  See:
  # https://bugzilla.redhat.com/show_bug.cgi?id=260161
  suffix=security/classpath.security
  secfiles="/usr/lib/$suffix /usr/lib64/$suffix"

  for secfile in $secfiles
  do
    # check if this classpath.security file exists
    [ -f "$secfile" ] || continue

    sed -i '/^security\.provider\./d' "$secfile"

    count=0
    for provider in $(ls /etc/java/security/security.d)
    do
      count=$((count + 1))
      echo "security.provider.${count}=${provider#*-}" >> "$secfile"
    done
  done
} || :

if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%postun -n java-%{javaver}-gcj
if [ $1 -eq 0 ]
then
  alternatives --remove java %{jrebindir}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jrelnk}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
  alternatives --remove jaxp_parser_impl \
    %{_javadir}/libgcj-%{version}.jar
fi

{
  # Rebuild the list of security providers in classpath.security
  suffix=security/classpath.security
  secfiles="/usr/lib/$suffix /usr/lib64/$suffix"

  for secfile in $secfiles
  do
    # check if this classpath.security file exists
    [ -f "$secfile" ] || continue

    sed -i '/^security\.provider\./d' "$secfile"

    count=0
    for provider in $(ls /etc/java/security/security.d)
    do
      count=$((count + 1))
      echo "security.provider.${count}=${provider#*-}" >> "$secfile"
    done
  done
} || :

if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%post -n java-%{javaver}-gcj-devel
alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java         java_sdk          %{_jvmdir}/%{sdklnk} \
  --slave %{_jvmjardir}/java      java_sdk_exports  %{_jvmjardir}/%{sdklnk} \
  --slave %{_bindir}/javadoc      javadoc           %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah        javah             %{sdkbindir}/javah \
  --slave %{_bindir}/jar          jar               %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner    jarsigner         %{sdkbindir}/jarsigner \
  --slave %{_bindir}/appletviewer appletviewer      %{sdkbindir}/appletviewer \
  --slave %{_bindir}/rmic         rmic              %{sdkbindir}/rmic

alternatives \
  --install %{_jvmdir}/java-%{origin} \
  java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{origin} \
  java_sdk_%{origin}_exports %{_jvmjardir}/%{sdklnk}

alternatives \
  --install %{_jvmdir}/java-%{javaver} \
  java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{javaver} \
  java_sdk_%{javaver}_exports %{_jvmjardir}/%{sdklnk}

%postun -n java-%{javaver}-gcj-devel
if [ $1 -eq 0 ]
then
  alternatives --remove javac %{sdkbindir}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdklnk}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi

%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig

%post -n libgnat -p /sbin/ldconfig

%postun -n libgnat -p /sbin/ldconfig

%post -n libgomp
/sbin/ldconfig
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :

%preun -n libgomp
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp -p /sbin/ldconfig

%post -n libmudflap -p /sbin/ldconfig

%postun -n libmudflap -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/protoize
%{_prefix}/bin/unprotoize
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/protoize.1*
%{_mandir}/man1/unprotoize.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/SYSCALLS.c.X
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vec_types.h
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%endif
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING*

%files -n cpp -f cpplib.lang
%defattr(-,root,root)
/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
%defattr(-,root,root)
/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{_prefix}/sbin/libgcc_post_upgrade
%doc gcc/COPYING.LIB

%files c++
%defattr(-,root,root)
%{_prefix}/bin/%{gcc_target_platform}-*++
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%defattr(-,root,root)
%{_prefix}/%{_lib}/libstdc++.so.6*

%files -n libstdc++-devel
%defattr(-,root,root)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%endif
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README* libstdc++-v3/doc/html/

%files objc
%defattr(-,root,root)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%defattr(-,root,root)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%defattr(-,root,root)
%{_prefix}/%{_lib}/libobjc.so.2*

%files gfortran
%defattr(-,root,root)
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%endif
%doc rpm.doc/gfortran/*

%files -n libgfortran
%defattr(-,root,root)
%{_prefix}/%{_lib}/libgfortran.so.3*

%if %{build_java}
%files java
%defattr(-,root,root)
%{_prefix}/bin/gcj
%{_prefix}/bin/gjavah
%{_prefix}/bin/gcjh
%{_prefix}/bin/jcf-dump
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gcjh.1*
%{_infodir}/gcj*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ecj1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jvgenmain
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj-tools.so
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgij.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgij.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgij.so
%endif
%doc rpm.doc/changelogs/gcc/java/ChangeLog*

%files -n libgcj
%defattr(-,root,root)
%{_prefix}/bin/jv-convert
%{_prefix}/bin/gij
%{_prefix}/bin/gjar
%{_prefix}/bin/fastjar
%{_prefix}/bin/grepjar
%{_prefix}/bin/grmic
%{_prefix}/bin/grmid
%{_prefix}/bin/grmiregistry
%{_prefix}/bin/gtnameserv
%{_prefix}/bin/gkeytool
%{_prefix}/bin/gorbd
%{_prefix}/bin/gserialver
%{_prefix}/bin/gcj-dbtool
%if %{include_gappletviewer}
%{_prefix}/bin/gappletviewer
%{_mandir}/man1/gappletviewer.1*
%endif
%{_prefix}/bin/gjarsigner
%{_mandir}/man1/fastjar.1*
%{_mandir}/man1/grepjar.1*
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/gij.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmid.1*
%{_mandir}/man1/gserialver.1*
%{_mandir}/man1/gtnameserv.1*
%{_infodir}/fastjar.info*
%{_infodir}/cp-tools.info*
%{_prefix}/%{_lib}/libgcj.so.*
%{_prefix}/%{_lib}/libgcj-tools.so.*
%{_prefix}/%{_lib}/libgcj_bc.so.*
%{_prefix}/%{_lib}/libgij.so.*
%dir %{_prefix}/%{_lib}/gcj-%{version}
%{_prefix}/%{_lib}/gcj-%{version}/libgtkpeer.so
%{_prefix}/%{_lib}/gcj-%{version}/libgjsmalsa.so
%{_prefix}/%{_lib}/gcj-%{version}/libjawt.so
%if %{include_gappletviewer}
%{_prefix}/%{_lib}/gcj-%{version}/libgcjwebplugin.so
%endif
%{_prefix}/%{_lib}/gcj-%{version}/libjvm.so
%{_prefix}/%{_lib}/gcj-%{version}/libjavamath.so
%dir %{_prefix}/share/java
%{_prefix}/share/java/[^sl]*
%{_prefix}/share/java/libgcj-%{version}.jar
%dir %{_prefix}/%{_lib}/security
%config(noreplace) %{_prefix}/%{_lib}/security/classpath.security
%{_prefix}/%{_lib}/logging.properties
%dir %{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%if %{include_gappletviewer}
%doc rpm.doc/README.libgcjwebplugin.so
%endif

%files -n libgcj-devel
%defattr(-,root,root)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/gcj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jvmpi.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.spec
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgcj_bc.so
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgcj_bc.so
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[gj]*
%{_prefix}/include/c++/%{gcc_version}/org
%{_prefix}/include/c++/%{gcc_version}/sun
%{_prefix}/%{_lib}/pkgconfig/libgcj-*.pc
%doc rpm.doc/boehm-gc/* rpm.doc/fastjar/* rpm.doc/libffi/*
%doc rpm.doc/libjava/*

%files -n libgcj-src
%defattr(-,root,root)
%dir %{_prefix}/share/java
%{_prefix}/share/java/src*.zip
%{_prefix}/share/java/libgcj-tools-%{version}.jar

%files -n java-%{javaver}-gcj
%defattr(-,root,root,-)
%dir %{_jvmdir}/%{sdkdir}
%dir %{_jvmdir}/%{jredir}
%dir %{_jvmdir}/%{jredir}/bin
%dir %{_jvmdir}/%{jredir}/lib
%dir %{_jvmdir}/%{jredir}/lib/%{_arch}
%dir %{_jvmdir}/%{jredir}/lib/%{_arch}/client
%dir %{_jvmdir}/%{jredir}/lib/%{_arch}/server
%dir %{_jvmdir}/%{jredir}/lib/security
%dir %{jvmjardir}
%dir %{_prefix}/%{_lib}/gcj
%{_bindir}/rebuild-gcj-db
%{_jvmdir}/%{jredir}/bin/java
%{_jvmdir}/%{jredir}/bin/keytool
%{_jvmdir}/%{jredir}/bin/rmiregistry
%{_jvmdir}/%{jredir}/bin/orbd
%{_jvmdir}/%{jredir}/bin/rmid
%{_jvmdir}/%{jredir}/bin/tnameserv
%{_jvmdir}/%{jredir}/lib/security/cacerts
%{_jvmdir}/%{jredir}/lib/security/java.security
%{_jvmdir}/%{jredir}/lib/jaas.jar
%{_jvmdir}/%{jredir}/lib/jce.jar
%{_jvmdir}/%{jredir}/lib/jdbc-stdext.jar
%{_jvmdir}/%{jredir}/lib/jndi-cos.jar
%{_jvmdir}/%{jredir}/lib/jndi-dns.jar
%{_jvmdir}/%{jredir}/lib/jndi-ldap.jar
%{_jvmdir}/%{jredir}/lib/jndi-rmi.jar
%{_jvmdir}/%{jredir}/lib/jndi.jar
%{_jvmdir}/%{jredir}/lib/jsse.jar
%{_jvmdir}/%{jredir}/lib/sasl.jar
%ifarch x86_64
%{_jvmdir}/%{jredir}/lib/amd64
%endif
%{_jvmdir}/%{jrelnk}
%{jvmjardir}/jaas.jar
%{jvmjardir}/jaas-%{javaver}.jar
%{jvmjardir}/jaas-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/jce.jar
%{jvmjardir}/jce-%{javaver}.jar
%{jvmjardir}/jce-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/jdbc-stdext.jar
%{jvmjardir}/jdbc-stdext-%{javaver}.jar
%{jvmjardir}/jdbc-stdext-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/jndi.jar
%{jvmjardir}/jndi-%{javaver}.jar
%{jvmjardir}/jndi-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/jndi-cos.jar
%{jvmjardir}/jndi-cos-%{javaver}.jar
%{jvmjardir}/jndi-cos-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/jndi-dns.jar
%{jvmjardir}/jndi-dns-%{javaver}.jar
%{jvmjardir}/jndi-dns-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/jndi-ldap.jar
%{jvmjardir}/jndi-ldap-%{javaver}.jar
%{jvmjardir}/jndi-ldap-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/jndi-rmi.jar
%{jvmjardir}/jndi-rmi-%{javaver}.jar
%{jvmjardir}/jndi-rmi-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/jsse.jar
%{jvmjardir}/jsse-%{javaver}.jar
%{jvmjardir}/jsse-%{javaver}.%{javabuildver}.jar
%{jvmjardir}/sasl.jar
%{jvmjardir}/sasl-%{javaver}.jar
%{jvmjardir}/sasl-%{javaver}.%{javabuildver}.jar
%{_jvmjardir}/%{jrelnk}
%{_jvmdir}/%{sdkdir}/jre/lib/rt.jar
%{_jvmdir}/%{jredir}/lib/%{_arch}/libjawt.so
%{_jvmdir}/%{jredir}/lib/%{_arch}/client/libjvm.so
%{_jvmdir}/%{jredir}/lib/%{_arch}/server/libjvm.so
# These must not be marked %config(noreplace).  Their file names are
# used in post and postun.  Their contents are ignored, so replacing
# them doesn't matter.  .rpmnew files are harmful since they're
# interpreted by post and postun as classnames ending in rpmnew.
%{_sysconfdir}/java/security/security.d/1000-gnu.java.security.provider.Gnu
%{_sysconfdir}/java/security/security.d/1001-gnu.javax.crypto.jce.GnuCrypto
%{_sysconfdir}/java/security/security.d/1002-gnu.javax.crypto.jce.GnuSasl
%{_sysconfdir}/java/security/security.d/1003-gnu.javax.net.ssl.provider.Jessie
%{_sysconfdir}/java/security/security.d/1004-gnu.javax.security.auth.callback.GnuCallbacks

%files -n java-%{javaver}-gcj-devel
%defattr(-,root,root,-)
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/include/linux
%dir %{_jvmdir}/%{sdkdir}/lib
%{_bindir}/aot-compile
%{_bindir}/aot-compile-rpm
%{_prefix}/%{python_sitelib}/aotcompile.py*
%{_prefix}/%{python_sitelib}/classfile.py*
%{_jvmdir}/%{sdkdir}/bin/appletviewer
%{_jvmdir}/%{sdkdir}/bin/jar
%{_jvmdir}/%{sdkdir}/bin/jarsigner
%{_jvmdir}/%{sdkdir}/bin/java
%{_jvmdir}/%{sdkdir}/bin/javac
%{_jvmdir}/%{sdkdir}/bin/javadoc
%{_jvmdir}/%{sdkdir}/bin/javah
%{_jvmdir}/%{sdkdir}/bin/keytool
%{_jvmdir}/%{sdkdir}/bin/native2ascii
%{_jvmdir}/%{sdkdir}/bin/orbd
%{_jvmdir}/%{sdkdir}/bin/rmic
%{_jvmdir}/%{sdkdir}/bin/rmid
%{_jvmdir}/%{sdkdir}/bin/rmiregistry
%{_jvmdir}/%{sdkdir}/bin/serialver
%{_jvmdir}/%{sdkdir}/bin/tnameserv
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_jvmdir}/%{sdkdir}/include/jawt.h
%{_jvmdir}/%{sdkdir}/include/jni.h
%{_jvmdir}/%{sdkdir}/include/linux/jawt_md.h
%{_jvmdir}/%{sdkdir}/include/linux/jni_md.h
%{_jvmdir}/%{sdkdir}/lib/tools.jar

%files -n java-%{javaver}-gcj-src
%defattr(-,root,root,-)
%{_jvmdir}/%{sdkdir}/src.zip

%if ! %{bootstrap_java}
%files -n java-%{javaver}-gcj-javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/java-%{javaver}-gcj
# A JPackage that "provides" this directory will, in its %post script,
# remove the existing directory and install a new symbolic link to its
# versioned directory.  For Fedora we want clear file ownership so we
# make java-1.5.0-gcj-javadoc own this file.  Installing the
# corresponding JPackage over java-1.5.0-gcj-javadoc will work but
# will invalidate this file.
%doc %{_javadocdir}/java
%endif

%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root)
%{_prefix}/bin/gnat*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adalib
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adalib
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%defattr(-,root,root)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%defattr(-,root,root)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%endif
%endif

%files -n libgomp
%defattr(-,root,root)
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%files -n libmudflap
%defattr(-,root,root)
%{_prefix}/%{_lib}/libmudflap.so.0*
%{_prefix}/%{_lib}/libmudflapth.so.0*

%files -n libmudflap-devel
%defattr(-,root,root)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mf-runtime.h
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflapth.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflapth.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%endif
%doc rpm.doc/changelogs/libmudflap/ChangeLog*

%changelog
* Fri Apr 10 2009 Deepak Bhole <dbhole@redhat.com> 4.4.0-0.33
- create new java-1.5.0-gcj* packages to install JPackage compliant links

* Thu Apr  9 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.32
- update from gcc-4_4-branch
  - PRs c++/34691, c++/35146, c++/35240, c++/37806, c++/38030, c++/38850,
	c++/39608, c++/39637, c++/4926, c/37772, fortran/38152,
	fortran/39519, fortran/39594, libmudflap/38462, libstdc++/39310,
	middle-end/39573, objc/18456, objc/27377, other/39591,
	rtl-optimization/39588, rtl-optimization/39607, target/39501,
	target/39592, target/39634, testsuite/39325, tree-optimization/35011,
	tree-optimization/39595, tree-optimization/39648
  - handle .cfi_undefined(%ip) in libgcc_s unwinder (#491542)
- fix debug info for C++ static data members (#410691)
- revert fwprop fix, it causes glibc.i586 miscompilation

* Mon Mar 30 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.31
- update from gcc-4_4-branch
  - PR target/39545
  - fix Fortran bind(c) function using RESULT() (#492657)
- fix bogus warnings on strcmp/strncmp macros (#492846)

* Sat Mar 28 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.30
- update from gcc-4_4-branch
  - PRs c++/39380, c++/28274, c++/29727, c++/35652, c++/36799, c++/37647,
	c++/38638, c++/39554, libfortran/39528, middle-end/39497,
	rtl-optimization/39522, target/38034, target/39523,
	tree-optimization/39529, tree-optimization/39548,
	tree-optimization/39557
- emit debuginfo for block local externs in C (PR debug/39563)
- fix -maltivec conditional vector macro (PR target/39558)
- teach fwprop to handle asm (PR rtl-optimization/39543)

* Tue Mar 24 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.29
- update from trunk
  - PRs c++/28879, c++/37729, c++/39526, debug/39524, tree-optimization/39516

* Thu Mar 19 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.28
- update from trunk
  - PRs c++/39425, c++/39475, c/39495, debug/39485, middle-end/37805,
	middle-end/38609, middle-end/39378, middle-end/39447,
	middle-end/39500, target/35180, target/39063, target/39496
  - fix RA bug with global reg variables (#490509)
- use DW_LANG_C99 for -std=c99 or -std=gnu99 compiled C code (PR debug/38757)
- emit DW_AT_explicit when needed (PR debug/37959)
- optimize memmove into memcpy in more cases when we can prove src and dest
  don't overlap

* Tue Mar 17 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.27
- update from trunk
  - PRs debug/37890, debug/39471, debug/39474, libstdc++/39405, target/34299,
	target/39473, target/39476, target/39477, target/39482,
	testsuite/37628, testsuite/37630, testsuite/37960, testsuite/38526,
	tree-optimization/39455

* Sat Mar 14 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.26
- fix ppc64 regression caused by the power7 backport (#490149,
  PR target/39457)

* Fri Mar 13 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.25
- update from trunk
  - PRs debug/39086, debug/39432, libobjc/27466, middle-end/37850,
	target/39137, target/39181, target/39431, target/39445, target/5362,
	testsuite/39451, tree-optimization/39422
- fix ICE in gen_tagged_type_instantiation_die (#489308, PR debug/39412)
- fix memcmp builtin asm redirection (PR middle-end/39443)
- fix sparcv9 profiledbootstrap (PR bootstrap/39454)

* Thu Mar 12 2009 Dennis Gilmore <dennis@ausil.us> 
- don't build with graphite support on sparc arches
  - still missing some deps

* Tue Mar 10 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.24
- update from trunk
  - PRs ada/39221, c++/39060, c++/39367, c++/39371, libfortran/39402,
	middle-end/38028, target/39361, tree-optimization/39394
- use system cloog-ppl instead of building a private libcloog.so.0 (#489183)
- preliminary Power7 support (#463846)

* Sat Mar  7 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.23
- update from trunk
  - PRs c++/13549, c++/29469, c++/29607, c++/33492, c++/37520, c++/38908,
	c++/9634, debug/39372, middle-end/39360, rtl-optimization/39235,
	testsuite/39357, tree-optimization/39349
  - emit DW_TAG_imported* even in main or in lexical blocks that
    contain no automatic variables (#488547, PR debug/39379)
  - fix DW_AT_decl_line on DW_TAG_imported* (#488771, PR debug/39387)
  - fix SCCVN with SSA names occurring in abnormal PHIs (#488061,
    PR tree-optimization/39362)

* Wed Mar  4 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.22
- update from trunk
  - PRs ada/39172, ada/39264, bootstrap/39257, c++/36411, c++/37789,
	c++/38880, c++/39225, c++/39242, c/12245, classpath/38417,
	classpath/38912, debug/39267, debug/39285, fortran/38914,
	fortran/39292, fortran/39295, fortran/39309, fortran/39354,
	libgcj/38861, middle-end/10109, middle-end/34443,
	middle-end/39157, middle-end/39272, middle-end/39308,
	middle-end/39335, middle-end/39345, rtl-optimization/39241,
	target/33785, target/35965, target/39256, target/39261,
	target/39327, testsuite/38164, tree-optimization/37709,
	tree-optimization/39248, tree-optimization/39259,
	tree-optimization/39260, tree-optimization/39318,
	tree-optimization/39331, tree-optimizations/39259,
	tree-optimization/39358
  - fix ivopts (#486088, PR tree-optimization/39233)
  - fix SRA (#487795, PR tree-optimization/39339)
  - fix __builtin_object_size with unions (#487702,
    PR tree-optimization/39343)
- fix ppc -m64 -O2 -mtune=cell and patterns (#485067, PR target/39226)
- -march=atom/-mtune=atom support from ix86/atom branch

* Thu Feb 19 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.21
- update from trunk
  - PRs c++/39188, c++/39219, c/35447, c/38483, target/34587,
	target/38891, target/39082, target/39179, target/39224,
	target/39228, testsuite/38165, testsuite/38166,
	tree-optimization/36922, tree-optimization/39074,
  - another bogus aliasing warning fix (#485463, PR tree-optimization/39207)
- fix tail call optimization on ppc (#485067, PR target/39240)

* Tue Feb 17 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.20
- update from trunk
  - PRs c/35446, middle-end/39214, tree-optimization/39202
  - fix ICE in compute_attic (#485708, PR tree-optimization/39204)
  - fix bogus aliasing warning (#485463, PR tree-optimization/39207)
- update for i386.rpm -> i586.rpm switch

* Mon Feb 16 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.19
- update from trunk
  - PRs c++/39070, fortran/36528, fortran/36703, fortran/38259,
	libstdc++/39168, target/37049, target/38056, target/39149,
	target/39162, target/39196
  - ix86 peephole fix (#485729, PR target/39152)
  - uglify function parameter names in gthr*.h (#485619)

* Fri Feb 13 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.18
- update from trunk
  - PRs c++/30111, c++/38950, c++/39153, c/35444, middle-end/39154,
	target/38824, target/39152
- fix ICE on ppc32 with -fpic -fvisibility=hidden (#485232, PR target/39175)

* Wed Feb 11 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.17
- update from trunk
  - fix ICE on xen (PR target/39139)
  - PRs c++/34397, c++/35147, c++/36744, c++/37737, c++/38649, c++/39109,
	c/35434, c/36432, c/39035, c/39084, middle-end/35202,
	middle-end/38953, middle-end/38981, middle-end/39124,
	middle-end/39127, target/39118, target/39119, testsuite/33300,
	tree-optimization/39132
- force emitting .debug_info for empty CUs with -g3 (#479912)

* Fri Feb  6 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.16
- update from trunk
  - don't emit thunks for versioned functions (PR c++/39106)
  - fix -fstrict-aliasing miscompilation (PR tree-optimization/39100)

* Wed Feb  4 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.15
- update from trunk
  - C++ mangling fix (PR c++/39095)
  - only complain about calling main in C++ if -pedantic
- add raw string support

* Tue Feb  3 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.14
- update from trunk
- when compiling with -march=i386, don't use __sync_* builtins in
  ext/atomicity.h

* Wed Jan 28 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.13
- fix graphite make check

* Tue Jan 27 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.12
- update from trunk
- add graphite support
- change gcc default ISA and tuning:
  i386 and x86_64 -m32:
  -march=i586 -mtune=generic from -march=i386 -mtune=generic
  x86_64 -m64 remains at:
  -march=x86-64 -mtune=generic
  s390 and s390x -m31:
  -march=z9-109 -mtune=z10 from -march=g5 -mtune=z9-109
  s390x -m64:
  -march=z9-109 -mtune=z10 from -march=z900 -mtune=z9-109

* Wed Jan 21 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.9
- rebuilt without ppc64 ada bootstrap hacks

* Tue Jan 20 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.8
- attempt to enable Ada support on ppc64

* Fri Jan 16 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.3
- initial 4.4 package, using newly created redhat/gcc-4_4-branch

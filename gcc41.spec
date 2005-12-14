%define DATE 20051214
%define gcc_version 4.1.0
%define gcc_release 0.8
%define _unpackaged_files_terminate_build 0
%define multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch %{ix86} x86_64 ia64
%define build_ada 1
%else
%define build_ada 0
%endif
%define build_java 1
%ifarch s390x
%define multilib_32_arch s390
%endif
%ifarch sparc64
%define multilib_32_arch sparc
%endif
%ifarch ppc64
%define multilib_32_arch ppc
%endif
%ifarch x86_64
%define multilib_32_arch i386
%endif
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}
License: GPL
Group: Development/Languages
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: libgcc_post_upgrade.c
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
BuildRequires: binutils >= 2.16.91.0.3-1
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
BuildRequires: glibc-devel >= 2.3.90-2
%ifarch %{multilib_64_archs} sparc ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
Requires: binutils >= 2.16.91.0.3-1
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
Obsoletes: gcc3
Obsoletes: egcs
Obsoletes: gcc-chill
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
Obsoletes: libgnat < %{version}-%{release}
%endif
%ifarch sparc sparc64
Obsoletes: egcs64
%endif
Obsoletes: gcc34
Obsoletes: gcc35
Obsoletes: gcc4
Provides: gcc4 = %{version}-%{release}
Prereq: /sbin/install-info
AutoReq: true

Patch1: gcc41-ice-hack.patch
Patch2: gcc41-ppc64-m32-m64-multilib-only.patch
Patch3: gcc41-ia64-libunwind.patch
Patch4: gcc41-gnuc-rh-release.patch
Patch5: gcc41-java-nomulti.patch
Patch6: gcc41-multi32-hack.patch
Patch7: gcc41-ia64-stack-protector.patch
Patch8: gcc41-ada-pr18302.patch
Patch9: gcc41-ada-tweaks.patch
Patch10: gcc41-java-rmic.patch
Patch11: gcc41-java-slow_pthread_self.patch
Patch12: gcc41-libjava-libltdl.patch
Patch13: gcc41-fortran-finclude.patch
Patch14: gcc41-ppc64-sync.patch
Patch15: gcc41-ppc32-retaddr.patch
Patch17: gcc41-pr24823.patch
Patch18: gcc41-pr24982.patch
Patch19: gcc41-pr25180.patch
Patch20: gcc41-s390-atomic1.patch
Patch21: gcc41-rh175569.patch
Patch22: gcc41-java-src-filename.patch
Patch23: gcc41-unwind-dw2-glibc.patch
Patch24: gcc41-cxx-relro.patch

%define _gnu %{nil}
%ifarch sparc
%define gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc
%define gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparc ppc
%define gcc_target_platform %{_target_platform}
%endif

%description
The gcc package contains the GNU Compiler Collection version 4.1.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.1 shared support library
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
Obsoletes: gcc3-c++
Obsoletes: gcc34-c++
Obsoletes: gcc35-c++
Obsoletes: gcc4-c++
Provides: gcc4-c++ = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Obsoletes: libstdc++3
Obsoletes: libstdc++34
Provides: libstdc++34
Autoreq: true

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++ = %{version}-%{release}
Obsoletes: libstdc++3-devel
Obsoletes: libstdc++34-devel
Provides: libstdc++34-devel
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
Obsoletes: gcc3-objc
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
Summary: Fortran 95 support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
BuildRequires: gmp-devel >= 4.1.2-8
Prereq: /sbin/install-info
Obsoletes: gcc3-g77
Obsoletes: gcc-g77
Obsoletes: gcc4-gfortran
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran 95
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran 95 runtime
Group: System Environment/Libraries
Obsoletes: libf2c
Autoreq: true

%description -n libgfortran
This package contains Fortran 95 shared library which is needed to run
Fortran 95 dynamically linked programs.

%package -n libgomp
Summary: GCC OpenMP 2.5 shared support library
Group: System Environment/Libraries

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP 2.5 support.

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
Requires: libgcj-devel = %{version}-%{release}, zlib-devel
Obsoletes: gcc3-java
Obsoletes: gcc34-java
Obsoletes: gcc35-java
Obsoletes: gcc4-java
Provides: gcc4-java
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
BuildRequires: gtk2-devel >= 2.4.0
Requires: glib2 >= 2.4.0
BuildRequires: glib2-devel >= 2.4.0
Requires: libart_lgpl >= 2.1.0
BuildRequires: libart_lgpl-devel >= 2.1.0
BuildRequires: alsa-lib-devel
Obsoletes: gcc-libgcj
Obsoletes: libgcj3
Obsoletes: libgcj34
Obsoletes: libgcj4
Provides: libgcj4
Autoreq: true

%description -n libgcj
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%package -n libgcj-devel
Summary: Libraries for Java development using GCC
Group: Development/Languages
Requires: zip >= 2.1, libgcj = %{version}-%{release}
Obsoletes: libgcj3-devel
Obsoletes: libgcj34-devel
Obsoletes: libgcj4-devel
Provides: libgcj4-devel
Autoreq: true

%description -n libgcj-devel
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%package -n libgcj-src
Summary: Java library sources from GCC4 preview
Group: System Environment/Libraries
Requires: libgcj = %{version}-%{release}
Obsoletes: libgcj4-src
Provides: libgcj4-src
Autoreq: true

%description -n libgcj-src
The Java(tm) runtime library sources for use in Eclipse.

%package sparc32
Summary: The C compiler optimized for generating SPARC 32bit code
Group: Development/Languages
Requires: gcc = %{version}-%{release}, %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
Autoreq: true

%description sparc32
This package contains the GNU C compiler which only supports generating
32bit SPARC code, but should be faster than the 32/64bit gcc package. You
should install this package if you want to trade disk space required for
this package for faster compilation of 32bit code.

%package c++-sparc32
Summary: The C++ compiler optimized for generating SPARC 32bit code
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-sparc32 = %{version}-%{release}
Requires: %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
Autoreq: true

%description c++-sparc32
This package contains the GNU C++ compiler which only supports generating
32bit SPARC code, but should be faster than the 32/64bit gcc package. You
should install this package if you want to trade disk space required for
this package for faster compilation of 32bit code.

%package ppc32
Summary: The C compiler optimized for generating PowerPC 32bit code
Group: Development/Languages
Requires: gcc = %{version}-%{release}, %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
Autoreq: true

%description ppc32
This package contains the GNU C compiler which only supports generating
32bit PowerPC code, but should be faster than the 32/64bit gcc package. You
should install this package if you want to trade disk space required for
this package for faster compilation of 32bit code.

%package c++-ppc32
Summary: The C++ compiler optimized for generating PowerPC 32bit code
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-ppc32 = %{version}-%{release}
Requires: %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
Autoreq: true

%description c++-ppc32
This package contains the GNU C++ compiler which only supports generating
32bit PowerPC code, but should be faster than the 32/64bit gcc package. You
should install this package if you want to trade disk space required for
this package for faster compilation of 32bit code.

%package -n cpp
Summary: The C Preprocessor.
Group: Development/Languages
Prereq: /sbin/install-info
%ifarch ia64
Obsoletes: gnupro
%endif
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
Requires: gcc = %{version}-%{release}, libgnat = %{version}-%{release}
Obsoletes: gnat-devel, gcc3-gnat
Prereq: /sbin/install-info
Autoreq: true

%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development tools,
the documents and Ada 95 compiler.

%package -n libgnat
Summary: GNU Ada 95 runtime shared libraries
Group: System Environment/Libraries
Obsoletes: gnat libgnat3
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared libraries,
which are required to run programs compiled with the GNAT.

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch1 -p0 -b .ice-hack~
%patch2 -p0 -b .ppc64-m32-m64-multilib-only~
%patch3 -p0 -b .ia64-libunwind~
%patch4 -p0 -b .gnuc-rh-release~
%patch5 -p0 -b .java-nomulti~
%ifarch ppc sparc
%patch6 -p0 -b .multi32-hack~
%endif
%patch7 -p0 -b .ia64-stack-protector~
%patch8 -p0 -b .ada-pr18302~
%patch9 -p0 -b .ada-tweaks~
%patch10 -p0 -b .java-rmic~
%patch11 -p0 -b .java-slow_pthread_self~
%patch12 -p0 -b .libjava-libltdl~
%patch13 -p0 -b .fortran-finclude~
%patch14 -p0 -b .ppc64-sync~
%patch15 -p0 -b .ppc32-retaddr~
%patch17 -p0 -b .pr24823~
%patch18 -p0 -b .pr24982~
%patch19 -p0 -b .pr25180~
%patch20 -p0 -b .s390-atomic1~
%patch21 -p0 -b .rh175569~
%patch22 -p0 -b .java-src-filename~
%patch23 -p0 -b .unwind-dw2-glibc~
%patch24 -p0 -b .cxx-relro~

sed -i -e 's/4\.1\.0/4.1.0/' gcc/BASE-VER gcc/version.c
sed -i -e 's/" (Red Hat[^)]*)"/" (Red Hat %{version}-%{gcc_release})"/' gcc/version.c

sed -i -e 's/libjawt/libgcjawt/g' libjava/Makefile.{am,in}

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

%ifarch ppc
if [ -d libstdc++-v3/config/abi/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/sparc64-linux-gnu/32
fi
%endif

%build

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

if [ ! -f /usr/lib/locale/de_DE/LC_CTYPE ]; then
  mkdir locale
  localedef -f ISO-8859-1 -i de_DE locale/de_DE
  export LOCPATH=`pwd`/locale:/usr/lib/locale
fi

CC=gcc
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
%ifarch sparc sparc64
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g'`
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
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-libgcj-multifile \
%if !%{build_ada}
	--enable-languages=c,c++,objc,obj-c++,java,fortran \
%else
	--enable-languages=c,c++,objc,obj-c++,java,fortran,ada \
%endif
%if !%{build_java}
	--disable-libgcj \
%else
	--enable-java-awt=gtk --disable-dssi \
	--with-java-home=%{_prefix}/lib/jvm/java-1.4.2-gcj-1.4.2.0/jre \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifnarch sparc ppc
	--host=%{gcc_target_platform}
%endif

make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
#%ifarch %{ix86} x86_64
#make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
#%else
#make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap-lean
#%endif

# run the tests.
make %{?_smp_mflags} -k check RUNTESTFLAGS="ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++" || :
cd gcc
mv testsuite{,.normal}
make %{?_smp_mflags} -k \
  `sed -n 's/check-ada//;s/^CHECK_TARGETS[[:blank:]]*=[[:blank:]]*//p' Makefile` \
  RUNTESTFLAGS="--target_board=unix/-fstack-protector ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++" || :
mv testsuite{,.ssp}
mv testsuite{.normal,}
cd ..
echo ====================TESTING=========================
( ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================

# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto

%ifarch sparc ppc
# Build the -m32 only compiler which does not use long long for HOST_WIDE_INT
mkdir gcc32
cd gcc32
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g'`
echo "#!/bin/sh" > gcc32
echo "exec `cd ../gcc; pwd`/xgcc -B `cd ../gcc; pwd`/ $OPT_FLAGS "'"$@"' >> gcc32
chmod +x gcc32
CC=`pwd`/gcc32 CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" \
  TCFLAGS="$OPT_FLAGS" ../../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
  --enable-shared --enable-threads=posix --enable-checking=release --disable-libunwind-exceptions \
  --with-system-zlib --enable-__cxa_atexit --enable-languages=c,c++ \
  --host=%{_target_platform} --build=%{_target_platform} --target=%{_target_platform}
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc 
cd ..
%endif

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

for i in {gcc,gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/f; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i.f
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
(cd fastjar; for i in ChangeLog* README*; do
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

%install
rm -fr $RPM_BUILD_ROOT

perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/docs/html/documentation.html
ln -sf documentation.html libstdc++-v3/docs/html/index.html

cd obj-%{gcc_target_platform}

if [ ! -f /usr/lib/locale/de_DE/LC_CTYPE ]; then
  export LOCPATH=`pwd`/locale:/usr/lib/locale
fi

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

%ifarch sparc ppc
# Install the sparc/ppc -m32 only compilers
FULLPATH32=$RPM_BUILD_ROOT%{_prefix}/lib/gcc/%{_target_platform}/%{gcc_version}
FULLEPATH32=$RPM_BUILD_ROOT%{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}
mkdir -p $FULLPATH32 $FULLEPATH32
ln -sf %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include \
  $FULLPATH32/
install -m 755 gcc32/gcc/cc1 $FULLEPATH32/
install -m 755 gcc32/gcc/cc1plus $FULLEPATH32/
ln -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target_platform}-gcc \
  $RPM_BUILD_ROOT%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc ppc
cp -al $RPM_BUILD_ROOT%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform} \
  $RPM_BUILD_ROOT%{_prefix}/include/c++/%{gcc_version}/%{_target_platform}
%endif
%ifarch sparc64
ln -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target_platform}-gcc \
  $RPM_BUILD_ROOT%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64
ln -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target_platform}-gcc \
  $RPM_BUILD_ROOT%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparc ppc
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
if [ "%{build_java}" -gt 0 ]; then
# gcj -static doesn't work properly anyway, unless using --whole-archive
# and saving 35MB is not bad.
find $RPM_BUILD_ROOT -name libgcj.a -o -name lib-gnu-java-awt-peer-gtk.a \
		     -o -name libgjsmalsa.a \
		     -o -name libgij.a -o -name libgcjawt.a | xargs rm -f

mv $RPM_BUILD_ROOT%{_prefix}/lib/libgcj.spec $FULLPATH/
sed -i -e 's/lib: /&%%{static:%%eJava programs cannot be linked statically}/' \
  $FULLPATH/libgcj.spec
fi

mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgcc_s.so.1 $RPM_BUILD_ROOT/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 $RPM_BUILD_ROOT/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 $RPM_BUILD_ROOT/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparc ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif

mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/
mv -f $RPM_BUILD_ROOT%{_prefix}/include/omp.h $FULLPATH/include/
mkdir -p $FULLPATH/finclude
mv -f $RPM_BUILD_ROOT%{_prefix}/include/omp_lib* $FULLPATH/finclude/

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
#mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/classpath/libgjsmalsa.so* \
#      $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/classpath/libgjsmalsa.so* \
      $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
%endif

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.1 libobjc.so
ln -sf ../../../libstdc++.so.6.* libstdc++.so
ln -sf ../../../libgfortran.so.1.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
ln -sf ../../../libmudflap.so.0.* libmudflap.so
ln -sf ../../../libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../libgcj.so.7.* libgcj.so
ln -sf ../../../lib-gnu-java-awt-peer-gtk.so.7.* lib-gnu-java-awt-peer-gtk.so
ln -sf ../../../libgjsmalsa.so.0.* libgjsmalsa.so
ln -sf ../../../libgij.so.7.* libgij.so
ln -sf ../../../libgcjawt.so.7.* libgcjawt.so
%endif
%if %{build_ada}
cd adalib
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-4.1.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-4.1.so
cd ..
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.1 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.* libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.1.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
ln -sf ../../../../%{_lib}/libmudflap.so.0.* libmudflap.so
ln -sf ../../../../%{_lib}/libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../../%{_lib}/libgcj.so.7.* libgcj.so
ln -sf ../../../../%{_lib}/lib-gnu-java-awt-peer-gtk.so.7.* lib-gnu-java-awt-peer-gtk.so
ln -sf ../../../../%{_lib}/libgjsmalsa.so.0.* libgjsmalsa.so
ln -sf ../../../../%{_lib}/libgij.so.7.* libgij.so
ln -sf ../../../../%{_lib}/libgcjawt.so.7.* libgcjawt.so
%endif
%if %{build_ada}
cd adalib
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-4.1.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-4.1.so
cd ..
%endif
fi
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libsupc++.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgfortran.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgfortranbegin.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libobjc.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libmudflap{,th}.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/include/mf-runtime.h include/

%ifarch sparc ppc
ln -sf ../../../../../lib64/libobjc.so.1 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.* | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.1.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
ln -sf ../`echo ../../../../lib/libmudflap.so.0.* | sed s~/lib/~/lib64/~` 64/libmudflap.so
ln -sf ../`echo ../../../../lib/libmudflapth.so.0.* | sed s~/lib/~/lib64/~` 64/libmudflapth.so
if [ "%{build_java}" -gt 0 ]; then
ln -sf ../`echo ../../../../lib/libgcj.so.7.* | sed s~/lib/~/lib64/~` 64/libgcj.so
ln -sf ../`echo ../../../../lib/lib-gnu-java-awt-peer-gtk.so.7.* | sed s~/lib/~/lib64/~` 64/lib-gnu-java-awt-peer-gtk.so
ln -sf ../`echo ../../../../lib/libgjsmalsa.so.0.* | sed s~/lib/~/lib64/~` 64/libgjsmalsa.so
ln -sf ../`echo ../../../../lib/libgij.so.7.* | sed s~/lib/~/lib64/~` 64/libgij.so
ln -sf ../`echo ../../../../lib/libgcjawt.so.7.* | sed s~/lib/~/lib64/~` 64/libgcjawt.so
fi
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libsupc++.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libgfortran.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libgfortranbegin.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libobjc.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libgomp.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libmudflap{,th}.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.1 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.* | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.1.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
ln -sf ../`echo ../../../../lib64/libmudflap.so.0.* | sed s~/../lib64/~/~` 32/libmudflap.so
ln -sf ../`echo ../../../../lib64/libmudflapth.so.0.* | sed s~/../lib64/~/~` 32/libmudflapth.so
if [ "%{build_java}" -gt 0 ]; then
ln -sf ../`echo ../../../../lib64/libgcj.so.7.* | sed s~/../lib64/~/~` 32/libgcj.so
ln -sf ../`echo ../../../../lib64/lib-gnu-java-awt-peer-gtk.so.7.* | sed s~/../lib64/~/~` 32/lib-gnu-java-awt-peer-gtk.so
ln -sf ../`echo ../../../../lib64/libgjsmalsa.so.0.* | sed s~/../lib64/~/~` 32/libgjsmalsa.so
ln -sf ../`echo ../../../../lib64/libgij.so.7.* | sed s~/../lib64/~/~` 32/libgij.so
ln -sf ../`echo ../../../../lib64/libgcjawt.so.7.* | sed s~/../lib64/~/~` 32/libgcjawt.so
fi
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libsupc++.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libgfortran.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libgfortranbegin.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libobjc.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libgomp.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libmudflap{,th}.*a 32/
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
if [ "%{build_java}" -gt 0 ]; then
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgcj.a 32/libgcj.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/lib-gnu-java-awt-peer-gtk.a 32/lib-gnu-java-awt-peer-gtk.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgij.a 32/libgij.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgcjawt.a 32/libgcjawt.a
fi
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libmudflap.a -o -name libmudflapth.a \
		    -o -name libgcc.a -o -name libgcov.a \) -a -type f`
popd
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgfortran.so.1.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libmudflap{,th}.so.0.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libobjc.so.1.*

%if %{build_ada}
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgnat*so*
%endif

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

%if %{build_java}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/java/gcj-endorsed \
	 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
chmod 755 $RPM_BUILD_ROOT%{_prefix}/share/java/gcj-endorsed \
	  $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version} \
	  $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
touch $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcc.info.gz

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz
fi

%post -n cpp
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/cpp.info.gz

%preun -n cpp
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz
fi

%post gfortran
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz

%preun gfortran
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz
fi

%post java
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcj.info.gz

%preun java
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcj.info.gz
fi

%post gnat
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat_ugn_unw.info.gz
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz

%preun gnat
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn_unw.info.gz
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz
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
  --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz

%preun -n libgcj
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz
fi

%postun -n libgcj -p /sbin/ldconfig

%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig

%post -n libgnat -p /sbin/ldconfig

%postun -n libgnat -p /sbin/ldconfig

%post -n libgomp -p /sbin/ldconfig

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
%ifarch sparc ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/README
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
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
%ifarch sparc ppc
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
%ifarch sparc ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%ifarch sparc sparc64 ppc ppc64
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
%{_prefix}/include/c++/%{gcc_version}/[^gj]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%endif
%ifnarch sparc sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%endif
%ifnarch sparc ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README* libstdc++-v3/docs/html/

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
%ifarch sparc ppc
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
%{_prefix}/%{_lib}/libobjc.so.1*

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
%ifarch sparc ppc
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
%{_prefix}/%{_lib}/libgfortran.so.1*

%if %{build_java}
%files java
%defattr(-,root,root)
%{_prefix}/bin/gcj
%{_prefix}/bin/gcjh
%{_prefix}/bin/gjnih
%{_prefix}/bin/jcf-dump
%{_prefix}/bin/jv-scan
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/gcjh.1*
%{_mandir}/man1/gjnih.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/jv-scan.1*
%{_infodir}/gcj*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jvgenmain
%doc rpm.doc/changelogs/gcc/java/ChangeLog*

%files -n libgcj
%defattr(-,root,root)
%{_prefix}/bin/jv-convert
%{_prefix}/bin/gij
%{_prefix}/bin/fastjar
%{_prefix}/bin/grepjar
%{_prefix}/bin/grmic
%{_prefix}/bin/grmiregistry
%{_prefix}/bin/gcj-dbtool
%{_mandir}/man1/fastjar.1*
%{_mandir}/man1/grepjar.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/gij.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_infodir}/fastjar*
%{_prefix}/%{_lib}/libgcj.so.*
%{_prefix}/%{_lib}/lib-gnu-java-awt-peer-gtk.so.*
%{_prefix}/%{_lib}/libgjsmalsa.so.*
%{_prefix}/%{_lib}/libgij.so.*
%{_prefix}/%{_lib}/libgcjawt.so.*
%dir %{_prefix}/share/java
%{_prefix}/share/java/[^s]*
%dir %{_prefix}/lib/security
%config(noreplace) %{_prefix}/lib/security/classpath.security
%config(noreplace) %{_prefix}/lib/security/libgcj.security
%{_prefix}/lib/logging.properties
%dir %{_prefix}/%{_lib}/gcj-%{version}
%dir %{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/gcj-%{version}/classmap.db

%files -n libgcj-devel
%defattr(-,root,root)
%{_prefix}/bin/addr2name.awk
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib-gnu-java-awt-peer-gtk.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgij.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcjawt.so
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/lib-gnu-java-awt-peer-gtk.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgij.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcjawt.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/lib-gnu-java-awt-peer-gtk.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgij.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcjawt.so
%endif
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[gj]*
%{_prefix}/lib/pkgconfig/libgcj.pc
%doc rpm.doc/boehm-gc/* rpm.doc/fastjar/* rpm.doc/libffi/*
%doc rpm.doc/libjava/*
%endif

%files -n libgcj-src
%defattr(-,root,root)
%dir %{_prefix}/share/java
%{_prefix}/share/java/src*.zip

%if %{build_ada}
%files gnat
%defattr(-,root,root)
%{_prefix}/bin/gnat*
%{_prefix}/bin/gpr*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%defattr(-,root,root)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so
%endif

%files -n libgomp
%defattr(-,root,root)
%{_prefix}/%{_lib}/libgomp.so.1*
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.so
%endif
%doc rpm.doc/changelogs/libmudflap/ChangeLog*

%ifarch sparc
%files sparc32
%defattr(-,root,root)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{_target_platform}
%dir %{_prefix}/lib/gcc/%{_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{_target_platform}
%dir %{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}/cc1
%{_prefix}/lib/gcc/%{_target_platform}/%{gcc_version}/include

%files c++-sparc32
%defattr(-,root,root)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{_target_platform}
%dir %{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}/cc1plus
%endif

%ifarch ppc
%files ppc32
%defattr(-,root,root)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{_target_platform}
%dir %{_prefix}/lib/gcc/%{_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{_target_platform}
%dir %{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}/cc1
%{_prefix}/lib/gcc/%{_target_platform}/%{gcc_version}/include

%files c++-ppc32
%defattr(-,root,root)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{_target_platform}
%dir %{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{_target_platform}/%{gcc_version}/cc1plus
%endif

%changelog
* Wed Dec 12 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.8
- update from gcc-4_1-branch (-r108414:108539)
  - PRs classpath/25389, fortran/23815, fortran/25078, target/25254
- fix Java ICE on initialized static final var used in case
  (Andrew Haley, #175569)
- fix crash in _Unwind_IteratePhdrCallback (Andrew Haley)
- don't Require alsa-lib-devel, just BuildRequire it
  (#175627)
- use .gnu.linkonce.d.rel.ro.* sections for objects that
  are constant after relocation processing

* Mon Dec 12 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.7
- update from gcc-4_1-branch (-r108157:108414)
  - PRs c++/19317, c++/19397, c++/19762, c++/19764, c++/25010, c++/25300,
	c++/25337, debug/24908, fortran/25292, libfortran/25116,
	libgcj/25265, target/17828, target/19005, target/23424,
	target/25212, target/25258, target/25311, testsuite/20772,
	testsuite/24478, testsuite/25167, tree-optimization/25248
- update from gomp-20050608-branch (up to -r108424)
- add BuildReq for alsa-lib-devel and configure with --disable-dssi
- sort files in libgcj-*.jar and touch them to latest ChangeLog
  timestamp, so that libgcj-*.jar is identical across multilib arches
- don't use pushw instruction on i?86, as that leads to ICEs
  in def_cfa_1, because negative CFA offsets not multiple of 4
  aren't representable in the unwind and debug info (PR debug/25023,
  PR target/25293)
- fix ICEs with x86_64 -mlarge-data-threshold=N and STRING_CSTs
  (Jan Hubicka, PR target/24188)
- fix Java ICE with input_filename being unset (Alexandre Oliva, #174912)
- don't accept invalid int x,; in C++ (Petr Machata, PR c++/24907)
- fix Java ICE in do_resolve_class (Andrew Haley, PR java/25366,
  PR java/25368)
- make sure g*.dg/compat/struct-layout-1.exp generated tests
  don't use arrays with entries aligned more than their size (PR c++/25331)
- don't use -liberty in g++.dg/compat/struct-layout-1.exp tests

* Wed Dec  7 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.6
- allow #pragmas at C struct scope as well as ObjC class scope
  (PR c/25246)
- some gomp testcase fixes

* Wed Dec  7 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.5
- update from gcc-4_1-branch (-r107810:108157)
  - PRs bootstrap/25207, c++/24103, c++/24138, c++/24173, fortran/15809,
	fortran/21302, fortran/23912, java/25283, libfortran/24919,
	libgfortran/25149, middle-end/25176, other/13873, target/18580,
	target/24108, target/24475, target/24934, target/25199,
	testsuite/25247, tree-optimization/24963
- update from gomp-20050608-branch (up to -r108105)
- -Wstrict-aliasing C++ support (Richard Guenther, Dirk Mueller,
  Paolo Carlini, PRs c++/14024, libstdc++/24975)
- fix mark_used_regs regression (Andreas Krebbel, PR rtl-optimization/24823)
- fix reload ICE (Kaz Kojima, PR target/24982)
- fix PPC ICE on Linux kernel (Paolo Bonzini, PR target/24982)
- fix s390{,x} shifts with shift count ANDed with constant mask
  (Andreas Krebbel, PR target/25268)
- s390{,x} atomic builtins enhancements (Adrian Straetling)

* Thu Dec  1 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.4
- update from gcc-4_1-branch (-r107618:107810)
  - PRs c++/21123, c++/21166, fortran/24223, fortran/24705, java/18278,
	libgfortran/25109, middle-end/20109, middle-end/25120,
	middle-end/25158, rtl-opt/24930
- use %%{_tmppath} in BuildRoot (#174594)
- require libgomp in gcc subpackage
- fix Java .so symlinks

* Tue Nov 29 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.3
- fix IA-64 local-exec TLS handling
- fix IA-64 __sync_fetch_and_{sub,xor,...}

* Mon Nov 28 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.2
- update from gcc-4_1-branch (-r107462:107618)
  - PRs fortran/24917, libgcj/25016, libgfortran/24945, middle-end/21309,
	middle-end/25022, libfortran/24991
- update from gomp-20050608-branch (up to -r107619)
  - fix omp_get_wti{me,ck} on older kernels
- ppc32 EH fix
- fix #pragma omp atomic
- resurrected multi32 hack for ppc32 and sparc32

* Thu Nov 24 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.1
- initial 4.1 package, using newly created redhat/gcc-4_1-branch

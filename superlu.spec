%define major 5
%define libname %mklibname superlu %{major}
%define devname %mklibname superlu -d
%define _disable_ld_no_undefined %nil

%define oname SuperLU
%define Werror_cflags %{nil}

Summary:	Matrix solver
Name:		superlu
Version:	5.2.2
Release:	1
License:	BSD
Group:		Development/C
Url:		http://crd.lbl.gov/~xiaoye/SuperLU/
Source0:	https://github.com/xiaoyeli/superlu/archive/v%{version}.tar.gz
BuildRequires:	gcc-gfortran
BuildRequires:	tcsh
BuildRequires:	pkgconfig(blas)
BuildRequires:	cmake
# Build with -fPIC
Patch0:		%{name}-5x-add-fpic.patch
# Build shared library
Patch1:		%{name}-5x-build-shared-lib3.patch
# Fixes testsuite
Patch3:		%{name}-5x-fix-testsuite.patch
#Patch4:		https://data.gpo.zugaina.org/gentoo/sci-libs/superlu/files/superlu-5.2.2-no-internal-blas.patch
# remove non-free mc64 functionality
# patch obtained from the debian package
#Patch4:		%{name}-removemc64.patch

%description
SuperLU is an algorithm that uses group theory to optimize LU
decomposition of sparse matrices. It's the fastest direct solver for
linear systems that the author is aware of.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for SuperLU
Group:		System/Libraries

%description -n %{libname}
SuperLU is an algorithm that uses group theory to optimize LU
decomposition of sparse matrices. It's the fastest direct solver for
linear systems that the author is aware of.

%files -n %{libname}
%{_libdir}/libsuperlu.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and libraries for SuperLU development
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	%{oname}-devel = %{EVRD}

%description -n %{devname}
Header files and libraries for SuperLU development.

%files -n %{devname}
%doc README
%doc DOC
%{_includedir}/*.h
%{_libdir}/cmake/superlu/*.cmake
%{_libdir}/libsuperlu.so
%{_libdir}/pkgconfig/superlu.pc

#----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

# respect user's CFLAGS
sed -i -e 's/O3//' CMakeLists.txt

find . -type f | sed -e "/TESTING/d" | xargs chmod a-x

cp -p MAKE_INC/make.linux make.inc
sed -i	-e "s|-O3|%{optflags}|"							\
	-e "s|\$(SUPERLULIB) ||"							\
	-e "s|\$(HOME)/Dropbox/Codes/%{name}/%{name}|%{_builddir}/%{name}_%{version}|"	\
	-e 's|SuperLUroot.*|SuperLUroot = "%{_builddir}/%{name}_%{version}"|'		\
	-e 's!lib/libsuperlu_5.1.a$!SRC/libsuperlu.so!'					\
	-e 's!-shared!& %{ldflags}!'							\
	-e "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lsatlas|"				\
	make.inc

%build
%set_build_flags
%cmake -DCMAKE_BUILD_TYPE=Release \
	-Denable_internal_blaslib:BOOL=OFF \
	-DUSE_XSDK_DEFAULTS='FALSE' \
	-Denable_tests=OFF \
	-DBUILD_SHARED_LIBS=ON

%make_build

%install
%make_install -C build
#fix permissions
chmod 644 MATLAB/*

# remove all build examples
cd EXAMPLE
make clean
rm -rf *itersol*
cd ..
mv EXAMPLE examples
cp FORTRAN/README README.fortran

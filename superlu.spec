%define major 5
%define libname %mklibname superlu %major
%define develname %mklibname superlu -d
%define __noautoreq 'libsatlas\\.so\\.(.*)|libtatlas\\.so\\.(.*)'
%define _disable_lto 1
%define _disable_ld_no_undefined 1
%define oname SuperLU

Summary:        Matrix solver
Name:           superlu
Version:        5.2.1
Release:        1
License:        BSD
Group:          Development/C
URL:            http://crd.lbl.gov/~xiaoye/SuperLU/
Source0:        http://crd.lbl.gov/~xiaoye/SuperLU/%{name}_%{version}.tar.gz
Source1:        %{name}.rpmlintrc
# Build with -fPIC
Patch0:		%{name}-5x-add-fpic.patch
# Build shared library
Patch1:		%{name}-5x-build-shared-lib3.patch
# Fixes testsuite
Patch3:		%{name}-5x-fix-testsuite.patch
# remove non-free mc64 functionality
# patch obtained from the debian package
Patch4:		%{name}-removemc64.patch
BuildRequires:	gcc-gfortran
BuildRequires:	libatlas-devel
BuildRequires:	tcsh
BuildRequires:	cmake

%description
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.

%package -n     %{libname}
Summary:        Shared library for SuperLU
Group:          System/Libraries
Obsoletes:      %{name} < %{version}-%{release}

%description -n %{libname}
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.

%package -n	%{develname}
Summary:        Header files and libraries for SuperLU development
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains the header files
and libraries for use with CUnit package.

%prep
%setup -qn %{oname}_%{version}
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4

find . -type f | sed -e "/TESTING/d" | xargs chmod a-x
# Remove the shippped executables from EXAMPLE
find EXAMPLE -type f | while read file
do
   [ "$(file $file | awk '{print $2}')" = ELF ] && rm $file || :
done
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
%setup_compile_flags
%cmake -DCMAKE_BUILD_TYPE=Release -Denable_blaslib=ON -DUSE_XSDK_DEFAULTS='FALSE' -Denable_tests=OFF
%make

%install
%makeinstall_std -C build

#mkdir -p %{buildroot}%{_libdir}
#mkdir -p %{buildroot}%{_includedir}/%{oname}
#install -p SRC/libsuperlu.so.%{version} %{buildroot}%{_libdir}
#install -p SRC/*.h %{buildroot}%{_includedir}/%{oname}
#chmod -x %{buildroot}%{_includedir}/%{oname}/*.h
#cp -Pp SRC/libsuperlu.so %{buildroot}%{_libdir}

#fix permissions
chmod 644 MATLAB/*

# remove all build examples
cd EXAMPLE
make clean
rm -rf *itersol*
cd ..
mv EXAMPLE examples
cp FORTRAN/README README.fortran

%check
ln -s examples/ EXAMPLE
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
make testing
echo -ne "\nTest results\n"
for i in stest dtest ctest ztest; do
    cat TESTING/$i.out
done

%files -n %{libname}
%{_libdir}/libsuperlu.so.%{major}*

%files -n %{develname}
%doc DOC
%doc README
%{_includedir}/*.h
%{_libdir}/libsuperlu.so

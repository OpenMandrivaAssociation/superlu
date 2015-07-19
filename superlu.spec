%define major 4
%define libname %mklibname superlu %major
%define develname %mklibname superlu -d
%define __noautoreq 'libsatlas\\.so\\.(.*)|libtatlas\\.so\\.(.*)'

%define oname SuperLU

Summary:        Matrix solver
Name:           superlu
Version:        4.3
Release:        10
License:        BSD
Group:          Development/C
URL:            http://crd.lbl.gov/~xiaoye/SuperLU/
Source0:        http://crd.lbl.gov/~xiaoye/SuperLU/%{name}_%{version}.tar.gz
Source1:        %{name}.rpmlintrc
BuildRequires:	gcc-gfortran, libatlas-devel
BuildRequires:	tcsh
# Build with -fPIC
Patch0:		%{oname}-add-fpic.patch
# Build shared library
Patch1:		%{oname}-build-shared-lib3.patch
# Fixes FTBFS if "-Werror=format-security" flag is used (#1037343)
Patch2:		%{oname}-fix-format-security.patch
# Fixes testsuite
Patch3:		%{oname}-fix-testsuite.patch

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
%patch2 -p1
%patch3 -p1
find . -type f | sed -e "/TESTING/d" | xargs chmod a-x
# Remove the shippped executables from EXAMPLE
find EXAMPLE -type f | while read file
do
   [ "$(file $file | awk '{print $2}')" = ELF ] && rm $file || :
done
cp -p MAKE_INC/make.linux make.inc
sed -i	-e "s|-O3|$RPM_OPT_FLAGS|"							\
	-e "s|\$(SUPERLULIB) ||"							\
	-e "s|\$(HOME)/Codes/%{oname}_%{version}|%{_builddir}/%{oname}_%{version}|"	\
	-e 's!lib/libsuperlu_4.3.a$!SRC/libsuperlu.so!'					\
	-e 's!-shared!& %{ldflags}!'							\
	-e "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lsatlas|"				\
	make.inc

%build
make %{?_smp_mflags} superlulib
make -C TESTING

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{oname}
install -p SRC/libsuperlu.so.%{version} %{buildroot}%{_libdir}
install -p SRC/*.h %{buildroot}%{_includedir}/%{oname}
chmod -x %{buildroot}%{_includedir}/%{oname}/*.h
cp -Pp SRC/libsuperlu.so %{buildroot}%{_libdir}

%check
pushd TESTING
for _test in c d s z
do
  chmod +x ${_test}test.csh
  ./${_test}test.csh
done
popd

%files -n %{libname}
%doc README
%{_libdir}/libsuperlu.so.*

%files -n %{develname}
%doc DOC
%{_includedir}/%{oname}/
%{_libdir}/libsuperlu.so

%define major 4
%define libname %mklibname superlu %major
%define develname %mklibname superlu -d

%define oname SuperLU
%define Werror_cflags %nil

Summary:        Matrix solver
Name:           superlu
Version:        4.3
Release:        %mkrel 6
License:        BSD
Group:          Development/C
URL:            http://crd.lbl.gov/~xiaoye/SuperLU/
Source0:        http://crd.lbl.gov/~xiaoye/SuperLU/%{name}_%{version}.tar.gz
BuildRequires:	gcc-gfortran, blas-devel
BuildRequires:	tcsh
# Build with -fPIC
Patch0:		%{oname}-add-fpic.patch
# Build shared library
Patch1:		%{oname}-build-shared-lib3.patch

%description
SuperLU is an algorithm that uses group theory to optimize LU
decomposition of sparse matrices. It's the fastest direct solver for
linear systems that the author is aware of.


%package -n     %{libname}
Summary:        Shared library for SuperLU
Group:          System/Libraries
Obsoletes:      %{name} < %{version}-%{release}

%description -n %{libname}
SuperLU is an algorithm that uses group theory to optimize LU
decomposition of sparse matrices. It's the fastest direct solver for
linear systems that the author is aware of.


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
chmod a-x SRC/qselect.c 
cp -p MAKE_INC/make.linux make.inc
sed -i "s|-O3|$RPM_OPT_FLAGS|" make.inc
sed -i "s|\$(SUPERLULIB) ||" make.inc
sed -i "s|\$(HOME)/Codes/%{name}_%{version}|%{_builddir}/%{name}_%{version}|" make.inc
sed -i "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lblas|" make.inc

find . -perm 0600 -exec chmod 0644 {} \;

%build
%make superlulib BLASLIB="$(pkg-config --libs blas)"

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
install -p SRC/libsuperlu.so.%{version} %{buildroot}%{_libdir}
install -p SRC/*.h %{buildroot}%{_includedir}/%{name}
chmod -x %{buildroot}%{_includedir}/%{name}/*.h
cp -Pp SRC/libsuperlu.so %{buildroot}%{_libdir}

%files -n %{libname}
%{_libdir}/libsuperlu.so.*

%files -n %{develname}
%doc README
%doc DOC
%{_includedir}/%{name}/
%{_libdir}/libsuperlu.so

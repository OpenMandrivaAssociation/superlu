%define oname SuperLU

Summary:        Matrix solver
Name:           superlu
Version:        3.0
Release:        %mkrel 2
License:        BSD
Group:          Development/C
URL:            http://crd.lbl.gov/~xiaoye/SuperLU/
Source:         http://crd.lbl.gov/~xiaoye/SuperLU/%{name}_%{version}.tar.bz2
Source1:        superlu_ug.ps.gz
Patch0:		superlu-3.0-makefile.patch
Patch1:		superlu-3.0-i586-make.inc.patch
Patch2:		superlu-3.0-x86_64-make.inc.patch
Patch3:         superlu-overflow.patch
Patch4:         superlu-dont-opt-away.diff
Patch5:         superlu-initialize.diff
BuildRequires:	gcc-gfortran, blas-devel
BuildRequires:	tcsh
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot

%description
SuperLU is an algorithm that uses group theory to optimize LU
decomposition of sparse matrices. It's the fastest direct solver for
linear systems that the author is aware of.

%prep
%setup -qn %{oname}_%{version}
%patch0 -p0

%ifarch x86_64
%patch2 -p0
%else
%patch1 -p0
%endif

%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
perl -pi -e "s/CFLAGS=.*/CFLAGS=%{optflags}/" make.inc
make all

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}

install libsuperlu_%{version}.a %{buildroot}%{_libdir}/libsuperlu_%{version}.a

cp -pf README %{buildroot}%{_docdir}/%{name}-%{version}/README
cp -pf %{SOURCE1} %{buildroot}%{_docdir}/%{name}-%{version}/
cp -ax EXAMPLE %{buildroot}%{_docdir}/%{name}-%{version}/
cp -ax FORTRAN %{buildroot}%{_docdir}/%{name}-%{version}/

%clean 
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}/*
%{_libdir}/*.a
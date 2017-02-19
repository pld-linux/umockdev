Summary:	Mock hardware devices for creating unit tests
Summary(pl.UTF-8):	Imitowanie urządzeń sprzętowych na potrzeby testów jednostkowych
Name:		umockdev
Version:	0.8.13
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/martinpitt/umockdev/releases
Source0:	https://github.com/martinpitt/umockdev/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	88535a6ab705b3a854f1da9f7a5a6ddb
URL:		https://github.com/martinpitt/umockdev
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 1.32
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libtool >= 2:2.2
BuildRequires:	python >= 2
BuildRequires:	udev-devel
BuildRequires:	udev-glib-devel
BuildRequires:	vala >= 2:0.16.1
Requires:	glib2 >= 1:2.32.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
umockdev mocks Linux devices for creating integration tests for
hardware related libraries and programs. It also provides tools to
record the properties and behaviour of particular devices, and to run
a program or test suite under a test bed with the previously recorded
devices loaded. This allows developers of software like gphoto or
libmtp to receive these records in bug reports and recreate the
problem on their system without having access to the affected
hardware.

%description -l pl.UTF-8
umockdev imituje urządzenia pod Linuksem w celu tworzenia testów
integracyjnych dla bibliotek i programów związanych ze sprzętem.
Dostarcza także narzędzia do nagrywania właściwości i zachowania
określonych urządzeń oraz uruchamiania programów lub testów w
środowisku testowym z wczytanymi wcześniej nagranymi danymi
urządzenia. Pozwala to programistom z projektów takich jak gphoto czy
libmtp otrzymywać takie nagrania w zgłoszeniach błędów i odtwarzać we
własnym systemie bez dostępu do sprzętu dotkniętego problemem.

%package devel
Summary:	Header files for umockdev library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki umockdev
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0

%description devel
Header files for umockdev library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki umockdev.

%package static
Summary:	Static umockdev library
Summary(pl.UTF-8):	Statyczna biblioteka umockdev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static umockdev library.

%description static -l pl.UTF-8
Statyczna biblioteka umockdev.

%package -n vala-umockdev
Summary:	Vala API for umockdev library
Summary(pl.UTF-8):	API języka Vala do biblioteki umockdev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16.1
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-umockdev
Vala API for umockdev library.

%description -n vala-umockdev -l pl.UTF-8
API języka Vala do biblioteki umockdev.

%package apidocs
Summary:	umockdev API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki umockdev
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for umockdev library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki umockdev.

%prep
%setup -q

%build
%{__libtoolize}
%{__gtkdocize} --docdir docs
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON=/usr/bin/python \
	--enable-gtk-doc \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/umockdev

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.rst docs/script-format.txt
%attr(755,root,root) %{_bindir}/umockdev-record
%attr(755,root,root) %{_bindir}/umockdev-run
%attr(755,root,root) %{_bindir}/umockdev-wrapper
%attr(755,root,root) %{_libdir}/libumockdev.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libumockdev.so.0
%attr(755,root,root) %{_libdir}/libumockdev-preload.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libumockdev-preload.so.0
%{_libdir}/girepository-1.0/UMockdev-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libumockdev.so
%{_datadir}/gir-1.0/UMockdev-1.0.gir
%{_includedir}/umockdev-1.0
%{_pkgconfigdir}/umockdev-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libumockdev.a

%files -n vala-umockdev
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/umockdev-1.0.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/umockdev

#
# Conditional build:
%bcond_without	apidocs	# gtk-doc API documentation

Summary:	Mock hardware devices for creating unit tests
Summary(pl.UTF-8):	Imitowanie urządzeń sprzętowych na potrzeby testów jednostkowych
Name:		umockdev
Version:	0.17.17
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/martinpitt/umockdev/releases
Source0:	https://github.com/martinpitt/umockdev/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	f966821009a94be4e0e3011190ad03e0
URL:		https://github.com/martinpitt/umockdev
BuildRequires:	gcc >= 6:4.7
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 1.32
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.14}
BuildRequires:	libpcap-devel
BuildRequires:	libgudev-devel >= 232
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	vala >= 2:0.16.1
BuildRequires:	xz
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
Obsoletes:	umockdev-static < 0.15

%description devel
Header files for umockdev library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki umockdev.

%package -n vala-umockdev
Summary:	Vala API for umockdev library
Summary(pl.UTF-8):	API języka Vala do biblioteki umockdev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16.1
BuildArch:	noarch

%description -n vala-umockdev
Vala API for umockdev library.

%description -n vala-umockdev -l pl.UTF-8
API języka Vala do biblioteki umockdev.

%package apidocs
Summary:	umockdev API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki umockdev
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for umockdev library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki umockdev.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md docs/script-format.txt
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
%attr(755,root,root) %{_libdir}/libumockdev-preload.so
%{_datadir}/gir-1.0/UMockdev-1.0.gir
%{_includedir}/umockdev-1.0
%{_pkgconfigdir}/umockdev-1.0.pc

%files -n vala-umockdev
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/umockdev-1.0.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/umockdev
%endif

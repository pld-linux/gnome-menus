#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Implementation of the draft Desktop Menu Specification
Summary(pl.UTF-8):	Implementacja specyfikacji menu systemów biurkowych
Name:		gnome-menus
Version:	3.36.0
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-menus/3.36/%{name}-%{version}.tar.xz
# Source0-md5:	a8fd71fcf31a87fc799d80396a526829
URL:		https://www.gnome.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools >= 0.19.4
BuildRequires:	glib2-devel >= 1:2.30.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	filesystem >= 4.1-15
Provides:	xdg-menus
Obsoletes:	gnome-menus-editor
Obsoletes:	gnome-menus-filter-default
Obsoletes:	gnome-menus-filter-desktop
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
<http://www.freedesktop.org/Standards/menu-spec>.

%description -l pl.UTF-8
Pakiet zawiera implementację specyfikacji menu systemów biurkowych z
freedesktop.org: <http://www.freedesktop.org/Standards/menu-spec>.

%package libs
Summary:	gnome-menus library
Summary(pl.UTF-8):	Biblioteka gnome-menus
Group:		Libraries
Requires:	glib2 >= 1:2.30.0
Provides:	gnome-vfs-menu-module = 1.1-1
Provides:	gnome-vfs2-module-menu = 1.1-1
Obsoletes:	gnome-vfs-menu-module
Obsoletes:	gnome-vfs2-module-menu
Obsoletes:	gnome-vfs2-vfolder-menu

%description libs
gnome-menus library.

%description libs -l pl.UTF-8
Biblioteka gnome-menus.

%package devel
Summary:	Header files of gnome-menus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gnome-menus
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.30.0

%description devel
Headers for gnome-menus library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gnome-menus.

%package static
Summary:	Static gnome-menus library
Summary(pl.UTF-8):	Statyczna biblioteka gnome-menus
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of gnome-menu library.

%description static -l pl.UTF-8
Statyczna biblioteka gnome-menu.

%prep
%setup -q

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# not supported by glibc (as of 2.21-5)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{gn,io}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_sysconfdir}/xdg/menus/gnome-applications.menu
%{_datadir}/desktop-directories/AudioVideo.directory
%{_datadir}/desktop-directories/Development.directory
%{_datadir}/desktop-directories/Education.directory
%{_datadir}/desktop-directories/Game.directory
%{_datadir}/desktop-directories/Graphics.directory
%{_datadir}/desktop-directories/Network.directory
%{_datadir}/desktop-directories/Office.directory
%{_datadir}/desktop-directories/System-Tools.directory
%{_datadir}/desktop-directories/Utility.directory
%{_datadir}/desktop-directories/Utility-Accessibility.directory
%{_datadir}/desktop-directories/X-GNOME-*.directory

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-menu-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-menu-3.so.0
%{_libdir}/girepository-1.0/GMenu-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-menu-3.so
%{_datadir}/gir-1.0/GMenu-3.0.gir
%{_pkgconfigdir}/libgnome-menu-3.0.pc
%{_includedir}/gnome-menus-3.0

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgnome-menu-3.a
%endif

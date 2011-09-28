Summary:	Implementation of the draft Desktop Menu Specification
Summary(pl.UTF-8):	Implementacja specyfikacji menu systemów biurkowych
Name:		gnome-menus
Version:	3.2.0.1
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-menus/3.2/%{name}-%{version}.tar.xz
# Source0-md5:	74ce29e3b30584498cc29287ae049068
Patch0:		%{name}-nokde.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.29.15
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.3
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Provides:	xdg-menus
Obsoletes:	gnome-menus-filter-default
Obsoletes:	gnome-menus-filter-desktop
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec .

%description -l pl.UTF-8
Pakiet zawiera implementację specyfikacji menu systemów biurkowych z
freedesktop.org: http://www.freedesktop.org/Standards/menu-spec .

%package editor
Summary:	Simple menu editor
Summary(pl.UTF-8):	Prosty edytor menu
Group:		X11/Applications
Requires:	python-pygobject3
Requires:	xdg-menus

%description editor
Simple menu editor.

%description editor -l pl.UTF-8
Prosty edytor menu.

%package libs
Summary:	gnome-menus library
Summary(pl.UTF-8):	Biblioteka gnome-menus
Group:		Libraries
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
Requires:	glib2-devel >= 1:2.29.15

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
%patch0 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-static \
	--enable-python
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/GMenuSimpleEditor/*.py

install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/applications-merged

# not supported by glibc (as of 2.13-3)
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{gn,io}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_sysconfdir}/xdg/menus
%{_datadir}/desktop-directories

%files editor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gmenu-simple-editor
%{_datadir}/%{name}
%{_desktopdir}/gmenu-simple-editor.desktop
%dir %{py_sitedir}/GMenuSimpleEditor
%{py_sitedir}/GMenuSimpleEditor/*.py[co]

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

%files static
%defattr(644,root,root,755)
%{_libdir}/libgnome-menu-3.a
